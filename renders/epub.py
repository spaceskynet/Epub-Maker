#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,tempfile,chardet
from os import path,mkdir
from renders.ebook import EBooker
from renders.config import Configer
from zipfile import ZipFile,  ZIP_DEFLATED
from mako.template import Template

class EpubWriter(ZipFile):
    def write_content(self,file_name,content):
        temp = tempfile.TemporaryFile()
        #handle, tmp_file_name = tempfile.mkstemp()

        temp.write(content)
        temp.seek(0)
        
        self.writestr(file_name,temp.read())
        temp.close()
        #try:
            #os.remove(tmp_file_name)
        #except:
            #pass
            #print('Remove %s Error!' % tmp_file_name)

    
class Epuber(EBooker):
    __slots__ = ['conf', 'content', 'main_path', 'style_path',
                 'image_path', 'text_path']
    def __init__(self,config_file_name):
        self.conf=Configer(config_file_name)
        self.content=EBooker()
        self.content.update_meta_file(self.conf.read_meta_file())
        self.content.update_chapters(self.conf.read_chapters())
        self.main_path,self.style_path,self.image_path,self.text_path='OEBPS','Styles','Images','Text'
        self.style_path=path.join(self.main_path,self.style_path)
        self.image_path=path.join(self.main_path,self.image_path)
        self.text_path=path.join(self.main_path,self.text_path)
    
    #check the charset
    def detectCode(self,path): 
        with open(path, 'rb') as file: 
            data = file.read(20000) 
            dicts = chardet.detect(data) 
            #print(dicts)
            return dicts["encoding"]
    
    def save(self,format):
        if format not in ('epub','txt'): return 1
        if self.content.renderer not in ('text'): return 2
        if not path.exists(self.content.output_folder):
            mkdir(self.content.output_folder)
        # Create vars
        style_template='style.css'
        opf_template='content.opf'
        ncx_tempalte='toc.ncx'
        chapter_template='chapterTemplatePlain.html'
        part_template='partTemplatePlain.html'
        cover_template='titlepage.html'
        save_place=path.join(self.content.output_folder,self.content.title+'.'+format)
        # Create ZIP object
        EBook_file=EpubWriter(save_place,'w',ZIP_DEFLATED)
        # Check Cover image is exist or not
        if self.content.cover_art is not None:
            cover_file=path.join(self.image_path,self.content.cover_art)
            try:
                EBook_file.write(path.join(self.content.source_folder,self.content.cover_art), arcname=cover_file)
            except:
                print('Template Cover_art File Not Found Error!')
        # Write Epub Base Files
        for filename in [path.join('META-INF','container.xml'),'mimetype',path.join(self.style_path,style_template),path.join(self.text_path,cover_template)]:
            src=path.join(self.content.template_folder,filename)
            EBook_file.write(src,arcname=filename)
        # Write opf & ncx
        book = {}
        for (name,value) in vars(self.content).items():
            if name in ('chapters'): continue
            book[name] = getattr(self.content, name)
        #print(book)
        for template in [opf_template,ncx_tempalte]:
            template_file = path.join(self.content.template_folder, self.main_path,template)
            #print(Template(filename=template_file,
            #                        default_filters=['decode.utf8'],
            #                        input_encoding='utf-8').list_defs())
            xml_content = Template(filename=template_file,
                                   default_filters=['decode.utf8'],
                                   input_encoding='utf-8',output_encoding='utf-8').render(**book)
            EBook_file.write_content(path.join(self.main_path,template), xml_content)   
        
        # Write parts & chapters
        for j, part in enumerate(self.content.parts):
            
            xml = None
            filename = path.join(self.content.template_folder,self.text_path,part_template)

            xml = Template(filename=filename,default_filters=['decode.utf8'],input_encoding='utf-8',output_encoding='utf-8').render(title=part['partname'])

            if xml is not None:
                EBook_file.write_content(path.join(self.text_path,'chapter_%04d.html' % j), xml)    
            
            for i, (title, Path, num) in enumerate(part['chapters']):
                #print(title, content, num)
                xml = None
                filename = path.join(self.content.template_folder,self.text_path,chapter_template)
                Path=path.join(self.content.source_folder,Path)
                with open(Path, "r",encoding='{0}'.format(self.detectCode(Path)),errors='ignore') as f:
                    content = self.escape_text_to_html(f.read())
                #print(content)
                # make more html like
                xml = Template(filename=filename,default_filters=['decode.utf8'],input_encoding='utf-8',output_encoding='utf-8').render(title=title,content=content)

                if xml is not None:
                    EBook_file.write_content(path.join(self.text_path,'chapter_%04d_%04d.html' % (j,i)), xml)
        return 0
