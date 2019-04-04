#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:35:29 2019

@author: Adamlkl
"""
'''
    https://docs.python-guide.org/scenarios/crypto/
'''
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

class Encryptor:
    
    def generate_key(self):
        key = Fernet.generate_key()
        return key
    
    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048, 
            backend=default_backend())
        return private_key
                
    def encrypt(self, some_file, key):
        cipher_suite = Fernet(key)
        encrypted_file = cipher_suite.encrypt(file)
        return encrypted_file
        
    def decrypt(self, encrypted_file, key):
        cipher_suite = Fernet(key)
        decrypted_file = cipher_suite.decrypt(encrypted_file)
        return decrypted_file

def main():
    encryptor = Encryptor()
    ecrypted_text = encryptor.encrypt(some_file, key) 
    
if __name__ == '__main__':
    main()