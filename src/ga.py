from tqdm import tqdm
from typing import Dict, List, Tuple
from src.sequence import generate_random_sequence
from src.fitness import compute_fitness
from src.operators import mutate, crossover, tournament_selection, roulette_selection
from src.diversity import mean_pairwise_hamming, unique_sequence_ratio
import numpy as np

class GeneticAlgorithm:
    def __init__(self, config: Dict, eval_config: Dict):
        self.config = config
        self.eval_config = eval_config
        self.pop_size = config['population_size']
        self.seq_len = eval_config['sequence_length']
        self.mutation_rate = config['mutation_rate']
        self.crossover_rate = config['crossover_rate']
        self.crossover_type = config['crossover_type']
        self.selection_type = config['selection_type']
        self.tournament_size = config.get('tournament_size', 3)
        self.elite_count = config.get('elite_count', 1)
        
        self.population = [generate_random_sequence(self.seq_len) for _ in range(self.pop_size)]
        self.fitness_cache = {}
        self.history = []
        
    def evaluate_fitness(self, seq: str) -> float:
        if seq not in self.fitness_cache:
            self.fitness_cache[seq] = compute_fitness(seq, self.eval_config)
        return self.fitness_cache[seq]
        
    def get_evaluated_count(self) -> int:
        return len(self.fitness_cache)
        
    def step(self):
        fitnesses = [self.evaluate_fitness(seq) for seq in self.population]
        
        # Track stats
        best_idx = np.argmax(fitnesses)
        best_fitness = fitnesses[best_idx]
        mean_fitness = np.mean(fitnesses)
        worst_fitness = np.min(fitnesses)
        
        self.history.append({
            'best_fitness': best_fitness,
            'mean_fitness': mean_fitness,
            'worst_fitness': worst_fitness,
            'best_seq': self.population[best_idx],
            'diversity': mean_pairwise_hamming(self.population),
            'unique_ratio': unique_sequence_ratio(self.population)
        })
        
        # Elitism
        sorted_indices = np.argsort(fitnesses)[::-1]
        next_population = [self.population[i] for i in sorted_indices[:self.elite_count]]
        
        # Selection and reproduction
        while len(next_population) < self.pop_size:
            if self.selection_type == 'tournament':
                p1 = tournament_selection(self.population, fitnesses, self.tournament_size)
                p2 = tournament_selection(self.population, fitnesses, self.tournament_size)
            else:
                p1 = roulette_selection(self.population, fitnesses)
                p2 = roulette_selection(self.population, fitnesses)
                
            if np.random.rand() < self.crossover_rate:
                c1, c2 = crossover(p1, p2, self.crossover_type)
            else:
                c1, c2 = p1, p2
                
            c1 = mutate(c1, self.mutation_rate)
            c2 = mutate(c2, self.mutation_rate)
            
            next_population.extend([c1, c2])
            
        self.population = next_population[:self.pop_size]
        
    def run(self, generations: int, disable_tqdm: bool = False) -> Tuple[List[Dict], Dict]:
        # Evaluate initial population properly for first history entry
        fitnesses = [self.evaluate_fitness(seq) for seq in self.population]
        best_idx = np.argmax(fitnesses)
        self.history.append({
            'best_fitness': fitnesses[best_idx],
            'mean_fitness': np.mean(fitnesses),
            'worst_fitness': np.min(fitnesses),
            'best_seq': self.population[best_idx],
            'diversity': mean_pairwise_hamming(self.population),
            'unique_ratio': unique_sequence_ratio(self.population)
        })

        for _ in tqdm(range(generations), disable=disable_tqdm, desc="Evolution"):
            self.step()
            
        return self.history, self.fitness_cache

