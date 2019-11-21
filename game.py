from .exceptions import *
import random
# Complete with your own, just for fun :)
LIST_OF_WORDS = ['LOL', 'HELLO', 'FOOL']


def _get_random_word(list_of_words):
    if not list_of_words:
        raise InvalidListOfWordsException
    return random.choice(list_of_words)


def _mask_word(word):
    if not word:
        raise InvalidWordException
    return '*' * len(word)


def _uncover_word(answer_word, masked_word, character):
    if len(character) > 1:
        raise InvalidGuessedLetterException
    if not answer_word or not masked_word or len(answer_word) != len(masked_word):
        raise InvalidWordException
    character = character.lower()
    new_masked_word = masked_word.lower()
    answer_word = answer_word.lower()
    for alpha in answer_word: #just in case of repeated letters, iterating over each letter in answer_word
        if character == alpha:
            position_of_character = alpha.index(character)
            new_masked_word[position_of_character] = character
    return new_masked_word



def guess_letter(game, letter):
    letter = letter.lower()
    if game['answer_word'] == game['masked_word'] or game['remaining_misses'] == 0:
        raise GameFinishedException
    #letter not in answer
    if game['masked_word'] == _uncover_word(word_to_guess, game['masked_word'], letter):
        game['previous_guesses'].append(letter) #adding to guesses
        game['remaining_misses'] -= 1 #remaining misses go down by one
    #letter in answer
    elif game['masked_word'] != _uncover_word(word_to_guess, game['masked_word'], letter):
        game['previous_guesses'].append(letter) #adding to guesses
        game['masked_word'] = _uncover_word(word_to_guess, game['masked_word'], letter) #updating masked word
    if game['answer_word'] == game['masked_word']:
        raise GameWonException
    if game['remaining_misses'] == 0:
        game['masked_word'] = masked_word
        raise GameLostException


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game
