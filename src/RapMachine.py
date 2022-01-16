"""Main Class for RapMachine.

Artificial Creativity
CIS - LMU Munich
Philipp Wicke, PhD

Authors:
    Miha Kacicnik
    Philipp Koch

2022
"""


class RapMachine:
    """Rap Machine Class."""

    model: any = None

    def __init__(self):
        """Initialize Class."""
        pass

    def load_model(self, **args) -> None:
        """Load Model."""
        pass

    def fine_tune(self, **args) -> None:
        """Fine-tune Model."""
        pass

    def generate(self, input: list, amount: int) -> list:
        """Generate Samples."""
        return []

    def rank(self, candidates: list) -> list:
        """Rank Outputs."""
        return []

    def censor(self, input: str) -> str:
        """Censor Text."""
        return ''
