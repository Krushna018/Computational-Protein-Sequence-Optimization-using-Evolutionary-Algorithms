import pandas as pd
import random
import numpy as np
import yaml
from src.ga import GeneticAlgorithm
from src.properties import compute_properties

def run_experiment(config_path: str):
    with open(config_path, 'r') as f:
        full_config = yaml.safe_load(f)
        
    global_seed = full_config.get('global_seed', 42)
    random.seed(global_seed)
    np.random.seed(global_seed)
    
    num_runs = full_config['runs']
    generations = full_config['generations']
    
    all_results = []
    top_sequences = []
    
    for cfg in full_config['configurations']:
        print(f"Running configuration: {cfg['name']}")
        config_eval = {
            'targets': full_config['targets'],
            'weights': full_config['weights'],
            'sequence_length': full_config['sequence_length']
        }
        
        for run_idx in range(num_runs):
            ga = GeneticAlgorithm(cfg, config_eval)
            history, fitness_cache = ga.run(generations, disable_tqdm=True)
            
            # Extract metrics
            initial_best = history[0]['best_fitness']
            final_best = history[-1]['best_fitness']
            improvement = ((final_best - initial_best) / initial_best * 100) if initial_best != 0 else 0
            
            # Convergence time (generations to 95% of final best)
            conv_target = 0.95 * final_best
            conv_gen = next((i for i, h in enumerate(history) if h['best_fitness'] >= conv_target), generations)
            
            eval_count = ga.get_evaluated_count()
            
            for gen, h in enumerate(history):
                all_results.append({
                    'config_name': cfg['name'],
                    'run': run_idx,
                    'generation': gen,
                    'best_fitness': h['best_fitness'],
                    'mean_fitness': h['mean_fitness'],
                    'diversity': h['diversity'],
                    'unique_ratio': h['unique_ratio'],
                })
            
            # Save top sequences
            best_seqs = sorted(fitness_cache.items(), key=lambda x: x[1], reverse=True)[:5]
            for seq, fit in best_seqs:
                props = compute_properties(seq)
                props['sequence'] = seq
                props['fitness'] = fit
                props['config_name'] = cfg['name']
                props['run'] = run_idx
                top_sequences.append(props)
                
            print(f"  Run {run_idx+1}/{num_runs} | Imprv: {improvement:.2f}% | Unique Evals: {eval_count}")

    df_results = pd.DataFrame(all_results)
    df_seqs = pd.DataFrame(top_sequences)
    
    return df_results, df_seqs, full_config
