"""Main Class for RapMachine.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""

import transformers


class RapMachine:
    """Rap Machine Class."""

    model: any = None

    def __init__(
            self,
            lm_str: str,
            model_path: str,
            gen_config: dict = {
                "num_beams": 5,
                'min_length': 400,
                'top-k': 50}):
        """Initialize Class."""
        self.lm_str: str = lm_str
        self.model_path: str = model_path
        self.gen_config: dict = gen_config

        self.generator: transformers.Pipeline = None
        pass

    def load_model(self, **args) -> None:
        """Load Model."""
        self.generator = transformers.pipeline('text-generation',
            model=self.model_path,
            tokenizer=self.lm_str,
            config = self.gen_config
        )

    def generate(self, input: list, amount: int) -> list:
        """Generate Samples."""
        candidates: list = []
        for i in range(amount):
            candidates.append(self.generator(input)[0]['generated_text'])
        return candidates

    def rank(self, candidates: list) -> list:
        """Rank Outputs."""
        return []

    def censor(self, input: str) -> str:
        """Censor Text."""
        return ''
