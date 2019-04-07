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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import os 

def generate_key():
    key = Fernet.generate_key()
    return key

def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048, 
        backend=default_backend())
    return private_key

def encrypt_asymmetric_key(public_key, asym_key):
    encrypted_key = public_key.encrypt(
                        asym_key,
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA256()),
                            algorithm=hashes.SHA256(),
                            label=None
                        )
                    )
    return encrypted_key
# put os here 
# take filename 
def encrypt(plain_text, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(plain_text)

def decrypt(encrypted_text, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_text)
    
def encryptt(filename, key):
    cipher_suite = Fernet(key)

    plain_file = open(filename, "rb")
    plain_text = plain_file.read()
    plain_file.close()

    encrypted_text = cipher_suite.encrypt(plain_text)
    encrypted_file = open(filename+".aes", "wb+")
    encrypted_file.write(encrypted_text)
    encrypted_file.close()

def decryptt(filename, key):
    cipher_suite = Fernet(key)
    
    '''
    with open(os.path.join("EncryptedFiles",filename), 'rb') as encrypted_file:
        encrypted_text = encrypted_file.read()
        encrypted_file.close()
    '''
    encrypted_file = open(filename+".aes", "rb")
    encrypted_text = encrypted_file.read()
    encrypted_file.close()
    
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    if '/' in filename:
        index = filename.rfind('/')
        format_name = filename[0:index]
        format_name = format_name + "/decrypted_"
        format_name = format_name + filename[index+1:]
        decrypted_file = open(format_name, "wb+")
    else:
        decrypted_file = open("decrypted_"+filename, "wb+")
    decrypted_file.write(decrypted_text)
    decrypted_file.close()

def main():
    key = generate_key()
    encrypt("testfiles/COPYLIST.txt",key)
    decrypt("testfiles/COPYLIST.txt",key)
    
if __name__ == '__main__':
    main()