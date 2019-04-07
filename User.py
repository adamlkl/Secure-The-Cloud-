#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:11:25 2019

@author: Adamlkl
"""
import os
import sys
import time
import queue
import random 
import threading
import Encryptor
import KeySaver 
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

folder_Id = '17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy'
             
def send_key(username, address, port, group_address, group_listener, user_key):
    ser_key = KeySaver.serialize_key(user_key)
    conn = Client(address, authkey=b'secret password')
    conn.send(username, port, ser_key)
    conn.close()
    # send key to group
    #---

    group_connection = group_listener.accept()

    encryption_key = b"error"
    try:
        encryption_key = group_connection.recv()
    except:
        pass
    group_connection.close()
    '''
    symkey = user_key.decrypt(
                encryption_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
    '''
    return KeySaver.generate_symmetric_key(user_key, encryption_key)
    
    
def retrieve_file(symmetric_key, filename, drive):
    file_list = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        if file1["title"] == filename:
            encoded = file1.GetContentString()    
            #unencoded = f.decrypt(encoded.encode())
            print(encoded)
    
def upload_file(symmetric_key, filename, drive):
    u_file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy"}],'title':filename})
    with open (os.path.join("testfiles",filename),'rb') as uploadfile:
        plain_text = uploadfile.read()
        encrypted_text = Encryptor.encryptt(plain_text, symmetric_key)
        u_file.SetContentString(encrypted_text.decode())
    u_file.Upload()
    
def usage():
    print "Command List: \n1. upload <file> \n2. download <file> \n3. quit\n"
    
def print_fileList(drive):
    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
    
def main():
    username = raw_input("Enter username?\n")
    try:
        user_key = KeySaver.load_key(username)
    except:
        user_key = Encryptor.generate_private_key()
        KeySaver.save_key(username, user_key)
        
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)

    address = ('localhost', 6000)
    port = random.randint(6001,7000)
    group_address = ('localhost', port)     # family is deduced to be 'AF_INET'
    group_listener = Listener(group_address, authkey=b'secret password')
    
    sym_key = send_key(username, address, port, group_address, group_listener, user_key)
    
    running = True
    
    while running:
        inputs = raw_input("How can I help you?\n")
        argv = inputs.split(' ')
        if len(argv)>2:
            print "Usage: python ex.py "
            sys.exit(1)
        else:
            command = argv[0]
            
            if command == "upload":
                filename = argv[1]
                upload_file(sym_key, filename, drive)
            elif command == "download":
                filename = argv[1]
                retrieve_file(sym_key, filename, drive)
            elif command == "quit":
                running = False 
                print "Goodbye"
            else:
                usage()
    
if __name__ == '__main__':
    main()