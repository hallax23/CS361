# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 09:49:32 2025

@author: user_name
"""

import zmq
    
def remove_non_favorites(flashcards_json):
    """goes through all cards, only adding the favroties to the new deck"""
    
    deck = []
    
    for card in flashcards_json:
        print(card)
        
        if card['favorite'] == 1:
            print('fav found')
            deck.append (card)
            
    return deck
            
    
        
def main():
    
    while True:
        
        print ('conecting to server')
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5561")
        
        print ('waiting for data...')        
        flashcards_json = socket.recv_json()
        
        no_favorites = remove_non_favorites(flashcards_json)
        print(no_favorites)
        
        socket.send_json(no_favorites)
        
        print('removed non-favorites!')
        
main()
        
        