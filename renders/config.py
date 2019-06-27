#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml,os,chardet
from os import path

class Configer(object):
    def __init__(self,config_file_name):
        try:
            self.f=open(config_file_name,encoding='utf-8')
        except FileNotFoundError:
            print('No such Conf File!')
            pass
        try:
            self.conf=yaml.load(self.f, Loader=yaml.FullLoader)#
        except:
            print("Conf format error!")
        self.constvalue=[\
                    'isbn', \
                    'cover_art', \
                    'title', \
                    'primary_author',\
                    'secondary_authors', \
                    'language', \
                    'publisher',\
                    #'date', \
                    'renderer', \
                    'chapters', \
                    'template_folder',\
                    'output_folder',\
                    #'format',\
                    'source_folder'\
                    ]

    def read_meta_file(self):
        Dict={}
        Dict.update(self.conf)
        Dict.pop('chapters')
        return Dict
    
    def read_chapters(self):
        parts,num=[],0
        for i,(part) in enumerate(self.conf['chapters']):
            partname,j,partnum=part['part'],0,num
            chapters=[]
            for j in range(0,len(part['name'])):
                #Path=path.join(self.conf['source_folder'],part['file'][j])
                #print(Path)
                #with open(Path, "r",encoding='{0}'.format(self.detectCode(Path)),errors='ignore') as f:
                    #st=f.read()
                    #print(st)
                num=num+1
                chapters.append((part['name'][j],part['file'][j],num))
            parts.append({'partname': partname, 'chapters': chapters, 'num': partnum}) 
            num=num+1
        return parts
        
        