import random
import collections
import numpy as np
from typing import List

def hamming_distance(seq1: str, seq2: str) -> int:
    """Computes Hamming distance between two sequences of equal length."""
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))

def mean_pairwise_hamming(population: List[str]) -> float:
    """Computes the mean pairwise Hamming distance of a population."""
    if len(population) < 2:
        return 0.0
    
    # Subsample if population is too large to compute all pairs efficiently
    sample_size = min(len(population), 100)
    sample = random.sample(population, sample_size)
    
    distances = []
    for i in range(sample_size):
        for j in range(i + 1, sample_size):
            distances.append(hamming_distance(sample[i], sample[j]))
            
    return np.mean(distances) if distances else 0.0

def unique_sequence_ratio(population: List[str]) -> float:
    """Computes the ratio of unique sequences in the population."""
    return len(set(population)) / len(population) if population else 0.0

def per_position_shannon_entropy(population: List[str]) -> List[float]:
    """Computes the Shannon entropy at each position in the sequences."""
    if not population:
        return []
    
    length = len(population[0])
    entropies = []
    
    for i in range(length):
        column = [seq[i] for seq in population]
        counts = collections.Counter(column)
        entropy = -sum((c / len(population)) * np.log2(c / len(population)) for c in counts.values())
        entropies.append(entropy)
        
    return entropies
