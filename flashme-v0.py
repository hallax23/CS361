# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:01:58 2025

@author: user_name
"""

import json
import zmq

class player:
    """
    used to keep track of current deck, and maybe future features
    """
    def __init__(self):
        self.deck = None

class flashCard:
    """
    used to store each flashcards info
    """
    def __init__(self, front, back, favorite=0):
        self.front = front
        self.back = back
        self.favorite = favorite
        
    def convert_to_dict(self):
        
        return {"front": self.front, "back":self.back, "favorite": self.favorite}


def main():
    """
    starts us off by initializing the player object, and calling the first two pages
    """
    player()
    welcome_message()
    home_page()
    

def welcome_message():
    """
    prints out welcome message
    """
    print ('Welcome to Flash Me! The CLI based flashcard app, designed to help you memorize stuff.')
    
def home_page():
    """
    the main menu
    """
    
    # choice for page nav
    print ('Please select an option from below by typing the corresponding number, and hitting enter.')
    
    print ('0. Create deck')
    print ('1. Info')
    print ('2. Exit')
    print ('3. Import deck')
    choice = make_choice(3)
    
    if choice == 0:
        create_deck()
    if choice == 1: 
        info_page()
    if choice == 2:
        return
    if choice ==3:
        import_json()
    
def info_page():
    """
    the info page
    """
    
    # prints out general info
    print ('This app was created by Axell Hall for a class while attending '
           'Oregon State. Using this app, you can create a deck of flashcards '
           'and practice it. All options will be given to you in a numbered '
           'format. To select an option enter the corresponding number, and '
           'then hit enter. You will also have to hit enter after every term '
           'definition you add to flashcards. Flash responsibly!')
    
    # choice for exit
    print ('0. Back')
    
    choice = make_choice(0)
    if choice == 0:
        home_page()
        
def deck_selected_page():
    """
    page you go to one a deck is selected
    """
    
    # options for what to do w deck
    print ('What would you like to do with the deck you have selected?')
    
    print ('0. Practice selected deck')
    print ('1. Select another deck (home page)')
    print ('2. Randomize order')
    print ('3. Export to JSON')
    print ('4. Remove non-favorite cards')
    
    choice = make_choice(4)
    if choice == 0:
        practice_deck(player.deck)
    if choice == 1:
        
        # over write warning
        print ('Are you sure you wish to contiue? Creating a new deck will overwrite any unsaved data.')
        
        print ('0. Yes')
        print ('1. No')
        
        choice = make_choice(1)
        if choice == 0:
            home_page()
        if choice == 1:
            deck_selected_page()
            
    if choice == 2:
        sort_json(convert_to_json())
    if choice == 3:
        export_to_json(convert_to_json())
    if choice == 4:
        remove_favorites()
        
        
        

        
def create_deck():
    """
    used to create a deck of flashcards
    """

    deck = []
    
    # start the loop
    keep_going = 1
    
    while keep_going == 1: 
        
        # gets flashcard data
        print('Enter the front of the flashcard (term), then hit enter:')
        front = input()
        print('Enter the back of the flashcard (definition), then hit enter:')
        back = input()
        new_card = flashCard(front, back)
        deck.append(new_card)
        
        # option to make more
        print('Would you like to add another term?')
        
        print ('0. Add another term')
        print ('1. All done')
        
        choice = make_choice(1)
        if choice == 1:
            player.deck = deck
            keep_going = 0
            
    deck_selected_page()
        
def practice_deck(deck):
    """
    takes a deck of flashCards as a parameter, and plays it for user

    """
    
    for card in deck:
        
        # show front of card
        print (card.front)
        
        # choice for what to do next
        print ('0. Reveal definition')
        print ('1. Next term')
        print ('2. Mark as favorite')
        print ('3. Exit')
        
        choice = make_choice(3)
        if choice == 0:
            print (card.back)
        if choice == 2:
            card.favorite = 1
        if choice == 3:
            return deck_selected_page()
    
    # once gone through all cards
    print('You got through the entire deck, congrats!')
    deck_selected_page()

def make_choice(max_choice):
    """
    gets user input for making choices in the CLI. choices should start at 0,
        and go out to mac_choice. mac_choice of 1 means users are choosing 1 or 0
    """
    
    while True:
        
        choice = input()
        
        # checks if user entered a number
        try:
            choice = int(choice)
        except ValueError:
            print ('Please enter a number, then hit enter.')
            continue

        # checks is number is one of the options
        if choice >= 0:
            if choice <= max_choice:
                return choice
            
        print ('The number you entered wasnt an option, please try again.')
        

def convert_to_json():
    """takes the current deck and turns it into json format"""
    
    flashcards_data = [card.convert_to_dict() for card in player.deck]
    
    return flashcards_data
        
def unpack_json(flashcards_json):
    """takes json format flashcard deck and turns it back to normal"""
    
    deck = []

    for card in flashcards_json:
        front = card['front']
        back = card['back']
        favorite = card['favorite']
        new_card = flashCard(front, back, favorite)
        deck.append(new_card)
    
    return deck
    
        
def sort_json(flashcard_json):
    """uses microservice a to randomize order or cards"""
    
    context = zmq.Context()
    print("Client attempting to connect to server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    
    data_to_send = flashcard_json
    
    socket.send_string('random', flags=zmq.SNDMORE)

    socket.send_json(data_to_send)
    
    sorted_flashcards = socket.recv_json()
    
    player.deck = unpack_json(sorted_flashcards)
    
    context.destroy()
    
    deck_selected_page()
    
def export_to_json(flashcard_json):
    """uses microservice b to export to json file"""
    
    context = zmq.Context()
    print("Client attempting to connect to server...")
    try:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5557")
    except KeyboardInterrupt:
        exit()
    
    print ('Type the desired filename and hit enter')
    file_name = input()
    
    socket.send_string(file_name, flags=zmq.SNDMORE)
    socket.send_json(flashcard_json)
    
    confirmation = socket.recv_string()
    
    print(confirmation)
    
    context.destroy()
    
    deck_selected_page()
    
def import_json():
    """uses microservice c to import a json file"""
    
    context = zmq.Context()
    print("Client attempting to connect to server...")
    try:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5558")
    except KeyboardInterrupt:
        exit()
    
    print('Type the name of the JSON file you would like to import')
    file_name = input()
    
    socket.send_string(file_name)
    
    flashcards = socket.recv_json()
    
    player.deck = unpack_json(flashcards)
    
    
    context.destroy()
    
    deck_selected_page()
    
def remove_favorites():
    """uses microservice d to remove non favorite cards"""
    
    print('Would you like to save over the currently selected deck or save as a new deck?')
    print('0. Save over currently selected deck')
    print('1. Save as new deck')
    choice = make_choice(1)
    
    context = zmq.Context()
    print("Client attempting to connect to server...")
    try:
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5561")
    except KeyboardInterrupt:
        exit()
    
    socket.send_json(convert_to_json())
    
    no_fav_flashcards = socket.recv_json()
    
    context.destroy()
    
    
    if choice == 0:
        # overwrites current deck
        player.deck = unpack_json(no_fav_flashcards)
        
    if choice ==1:
        #saves new deck to json
        export_to_json(no_fav_flashcards)
        
    deck_selected_page()
        
    
    
    
    
    
        
    
main()