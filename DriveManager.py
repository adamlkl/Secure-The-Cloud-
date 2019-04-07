#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:21:28 2019

@author: Adamlkl
"""
import Encryptor
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def encrypt_all_files(key, folder):
    for file1 in folder:
        plain_text = file1.GetContentString()    
        encrypted_text = Encryptor.encryptt(plain_text.encode(), key)
        file1.SetContentString(encrypted_text.decode())
        file1.Upload()
        #unencoded = f.decrypt(encoded.encode())
        print(encrypted_text)
            
def decrypt_all_files(key, folder):
    for file1 in folder:
        encrypted_text = file1.GetContentString()    
        decrypted_text = Encryptor.decryptt(encrypted_text.encode(), key)
        file1.SetContentString(decrypted_text.decode())
        file1.Upload()
        #unencoded = f.decrypt(encoded.encode())
        print(decrypted_text)

def list_all_files(folder):
    for file1 in folder:
        print('title: %s, id: %s' % (file1['title'], file1['id']))

def delete_all_files(folder):
    for file1 in folder:
        print('Deleting file... title: %s, id: %s' % (file1['title'], file1['id']))
        file1.Delete()
    
def main():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)
    
    key = Encryptor.generate_key()
    folder = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    
    #testing if I can get the encryption and decryption properly
    encrypt_all_files(key, folder)
    decrypt_all_files(key, folder)
    list_all_files(folder)
    
if __name__ == '__main__':
    main()