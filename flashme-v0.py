# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 08:01:58 2025

@author: user_name
"""

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
    def __init__(self, front, back):
        self.front = front
        self.back = back


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
    choice = make_choice(2)
    
    if choice == 0:
        create_deck()
    if choice == 1: 
        info_page()
    if choice == 2:
        return
    
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
    
    choice = make_choice(1)
    if choice == 0:
        practice_deck(player.deck)
    if choice == 1:
        
        # over write warning
        print ('Are you sure you wish to contiue? Creating a new deck will overwrite your old one.')
        
        print ('0. Yes')
        print ('1. No')
        
        choice = make_choice(1)
        if choice == 0:
            home_page()
        if choice == 1:
            deck_selected_page()
        

        
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
        print ('2. Exit')
        
        choice = make_choice(2)
        if choice == 0:
            print (card.back)
        if choice == 2:
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
        
main()