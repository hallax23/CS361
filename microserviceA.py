## This program will receive flashCards as JSON data and a sorting style, then sort the flashCards accordingly

import zmq
import random

def random_sort(cards):
    """Sorts the flash cards into a random order"""
    random.shuffle(cards)

def alpha_sort(cards):
    """Sorts the flash cards into alphabetical order based on the card's front value"""
    cards.sort(key=lambda item: item["front"].lower())

def favorites_sort(cards):
    """Sorts the flash cards into random order then sorts it so favorites are in front"""
    random_sort(cards)
    cards.sort(key=lambda item: item["favorite"], reverse=True)

def main():
    try: # This outer Try block will casue a clean Exit if any uncaught errors or keyboard interrupt occurs
        context = zmq.Context()
        socket = context.socket(zmq.REP)

        try: 
            socket.bind("tcp://*:5556")
        except zmq.ZMQError as e:
            print(f"Error binding socket: {e}")
            return  # Exits if binding fails

        while True:
            print("\nReady to receive data...")
            try:
                # Receives the data for the type of sorting to be performed or 'Q' to quit
                sortStyle = socket.recv_string()
                print("Instruction data received.")
            except zmq.ZMQError as e:
                print(f"Error receiving sort style: {e}")
                # Informs the client of the error
                socket.send_json(f"Error receiving sort style: {e}") 
                continue 

            if sortStyle == 'Q':
                print("\nQuit code received.")
                break
            
            try:
                # Receives the flash card data as json
                flashCards = socket.recv_json()
                print("Flash card data received.")
            except zmq.ZMQError as e:
                print(f"Error receiving flash cards: {e}")
                # Informs the client of the error
                socket.send_json(f"Error receiving flashcards: {e}")    
                continue

            try:
                # Sorts the flash cards based on the sorting style received
                if sortStyle.lower() == "random":
                    random_sort(flashCards)
                elif sortStyle.lower() == "alpha":
                    alpha_sort(flashCards)
                elif sortStyle.lower() == "faves":
                    favorites_sort(flashCards)
                else:
                    print(f"Unsupported sorting style: {sortStyle}. Try again")
                    socket.send_json(f"Error unsupported sorting style: {sortStyle}")                    
                    continue
            except Exception as e: # Catches general errors from the sorting functions
                print(f"Error occurred during sorting: {e}")
                socket.send_json(f"Error occurred during sorting: {e}")
                continue
                        
            try:
                # Sends the flash cards as JSON back to the client
                socket.send_json(flashCards)
                print(f"{sortStyle} sort complete. \nReturning data to client...")
            except zmq.ZMQError as e:
                print(f"Error sending the final sorted flash cards: {e}")
                continue
        
    finally:
        # Closes the sockets and ends the program
        context.destroy()
        print("Server shut down.")

if __name__ == "__main__":
    main()