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
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def save_key(username, private_key):
    '''
    pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
    )
    '''
    pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
    )
    with open(os.path.join("Users",username), 'wb') as key_file:
        key_file.write(pem)
    
def load_key(username):
    with open(os.path.join("Users",username), 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key
    
# serialize public key
def serialize_key(private_key):
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    return pem
