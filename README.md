# Epub Maker

> By:SpaceSkyNet

## Use YML to easily create a ePub file!

### Usage:

    epmk -h
    epmk -v
    epmk check CONFIG_FILE
    epmk make CONFIG_FILE [-f FORMAT]

### Options:

    -h --help           Show this screen.
    -v --version        Show version.
    -f --format FORMAT  Ebook format [epub /txt ,default: epub] 

### RuntimeEnvironment

> python 3.5/3.6
> docopt==0.6.2
> pyyaml==5.1.1
> mako==1.0.12
> chardet==3.0.4

### Yml conf format

```yml
title: "None" #must
primary_author: "None" #must
secondary_authors: [] 
cover_art: "cover.jpg" 
language: "zh-CN" #must
publisher: "Spaceskynet"
isbn: "0123456789"
renderer: "text" #must
template_folder: "template"
source_folder: "source" #must
output_folder: "output"
chapters: #must
  - part: "Part 1"
    name: ['Chapter 1']
    file: ['1.txt']

  - part: "Part 2"
    name: ['Chapter 2']
    file: ['2.txt']

  ...(more part)
```
### Thanks

[ebook-maker](https://github.com/daleobrien/ebook-maker)
