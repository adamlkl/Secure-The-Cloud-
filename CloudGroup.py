#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:19:19 2019

@author: Adamlkl
"""
import os
import time
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
    
    # change symmetric key of the CloudGroup
    def change_key(self,new_key):
        self.key = new_key
        
    # shut down the CloudGroup
    def close(self):
        self.running = False
        
    ''' 
        - continously listens to users
        - get public key from valid users 
        - encrypt symmetric key with corresponding public key
        - send encryted symmetric key back to the user
    '''
    def run(self):
        while True:
            connection = self.listener.accept()
            message = []
            try:
                message = connection.recv()
            except:
                pass
            # print(msg)
            if len(message)==3:  
                self.lock.acquire()
                if message[0] in self.users:
                    client_address = ('localhost', message[1])
                    response = Client(client_address, authkey=b'secret password')
                    
                    public_key = KeySaver.load_public_key(message[2])
                    encrypted_key = Encryptor.encrypt_symmetric_key(public_key, self.key)
                    response.send(encrypted_key)
                    response.close()
                else:
                    print('Unauthorised access by %s' % (message[0]))
                self.lock.release()
                
            connection.close()
        
    
# print commands in usage list 
def usage():
    print "Command List: \n1. add <username> \n2. remove <username> \n4. list \n4. quit\n"

'''
    - decrypt all the files in drive folder using old symmetric key
    - create new symmteric key and save it 
    - encrypt all the files in drive folder using new symmetric key
'''
def reset(key, drive, client_handler, sym_key_filename):
    folder = drive.ListFile({'q': "'17oua44SP5sR6E_g_h3a9Ua5qjHqAFvFy' in parents and trashed=false"}).GetList()
    DriveManager.decrypt_all_files(key, folder)
    new_key = Encryptor.generate_key()
    with open(os.path.join("SymmetricKey",sym_key_filename), 'wb') as key_file:
        key_file.write(new_key)
    client_handler.change_key(new_key)
    DriveManager.encrypt_all_files(new_key, folder)
           
def main():
    groupname = raw_input("Enter group name:\n") 
    group_path = os.path.join("Groups",groupname)
    if not os.path.isdir(group_path):
        os.mkdir(group_path)
        
    # filename = os.path.join(group_path,'UserList')
    filename = 'UserList'
    # load users in CloudGroup
    try:
        infile = open(filename,'rb')
        user_list = pickle.load(infile)
        infile.close()
    except IOError:
        print "Could not read file:", filename
        user_list = set()
        
    # load Symmetric key 
    sym_key_filename = 'Symmetric_Key.txt'
    try:
        with open(os.path.join("SymmetricKey",sym_key_filename), 'rb') as key_file:
            sym_key = key_file.read()       
    except:
        print "Could find symmetric key file:", filename
        sym_key = Encryptor.generate_key()
        with open(os.path.join("SymmetricKey",sym_key_filename), 'wb') as key_file:
            key_file.write(sym_key)
         
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
        - Create listener to receive requests from users 
        - attempting to establish connection with users to send symmetric 
          key for encryption of files
    '''   
    address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
    listener = Listener(address, authkey=b'secret password')
    lock = threading.Lock()
    client_handler = CloudGroup(user_list, lock, listener, sym_key)
    client_handler.start()
    running = True
    
    while running:
        command = raw_input('How may I help you?\n')
        argv = command.split(' ')
        # use lock to prevent anyone contacting CloudGroup at during management 
        lock.acquire()
        
        # add user to list 
        if argv[0] == 'add':
            user_list.add(argv[1])
        
        # remove user from list
        elif argv[0] == 'remove':
            user_list.remove(argv[1])
            reset(sym_key, drive, client_handler, sym_key_filename)
        
        # shut down CloudGroup
        elif argv[0] == 'quit':
            #save user files
            users = open('UserList','wb')
            pickle.dump(user_list,users)
            users.close()
            client_handler.close()
            running = False
            print 'Goodbye' 
        
        # print valid users 
        elif argv[0] == 'list':
            print 'Users:'
            for x in user_list:
                print(x)
                
        # print usage 
        else:
            usage()
        lock.release()
    
    
if __name__ == '__main__':
    main()