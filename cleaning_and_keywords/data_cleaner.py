#!/usr/bin/python3

import json
import langid
import re


regex = r'\[(.*?)\]|\[\]|\((.*?)\)|\(\)'
newlines = r'\n{2,}'
whitespaces = r'\s{2,}'
dots = r'\.{2,}'
multiple_exclamation_marks = r'!{2,}'
multiple_question_marks = r'\*?\?{2,}'
noisy_text = r'\*[\w\s,]+\n?'
interjections = r'\{\*[\w\s,]*\*?\},?|\*[\w\s,]*\*'
battlerap_noise = r'Watch the battle '
punctuation_beginning = r'^\.|\+'
other_symbols = r'[<>-]+'


def get_data(filename: str) -> str:
    """Read the data from the scraped JSON files for further processing.

    Args:
        path (str): path to the JSON files

    Returns:
        str: text from the JSON file for data cleaning
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f, strict=False)
            return data
    except FileNotFoundError:
        return "File does not exist."


def check_for_type(item):
    """Check if the lyrics of a song have type list or str.

    Args:
        item : song lyrics from list of raps 

    Returns:
        str: song lirics of type str for regex operations
    """
    if type(item) is list:
        item = " ".join([line for line in item])
        return item
    
    elif type(item) is str:
        return item


def clean_data(filename):
    """Clean noisy data with regex operations.

    Args:
        filename (str): path to file that will be cleaned

    Returns:
        list: list of dictionaries [{song_title}: cleaned_lyrics]
    """
    clean_raps = []
    data = get_data(filename)
    for song in data:
        for key, value in song.items():
            if key == 'lyrics':
                token = check_for_type(value)
                if langid.classify(token)[0] == "en":
                    token = re.sub(regex, "", token)
                    token = re.sub(noisy_text, "", token)
                    token = re.sub(interjections, "", token)
                    token = re.sub(other_symbols, "", token)
                    token = re.sub(battlerap_noise, "", token)
                    token = re.sub(whitespaces, " ", token)
                    token = re.sub(dots, ".", token)
                    token = re.sub(multiple_exclamation_marks, "!", token)
                    token = re.sub(multiple_question_marks, "?", token)
                    token = re.sub(punctuation_beginning, "", token.strip())
                    token = re.sub(newlines, "\n", token)
                    if len(token) > 0:
                        rap_data = {song['title']: token.strip()}
                        clean_raps.append(rap_data)
                        print("Cleaned Song",  song['title'])
    
    return clean_raps


def write_to_json(rap_list, out_file):
    """Write cleaned data to a JSON file.

    Args:
        rap_list (list): list of dictionaries [{song_title}: cleaned_lyrics]
        out_file (str): filename for JSON file
    """
    genius_json = json.dumps(rap_list)
    with open(out_file, "w", encoding="utf-8") as outfile:
        outfile.write(genius_json)


if __name__ == "__main__":
    data = clean_data("/home/mihael/Documents/LMU/WS2122/CK/data/rap_data.json")
    write_to_json(data, "/home/mihael/Documents/LMU/WS2122/CK/data/cleaned_rap_data.json")
