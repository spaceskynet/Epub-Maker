#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Epub Maker

Usage:
    epmk -h
    epmk -v
    epmk check CONFIG_FILE
    epmk make CONFIG_FILE [-f FORMAT]
    
Options:
    -h --help           Show this screen.
    -v --version        Show version.
    -f --format FORMAT  Ebook format [epub /txt ,default: epub] 

'''

from docopt import docopt
import renders.usrlib
    
if __name__ == '__main__':
    arg = docopt(__doc__, version='Epub Maker 0.1')
    #print(arg)
    renders.usrlib.run(arg)