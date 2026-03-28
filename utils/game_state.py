import random
from words import words

_current_painter = None
_current_word = None
_target_chat_id = None
_is_game_active = False

def start_game(user_id, chat_id=None):
    global _current_painter, _current_word, _is_game_active, _target_chat_id
    _current_painter = user_id
    _target_chat_id = chat_id
    _current_word = random.choice(words)
    _is_game_active = True
    return _current_word

def is_game_active():
    return _is_game_active

def get_target_chat():
    return _target_chat_id

def check_guess(text):
    if not _is_game_active or not _current_word or not text:
        return False
    return text.lower().strip() == _current_word.lower()

def finish_game():
    global _is_game_active, _current_painter, _current_word, _target_chat_id
    _is_game_active = False
    _current_painter = None
    _current_word = None
    _target_chat_id = None