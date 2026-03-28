import random
from words import words

current_word = None
drawer = None


def start_game(user_id):
    global current_word, drawer

    current_word = random.choice(words)
    drawer = user_id

    return current_word


def check_guess(text):
    global current_word
    return text.lower() == current_word


def next_round(user_id):
    global current_word, drawer

    drawer = user_id
    current_word = random.choice(words)

    return current_word