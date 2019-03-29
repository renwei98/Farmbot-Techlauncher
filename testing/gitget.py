# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 17:41:24 2019

@author: Yutian Wang
"""



#download library GitPython using 
#    $ pip install GitPython


import git

def getgit(targetfloder, sourcelink):
    git.Git(targetfloder).clone(sourcelink)
    
    
#example:
#import gitget
#floder = "C:\\\\Users\\User\\.spyder-py3\\dic1"
#git = "https://github.com/dopfer/Farmbot-Techlauncher.git"
#gitget.getgit(floder, git)