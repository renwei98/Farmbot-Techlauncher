# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 23:34:05 2019

@author: Wei
"""
import yaml, json, sys

file_read = open("file.json", 'r')
if f.mode == 'r':
    contents = file_read.read()
    #contents = sys.stdout.write(yaml.dump(json.load(sys.stdin)))

file_handle = open("file.yaml", 'w+')
file_handle.write(contents)
file_handle.close()
