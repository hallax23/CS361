# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 09:49:32 2025

@author: user_name
"""

import zmq
import json

def save_json(flashcards_json, file_name):
    """saves data to json file"""
    
    with open(file_name, 'w') as file:
        json.dump(flashcards_json, file)
        
def main():
    
    while True:
        
        print ('conecting to server')
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5557")
        
        print ('waiting for data...')
        file_name = socket.recv_string()
        
        flashcards_json = socket.recv_json()
        
        save_json(flashcards_json, file_name)
        
        socket.send_string("saved to json!")
        
        print('saved to json!')
        
main()
        
        