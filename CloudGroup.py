#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:19:19 2019

@author: Adamlkl
"""
import DriveManager
import pickle 

class CloudGroup:
    
    def __init__(self, validClients, lock, listener, key):
        super(CloudGroup,self).__init__()
        self.valid  = validClients
        self.lock = lock
        self.listener = listener
        self.key = key

user_list = set()

def usage():
    print "Command List: \n1. add <username> \n2. remove <username> \n4. list \n4. quit\n"
    
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
        infile = open(filename,'rb')
        user_list = pickle.load(infile)
        infile.close()
    except IOError:
        print "Could not read file:", filename
        user_list = set()
    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)
    
    running = True
    
    while running:
        command = raw_input('How may I help you?\n')
        argv = command.split(' ')
        
        if argv[0] == 'add':
            user_list.add(argv[1])
            
        elif argv[0] == 'remove':
            user_list.remove(argv[1])
            
        elif argv[0] == 'quit':
            #save user files
            users = open('UserList','wb')
            pickle.dump(user_list,users)
            users.close()
            running = False
            print 'Goodbye'
            
        elif argv[0] == 'list':
            print 'Users:'
            for x in user_list:
                print(x)
                
        else:
            usage()
    
    
    
if __name__ == '__main__':
    main()