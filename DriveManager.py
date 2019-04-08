#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:21:28 2019

@author: Adamlkl
"""
import Encryptor
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# create a child folder with the passed folder name at designated parent folder 
def create_folder(parent_folderid, folder_name, drive):
    file1 = drive.CreateFile({'title': folder_name, "parents":  [{"kind":"drive#fileLink", "id": parent_folderid}], "mimeType": "application/vnd.google-apps.folder"})
    file1.Upload()
    return file1["id"]

# find target folder or file in the passed folder 
def find_folder(folder, folder_name):
    for file1 in folder:
        if file1["title"] == folder_name:
            return file1["id"]
    return None

# encrypt all the files in the drive folder usng key passed
def encrypt_all_files(key, folder):
    for file1 in folder:
        plain_text = file1.GetContentString()    
        encrypted_text = Encryptor.encrypt(plain_text.encode(), key)
        file1.SetContentString(encrypted_text.decode())
        file1.Upload()
        print(encrypted_text)
            
# decrypt all the files in the drive folder usng key passed
def decrypt_all_files(key, folder):
    for file1 in folder:
        find_folder(folder, file1['title'])
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        encrypted_text = file1.GetContentString()    
        decrypted_text = Encryptor.decrypt(encrypted_text.encode(), key)
        file1.SetContentString(decrypted_text.decode())
        file1.Upload()
        print(decrypted_text)

# list all files in the drive folder 
def list_all_files(folder):
    for file1 in folder:
        print('title: %s, id: %s' % (file1['title'], file1['id']))

# clean the drive folder by deleting all files in it 
def delete_all_files(folder):
    for file1 in folder:
        print('Deleting file... title: %s, id: %s' % (file1['title'], file1['id']))
        file1.Delete()
    
def main():
    '''
        - sets up local Google webserver to automatically receive
          authentication code from user and authorizes by itself.
    '''
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.txt")
    
    if gauth.credentials is None or gauth.access_token_expired:
        # Creates local webserver and auto handles authentication.
        gauth.LocalWebserverAuth() 
        
    else: 
        gauth.Authorize()
        
    gauth.SaveCredentialsFile("credentials.txt")
    
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)
    
    key = Encryptor.generate_key()
    folder = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    
    #testing if I can get the encryption and decryption properly
    encrypt_all_files(key, folder)
    decrypt_all_files(key, folder)
    list_all_files(folder)
    delete_all_files(folder)
    
if __name__ == '__main__':
    main()