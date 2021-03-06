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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# save user's private key using username passed in local folders 
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
    
# load user's private key using username passed 
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

# generate symmetric key using SHA-256 hashing algorithm
def generate_symmetric_key(private_key, encryption_key):
    symkey = private_key.decrypt(
                encryption_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
    return symkey

# load public part of the key pair 
def load_public_key(key):
    return serialization.load_pem_public_key(key,backend=default_backend())