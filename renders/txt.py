#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,chardet
from os import path,mkdir,remove
from renders.ebook import EBooker
from renders.config import Configer

class Txter(EBooker):
    def __init__(self,config_file_name):
        self.conf=Configer(config_file_name)
        self.content=EBooker()
        self.content.update_meta_file(self.conf.read_meta_file())
        self.content.update_chapters(self.conf.read_chapters())
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
        save_place=path.join(self.content.output_folder,self.content.title+'.'+format)
        try:
            EBook_file=open(save_place,'w')
        except:
            pass
        EBook_file.write('<<'+self.content.title+'>>\n'+self.content.primary_author+'\n')
        for part in self.content.parts:
            EBook_file.write(part['partname']+'\n')    
            for (title, Path, num) in part['chapters']:
                EBook_file.write(title+'\n')
                Path=path.join(self.content.source_folder,Path)
                with open(Path, "r",encoding='{0}'.format(self.detectCode(Path)),errors='ignore') as f:
                    text=f.read()
                    for line in text.splitlines(False):
                        if line == '' : continue # delete blank line
                        else: EBook_file.write(line+'\n')
        return 3