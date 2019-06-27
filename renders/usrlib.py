#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,re,yaml
import renders.epub,renders.txt

def check_constvalue(conf):
    constvalue=['title', 'primary_author', 'language','renderer', 'chapters','source_folder']
    for keys in constvalue:
        if keys not in conf:
            return 'Please input the [%s] elements!' % keys
        if conf[keys] == None:
            return 'Please input the [%s] value!' % keys
    return True

def check_config_file(arg):
    if os.path.exists(arg['CONFIG_FILE']) is False: return 1
    f=open(arg['CONFIG_FILE'],encoding='utf-8')
    try:
        conf=yaml.load(f, Loader=yaml.FullLoader)#
    except:
        return 2
    if check_constvalue(conf) is not True: return 3
    for part in conf['chapters']:
        if len(part['name']) != len(part['file']): return 4
    return 0

def make_Ebook(arg):
    if arg['--format'] in ('epub',None):
        Ebook=renders.epub.Epuber(arg['CONFIG_FILE'])
        #print(Ebook)
        return Ebook.save('epub')
    elif arg['--format'] == 'txt':
        Ebook=renders.txt.Txter(arg['CONFIG_FILE'])
        return Ebook.save('txt')
        
def run(arg):
    if arg['--format'] not in ('epub', 'txt', None):
        print ("ERROR: Only support the epub or txt format!, '-f epub/txt'")
        exit(-1)
    ErrorsC=[\
            'The config is all right!',\
            'ERROR: No such conf file!',\
            'ERROR: Conf format error!',\
            'ERROR: Conf is uncomplete!',\
            'ERROR: The number of <name> must equal the number of <file>!'\
            ]
    ErrorsM=[\
            'The epub book is done!',\
            'ERROR: Only support the epub or txt format!',\
            'ERROR: Only support the text renderer!',\
            'The txt book is done!'\
            ]
    
    if arg['check']:
        print(ErrorsC[check_config_file(arg)])
    
    if arg['make']:
        msg=check_config_file(arg)
        if msg !=0 : 
            print(ErrorsC[msg])
        else:
            print(ErrorsM[make_Ebook(arg)])