"""Test-script for tweet generation.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""

import argparse
import re

import RapMachineBackendBase
import RapMachineBackendGPT2
import RapMachineBackendT5


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Test tweet generation. Provide script with necessary information.')
    parser.add_argument(
        '--path',
        type=str,
        required=True, 
        help='Provide the (absolute) path of the model folder.')    
    parser.add_argument(
        '--model',
        type=str,
        choices=['gpt2', 't5'],
        required=True,
        help='Define which model will be used.')
    parser.add_argument(
        '--input-seq',
        type=str,
        required=True,
        help='Write something, the bot will create a sequence from. For GPT2: Write a start the bot will complete. For T5: Write anything but keep it quoted.')
    parser.add_argument(
        '--off-words',
        type=str,
        required=True, 
        help='Provide the (absolute) path of the .txt file containing offensive words to be censored.')
    parser.add_argument(
        '--amount',
        type=int,
        default=4, 
        help='Amount of candidates to be generated.')   

    args = vars(parser.parse_args())
    model: str = args['model']
    input_str: str = args['input_seq']
    path: str = args['path']
    off_words: str = args['off_words']
    amount: int = args['amount']

    rm: RapMachineBackendBase = None
    if model == 't5':
        import nltk
        from nltk.tokenize import RegexpTokenizer
        from nltk.corpus import stopwords
        stop_words: set = stopwords.words('english')
        rm = RapMachineBackendT5.RapMachineT5(
            path,
            off_words)

        tokenizer = RegexpTokenizer(r'\w+')
        keywords: list = tokenizer.tokenize(input_str)
        keywords = [word for word in keywords if word.lower() not in stop_words]
        
    else:
        rm = RapMachineBackendGPT2.RapMachineGPT2(
            path,
            off_words)

    rm.load()
    model_input: any = input_str if model == 'gpt2' else keywords

    generated = rm.generate(
        model_input, 4)
    ranked = rm.rank(generated)
    censored = list(map(lambda sent: rm.censor(sent), ranked))
    print(censored)