#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:11:25 2019

@author: Adamlkl
"""
import os
import sys
import random 
import Encryptor
import KeySaver
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

folder_Id = '17oua44SP5sR6E_g_h3a9Ua5qjHqAFvF'
             #14nmbiUyCm-Ld7sY2aOO3v4P2JpmYoMzK
             
def send_key(username, address, port, group_address, group_listener, private_key):
    conn = Client(address, authkey=b'secret password')
    ser_key = Encryptor.serialize_key(private_key)
    conn.send(username, port, ser_key)
    conn.close()
    
def retrieve_file(symmetric_key, filename, drive):
    return None 
    
def upload_file(key, filename, drive):
    file4 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": "1gPPLp6BmCAqWxYXDPv8E38H4ZVBe64bY"}],'title':filename})
    with open (os.path.join("groupFiles",filename),'rb') as uploadfile:
        file4.SetContentString(key.encrypt(uploadfile.read()).decode())
    file4.Upload()
    return None
    
def usage():
    print "help"
    
def print_fileList(drive):
    # Auto-iterate through all files that matches this query
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
    
def main():
    inputs = raw_input("How can I help you?")
    argv = inputs.split(' ')
    if len(argv)!=2:
        print "Usage: python ex.py "
        sys.exit(1)
    else:
        command = argv[0]
        filename = argv[1]
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
        # Create GoogleDrive instance with authenticated GoogleAuth instance.
        drive = GoogleDrive(gauth)
        address = ('localhost', 6000)
        port = random.randint(6001,7000)
        group_address = ('localhost', port)     # family is deduced to be 'AF_INET'
        group_listener = Listener(group_address, authkey=b'secret password')
        
        if command == "upload":
            upload_file()
        elif command == "download":
            retrieve_file()
        else:
            usage()
    
if __name__ == '__main__':
    main()