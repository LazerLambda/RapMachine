"""Base Class for RapMachine.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""

import datetime
import os
import re
import time
import torch
import transformers

ERROR: str = "ERROR:\n\t-> %s."


class RapMachineBase:
    """Rap Machine Class."""

    model: any = None

    WORKING: str = "@%s: %s - still workin' hard."

    def __init__(
            self,
            model_path: str,
            slurlist_path: str):
        """Initialize Class."""
        assert isinstance(model_path, str),\
            ERROR % "'model_path' must be a string"
        assert os.path.isdir(model_path),\
            ERROR % f"'{model_path}' is no valid model path."

        self.model_path: str = model_path

        self.generator: transformers.Pipeline = None

        self.slur_list: list = self.load_slur_list(slurlist_path)
        self.slur_dict: dict = self.build_slur_dict(self.slur_list)
        pass

    def load(self, **args) -> None:
        """Load Model and Tokenizer."""
        raise NotImplementedError()

    def working_msg(self, user: str) -> str:
        raise NotImplementedError()


    @staticmethod
    def preprocess(inputstr) -> str:
        # remove RT: @...:

        regex_rt = r"^(RT @[A-Za-z0-7]+:)(.*)$"
        if bool(re.match(regex_rt, inputstr)):
            ouput = inputstr
            try:
                match = re.search(regex_rt, inputstr)
                output = match.group(2)
            except:
                pass
            return output
        else:
            return inputstr
        
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
        assert isinstance(input_str, str),\
            ERROR % f"Input to 'censored_data' must be of type str but is of type {type(input_str)}"
        censored_song = ''.join(slur_dict.get(word.lower(), word) for word in re.split('(\W+)', input_str))
        return censored_song

    def generate(
            self,
            input_data: any,
            amount: int,
            max_length: int = 512,
            min_length: int = 0,
            num_beams: int = 2,
            top_k: int = 100,
            top_p: float = 0.95,
            do_sample: bool = False,
            repetition_penalty: float = 2.5,
            length_penalty: float = 1.0,
            early_stopping: bool = True,
            skip_special_tokens: bool = True,
            clean_up_tokenization_spaces: bool = True) -> list:
        """Generate Samples.

        # TODO Documentation
        Args
            keywords (list): list of tokens from which a
                rap is to be generated
            amount (int): number determining how many
                candidates will be generated
            max_length (int): maximal length for candidates
            min_length (int): minimal length for candidates
            num_beams (int): length of beam when using beam search
            top_k (int): top k tokens used in top-k sampling
                (https://arxiv.org/pdf/1904.09751.pdf)
            top_p (float): in [0,1], determining the probability
                mass for top p tokens
            do_sample (bool): deactivate top-k and sample
                from distribution
            repetition_penalty (float): 
            # TODO

        Returns
        -------
        # TODO
        """
        raise NotImplementedError()

    def rank(self, candidates: list) -> list:
        """Rank Outputs."""
        return candidates

    def censor(self, input_str: str) -> str:
        """Censor Text."""
        return self.censor_data(input_str, self.slur_dict)
