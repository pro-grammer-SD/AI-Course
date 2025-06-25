# name the file as main.py , uncomment the imports and basic functions, complete  the code by writing remainig functions 

import re, random
from colorama import Fore, init

# Initialize colorama (autoreset ensures each print resets after use)
init(autoreset=True)

# Destination & joke data
destinations = {
     "beaches": ["Bali", "Maldives", "Phuket"],
     "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
     "cities": ["Tokyo", "Paris", "New York"]
 }
jokes = [
     "Why don't programmers like nature? Too many bugs!",
     "Why did the computer go to the doctor? Because it had a virus!",
     "Why do travelers always feel warm? Because of all their hot spots!"
]
 
# Helper function to normalize user input (remove extra spaces, make lowercase)
def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

# Provide travel recommendations (recursive if user rejects suggestions)

# Offer packing tips based on user’s destination and duration

# Tell a random joke

# Display help menu

# Main chat loop

# Run the chatbot
# if __name__ == "__main__":
#    chat()
