import random
from typing import List, Tuple
from src.sequence import AMINO_ACIDS

def mutate(seq: str, mutation_rate: float) -> str:
    """Applies point mutation to a sequence with given probability per position."""
    seq_list = list(seq)
    for i in range(len(seq_list)):
        if random.random() < mutation_rate:
            seq_list[i] = random.choice(AMINO_ACIDS)
    return "".join(seq_list)

def crossover(parent1: str, parent2: str, crossover_type: str = "single_point") -> Tuple[str, str]:
    """Applies crossover between two parent sequences."""
    length = len(parent1)
    if crossover_type == "single_point":
        point = random.randint(1, length - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    elif crossover_type == "two_point":
        point1 = random.randint(1, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    elif crossover_type == "uniform":
        child1_chars = []
        child2_chars = []
        for p1, p2 in zip(parent1, parent2):
            if random.random() < 0.5:
                child1_chars.append(p1)
                child2_chars.append(p2)
            else:
                child1_chars.append(p2)
                child2_chars.append(p1)
        child1 = "".join(child1_chars)
        child2 = "".join(child2_chars)
    else:
        raise ValueError(f"Unknown crossover type: {crossover_type}")
    
    return child1, child2

def tournament_selection(population: List[str], fitnesses: List[float], tournament_size: int) -> str:
    """Selects an individual using tournament selection."""
    indices = random.sample(range(len(population)), tournament_size)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx]

def roulette_selection(population: List[str], fitnesses: List[float]) -> str:
    """Selects an individual using roulette-wheel selection."""
    min_fit = min(fitnesses)
    # Shift fitnesses to be positive if needed
    if min_fit < 0:
        shifted_fitnesses = [f - min_fit for f in fitnesses]
    else:
        shifted_fitnesses = fitnesses
        
    total_fit = sum(shifted_fitnesses)
    if total_fit == 0:
        return random.choice(population)
        
    pick = random.uniform(0, total_fit)
    current = 0
    for i, fit in enumerate(shifted_fitnesses):
        current += fit
        if current > pick:
            return population[i]
    return population[-1]
