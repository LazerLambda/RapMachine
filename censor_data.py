#!/usr/bin/python3

"""Script for censoring bad words in twitter bot output."""


import re


def load_slur_list(filename):
    """Load list with ioffensive words.

    Args:
        filename (str): filename of text file with offensive words

    Returns:
        list: list of offensive words
    """
    with open(filename, "r") as slur_list:
        output = slur_list.read()
    
    return output.split()


def build_slur_dict(slur_list):
    """Map offensive words to [CENSORED] token.

    Args:
        slur_list (list): list of offensive words

    Returns:
        dict: dictionary -> {'offensive word': '[CENSORED]'}
    """
    slur_dict = {}
    for slur in slur_list:
        slur_dict[slur] = "[CENSORED]"

    return slur_dict


def censor_data(input_str, slur_dict):
    """Apply censorship to string.

    Args:
        input_str (str): string that has to be censored
        slur_dict (dict): dictionary -> {'offensive word': '[CENSORED]'}

    Returns:
        [type]: [description]
    """
    # replace offensive words in string with values from dictionary
    # while splitting the string at non alphanumeric tokens
    censored_song = ''.join(slur_dict.get(word.lower(), word) for word in re.split('(\W+)', input_str))
    return censored_song
