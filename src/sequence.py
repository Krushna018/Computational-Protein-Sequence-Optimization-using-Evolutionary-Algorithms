import random

AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

def generate_random_sequence(length: int) -> str:
    """Generates a random protein sequence of given length."""
    return "".join(random.choice(AMINO_ACIDS) for _ in range(length))

def validate_sequence(seq: str) -> bool:
    """Validates if a sequence contains only standard amino acids."""
    return all(aa in AMINO_ACIDS for aa in seq)
