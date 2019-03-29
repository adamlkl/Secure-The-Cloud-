#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 14:35:29 2019

@author: Adamlkl
"""
from cryptography.fernet import Fernet

class Encryptor:
    
    def generate_key(self):
        key = Fernet.generate_key()
        return key
                
    def encrypt(self, file, key):
        cipher_suite = Fernet(key)
        encrypted_file = cipher_suite.encrypt(file)
        return encrypted_file
        
    def decrypt(self, encrypted_file, key):
        cipher_suite = Fernet(key)
        decrypted_file = cipher_suite.decrypt(encrypted_file)
        return decrypted_file