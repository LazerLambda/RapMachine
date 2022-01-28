"""Main Class for RapMachine.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""
from .RapMachineBackendBase import RapMachineBase as RMB

import datetime
import os
import time
import torch
import transformers

ERROR: str = "ERROR:\n\t-> %s."


class RapMachine(RMB):
    """Rap Machine Class."""

    WORKING: str = "@%s: %s - still workin' hard."

    def load(self, **args) -> None:
        """Load Model and Tokenizer."""
        self.tokenizer: transformers.T5TokenizerFast =\
            transformers.T5TokenizerFast.from_pretrained(
                self.model_path)
        self.model: transformers.T5ForConditionalGeneration =\
            transformers.T5ForConditionalGeneration.from_pretrained(
                self.model_path)

    def working_msg(self, user: str) -> str:
        cr_time: str = str(datetime.datetime.now().time())
        return self.WORKING % (user, str(cr_time[0:5]))

    def generate(
            self,
            input_data: list,
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
        # set up gpu usage
        gpu: bool = True if torch.cuda.is_available() else False
        if gpu:
            torch.device("cuda")
        else:
            device = torch.device("cpu")

        keywords_str: str = " ".join(map(str, input_data))

        candidates: list = []
        for i in range(amount):
            # tokenize
            input_ids: torch.Tensor = self.tokenizer.encode(
                keywords_str,
                return_tensors="pt",
                add_special_tokens=True
            ).to(device)

            # generate
            generated_ids: torch.Tensor = self.model.generate(
                input_ids=input_ids,
                num_beams=num_beams,
                max_length=max_length,
                min_length=min_length,
                repetition_penalty=repetition_penalty,
                length_penalty=length_penalty,
                early_stopping=early_stopping,
                top_p=top_p,
                top_k=top_k,
            )

            # decode candidate
            preds: list = [
                self.tokenizer.decode(
                    g,
                    skip_special_tokens=skip_special_tokens,
                    clean_up_tokenization_spaces=clean_up_tokenization_spaces,
                )
                for g in generated_ids
            ][0]
            candidates.append(preds)
        return candidates