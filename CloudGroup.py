#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:19:19 2019

@author: Adamlkl
"""
import Encryptor

def main():
    key = Encryptor.generate_key()
    Encryptor.encrypt("testfiles/COPYLIST.txt",key)
    Encryptor.decrypt("testfiles/COPYLIST.txt",key)
    
if __name__ == '__main__':
    main()