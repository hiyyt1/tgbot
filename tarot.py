# tarot.py

import random
import os
from card_data import card_interpretations

cards_dir = os.path.join(os.path.dirname(__file__), "your_path")

def get_random_cards(num_cards=3):
    cards = random.sample(list(card_interpretations.items()), num_cards)
    return cards

def get_random_card():
    card = random.choice(list(card_interpretations.items()))
    return card

def get_card_image_path(card_code):
    file_name = f"{card_code}.jpg"
    file_path = os.path.join(cards_dir, file_name)
    
    if os.path.exists(file_path):
        return file_path
    else:
        return None
