from src.sequence import generate_random_sequence, validate_sequence
from src.properties import compute_properties
from src.fitness import compute_fitness
from src.operators import mutate, crossover
import math

def test_sequence_generation():
    seq = generate_random_sequence(50)
    assert len(seq) == 50
    assert validate_sequence(seq)
    
def test_properties_computation():
    seq = "ACDEFGHIKLMNPQRSTVWY" * 2
    props = compute_properties(seq)
    assert "molecular_weight" in props
    assert "gravy" in props
    assert "charge_at_pH_7" in props

def test_fitness_computation():
    seq = "ACDEFGHIKLMNPQRSTVWY"
    config = {
        'targets': {
            'gravy_min': -0.5, 'gravy_max': 0.5,
            'charge_min': -2.0, 'charge_max': 2.0,
            'instability_max': 40.0,
            'max_homopolymer': 4,
            'max_cys_pro_frac': 0.1
        },
        'weights': {
            'gravy': 10, 'charge': 10, 'stability': 15, 'diversity': 5,
            'homopolymer_penalty': -20, 'cys_pro_penalty': -20,
            'charge_penalty': -10, 'gravy_penalty': -10, 'instability_penalty': -10
        }
    }
    score = compute_fitness(seq, config)
    assert isinstance(score, float)
    assert 0 <= score <= 100

def test_mutate():
    seq = "A" * 50
    mutated = mutate(seq, 1.0) # 100% mutation rate
    assert len(mutated) == 50
    # High probability it's not all A's anymore
    assert mutated != seq

def test_crossover():
    p1 = "A" * 50
    p2 = "C" * 50
    c1, c2 = crossover(p1, p2, "single_point")
    assert len(c1) == 50
    assert len(c2) == 50
    assert "A" in c1 and "C" in c1
