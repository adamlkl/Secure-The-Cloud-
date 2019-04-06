#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 15:51:42 2019

@author: Adamlkl
""" 
''' 
    - https://www.datacamp.com/community/tutorials/pickle-python-tutorial#what 
    - https://security.stackexchange.com/questions/12332/where-to-store-a-server-side-encryption-key
    - https://pypi.org/project/pyAesCrypt/
'''
from cryptography.hazmat.primitives import serialization

class KeySaver:
    
    def save_key(private_key):
        pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
        )
    def get_key():
