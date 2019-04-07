#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:19:19 2019

@author: Adamlkl
"""
import os
import pickle 
import threading
import KeySaver 
import DriveManager 
import Encryptor 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from multiprocessing.connection import Client
from multiprocessing.connection import Listener


class CloudGroup(threading.Thread):
    
    def __init__(self, users, lock, listener, sym_key):
        super(CloudGroup,self).__init__()
        self.users  = users
        self.lock = lock
        self.listener = listener
        self.key = sym_key
        self.running = True
    
    def change_key(self,new_key):
        self.key = new_key
        
    def close(self):
        self.running = False
        
    def run(self):
        while True:
            connection = self.listener.accept()
            message = []
            try:
                message = connection.recv()
            except:
                pass
            #print(msg)
            if len(message)==3:  
                self.lock.acquire()
                if message[0] in self.users:
                    client_address = ('localhost', message[1])
                    response = Client(client_address, authkey=b'secret password')
                    
                    public_key = KeySaver.load_public_key(message[2])
                    encrypted_key = Encryptor.encrypt_asymmetric_key(public_key, self.key)
                    response.send(encrypted_key)
                    response.close()
                else:
                    print('Unauthorised access by %s' % (message[0]))
                self.lock.release()
                
            connection.close()
        
    

def usage():
    print "Command List: \n1. add <username> \n2. remove <username> \n4. list \n4. quit\n"

def reset(key, drive, client_handler, sym_key_filename):
    folder = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    DriveManager.decrypt_all_files(key, folder)
    new_key = Encryptor.generate_key()
    with open(os.path.join("SymmetricKey",sym_key_filename), 'wb') as key_file:
        key_file.write(new_key)
    client_handler.change_key(new_key)
    DriveManager.encrypt_all_files(new_key, folder)
           
def main():
    filename = 'UserList'
    try:
        infile = open(filename,'rb')
        user_list = pickle.load(infile)
        infile.close()
    except IOError:
        print "Could not read file:", filename
        user_list = set()
        
    sym_key_filename = 'Symmetric_Key.txt'
    try:
        with open(os.path.join("SymmetricKey",sym_key_filename), 'rb') as key_file:
            sym_key = key_file.read()       
    except:
        print "Could find symmetric key file:", filename
        sym_key = Encryptor.generate_key()
        with open(os.path.join("SymmetricKey",sym_key_filename), 'wb') as key_file:
            key_file.write(sym_key)
         
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)
    
    address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'secret password')
    lock = threading.Lock()
    client_handler = CloudGroup(user_list, lock, listener, sym_key)
    client_handler.start()
    running = True
    
    while running:
        command = raw_input('How may I help you?\n')
        argv = command.split(' ')
        lock.acquire()
        if argv[0] == 'add':
            user_list.add(argv[1])
            
        elif argv[0] == 'remove':
            user_list.remove(argv[1])
            reset(sym_key, drive, client_handler, sym_key_filename)
            
        elif argv[0] == 'quit':
            #save user files
            users = open('UserList','wb')
            pickle.dump(user_list,users)
            users.close()
            client_handler.close()
            running = False
            print 'Goodbye' 
            
        elif argv[0] == 'list':
            print 'Users:'
            for x in user_list:
                print(x)
                
        else:
            usage()
        lock.release()
    
    
if __name__ == '__main__':
    main()