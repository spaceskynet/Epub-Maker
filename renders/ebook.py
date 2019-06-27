#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, split
import time
import re

# tags that will be left as is when convert text/html to full html
HTML_TAGS = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'em', 'abbr',
             'acronym', 'address', 'bdo', 'blockquote', 'cite', 'q', 'code',
             'ins', 'del', 'dfn', 'kbd', 'pre', 'samp', 'var', 'br', 'br/',
             'br /', 'b', 'i', 'tt', 'sub', 'sup', 'big', 'small', 'hr')

SPACES = {'  ': '&#32;'}  # need a regex here ...

ESCAPES = {'€': '&euro;',
           '"': '&quot;',
           r'\&': '&amp;',
           '<': '&lt;',
           '>': '&gt;',
           #'...': '&hellip;'
           }

def remove_control_chars(s):
    control_chars = ''.join(map(chr, range(0,32)))
    control_chars = control_chars.join(map(chr,range(127,160)))
    control_chars = control_chars.replace('\n','')
    control_char_re = re.compile('[%s]' % re.escape(control_chars))

    return control_char_re.sub('', s)


class EBooker(object):

    def __init__(self):
        #self.constvalue = ['title', 'primary_author', 'language','renderer', 'chapters','source_folder']
        self.isbn = '0123456789'
        self.cover_art = join(split(__file__)[0], 'template','OEBPS','Images','cover.jpg')
        self.title = 'None'
        self.primary_author = "Anonymous"
        self.secondary_authors = []
        self.template_folder = join(split(__file__)[0], 'template')
        self.language = 'zh-CN'
        self.publisher = "None"
        self.renderer = 'text'
        self.output_folder = split(__file__)[0]
        self.source_folder = ""
        self.chapters=[]

    def escape_text_to_html(self, text):
        '''Try can convery plain text, maybe with some html markup into
        full html.
        Each line will be wrapped in a <p></p> tag, if needed
        '''

        # convert unicode characters to html
        _text = ""
        
        #text=remove_control_chars(text)
        #text=text.replace(b'',)
        #for ch in  [160,32,12288]: 
        
        for ch in text:
            if ord(ch) >= 127:
                _text += "&#%d;" % ord(ch)
            else:
                _text += ch
        
        
        text = str(_text)

        # escape all special characters to they display correctly
        # unless they are already escaped
        for key, value in  ESCAPES.items():
            text = re.sub(r'([^\\]|^)%s' % key, r"\1%s" % value, text)

        # restore unicode chars
        # either &#DDD; or &#xDDD; have been escaped
        text = re.sub(r'\&amp;#([xX]?)(\d+);', r'&#\1\2;', text)

        # restore any html tags
        for tag in HTML_TAGS:
            for t in (tag, tag.upper()):
                text = re.sub(r'\&lt;(/?)%s\&gt;' % t, r'<\1%s>' % t, text)

        text = re.sub(r'\&amp;#[xX](\d+);', r'&#x\1;', text)

        # remove escaped chars
        for key, value in  ESCAPES.items():
            text = re.sub(r'\\%s' % key, r"%s" % value, text)

        # add paragraph tags
        paragraphs = []
        for line in text.splitlines(False):
            for tag in ('p', 'P', 'blockquote', 'BLOCKQUOTE'):
                if line.startswith('<%s>' % t) and line.endswith('</%s>' % t):
                    paragraphs.append(line)
                    break
            if line == '' : continue # delete blank line
            else:
                paragraphs.append("<p>%s</p>" % line)
        return paragraphs
    
    def update_meta_file(self,conf):
        #print(conf)
        for (name,value) in conf.items():
            if name in ('chapters'): continue
            #print(name)
            exec('self.'+name+' = conf["'+name+'"]')
        self.date = time.strftime("%Y-%m-%d", time.localtime()) 
        
    def update_chapters(self,chapters):
        self.parts = chapters
#

if __name__ == "__main__":
    booker=EBooker()
    print(vars(booker))