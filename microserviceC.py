# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 09:49:32 2025

@author: user_name
"""

import zmq
import json

def grab_json(file_name):
    """imports json file data"""

    with open(file_name, "r") as file:
        return json.load(file)  # Load JSON as a Python dictionary or list

        
def main():
    
    
    while True:
        
        print ('conecting to server')
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5558")
        
        print ('waiting for data...')
        file_name = socket.recv_string()
        
        flashcards = grab_json(file_name)
        
        socket.send_json(flashcards)
        
        print('imported json!')
        
main()
        
        