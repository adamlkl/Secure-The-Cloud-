#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:11:25 2019

@author: Adamlkl
"""
import os
import sys
import pickle
import random 
import Encryptor
import KeySaver 
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

folder_Id = '17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy'
             
'''            
    - try to establish connection with CloudGroup
    - send over public key for symmetrical key encryption 
    - get encrypted symmetrical key from CloudGroup
    - if user is not in the userlist, encrypted symmetrical key won't be sent
'''
def retrieve_asymmetrical_key(username, address, port, group_address, group_listener, user_key):
    ser_key = KeySaver.serialize_key(user_key)
    conn = Client(address, authkey=b'secret password')
    conn.send([username, port, ser_key])
    conn.close()

    group_connection = group_listener.accept()

    # res = b"error"
    encryption_key = b"error"
    try:
        # res = group_connection.recv()
        encryption_key = group_connection.recv()
    except:
        pass
    group_connection.close()
    
    # return res
    return KeySaver.generate_symmetric_key(user_key, encryption_key)
    
# download file from drive folder with key passed and save it to downloads
def retrieve_file(symmetric_key, filename, drive, folder_id):
    file_list = drive.ListFile({'q': "'" + folder_id + "' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        # find file to be downloaded 
        if file1["title"] == filename:
            encrypted_text = file1.GetContentString()    
            decrypted_text = Encryptor.decrypt(encrypted_text.encode(), symmetric_key,)
            # printing downloaded text to check results 
            print(decrypted_text)
            
            # save files in downloads
            with open (os.path.join("downloads",filename),'wb') as d_file:
                d_file.write(decrypted_text)
                d_file.close()
    
# encrypt file with key passed and upload it to drive folder 
def upload_file(symmetric_key, filename, drive, folder_id):
    u_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}],'title':filename})
    with open (os.path.join("testfiles",filename),'rb') as uploadfile:
        plain_text = uploadfile.read()
        encrypted_text = Encryptor.encrypt(plain_text, symmetric_key)
        u_file.SetContentString(encrypted_text.decode())
        uploadfile.close()
    u_file.Upload()
    
# print usage of the user page 
def usage():
    print "Command List: \n1. upload <file> \n2. download <file> \n3. quit\n"

# print list of files in drive folder 
def print_fileList(drive):
    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
    
def main():
    # get username
    username = raw_input("Enter username?\n")
    
    '''
        - try to load user's key using username 
        - if found, load the key from file
        - otherwise, create a new one and save it in files 
    '''
    try:
        user_key = KeySaver.load_key(username)
    except:
        user_key = Encryptor.generate_private_key()
        KeySaver.save_key(username, user_key)
        
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
    
    '''
        - attempting to establish connection with CloudGroup to get symmetric 
          key for encryption of files
    '''   
    address = ('localhost', 6000)
    port = random.randint(6001,7000)
    group_address = ('localhost', port)     # family is deduced to be 'AF_INET'
    group_listener = Listener(group_address, authkey=b'secret password')
    
    # crude way of getting available folders 
    file_list = open("Drive Folders",'rb')
    drive_folders = pickle.load(file_list)
    file_list.close()
    
    '''
    drive_folders.pop("sylas ")
    print(drive_folders)
    file_list = open("Drive Folders",'wb')
    pickle.dump(drive_folders,file_list)
    file_list.close()
    '''
    
    folder_id = drive_folders['sylas']
    sym_key = retrieve_asymmetrical_key(username, address, port, group_address, group_listener, user_key)
    '''
    res = retrieve_asymmetrical_key(username, address, port, group_address, group_listener, user_key)
    sym_key = KeySaver.generate_asymmetric_key(user_key, res[0])
    folder_id = res[1]
    '''
    running = True
    
    while running:     
        inputs = raw_input("How can I help you?\n")
        
        # requests for symmetrical key in case it is changed
        sym_key = retrieve_asymmetrical_key(username, address, port, group_address, group_listener, user_key)
        '''
        res = retrieve_asymmetrical_key(username, address, port, group_address, group_listener, user_key)
        sym_key = KeySaver.generate_symmetric_key(user_key, res[0])
        folder_id = res[1]
        '''
        
        # handles instructions from users
        argv = inputs.split(' ')
        if len(argv)>2:
            print "Usage: python ex.py "
            sys.exit(1)
        else:
            command = argv[0]
            
            if command == "upload":
                filename = argv[1]
                upload_file(sym_key, filename, drive, folder_id)
            elif command == "download":
                filename = argv[1]
                retrieve_file(sym_key, filename, drive, folder_id)
            elif command == "quit":
                running = False 
                print "Goodbye"
            else:
                usage()
    
if __name__ == '__main__':
    main()