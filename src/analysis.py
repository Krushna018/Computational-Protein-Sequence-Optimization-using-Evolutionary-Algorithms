import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def analyze_and_plot(df_results: pd.DataFrame, df_seqs: pd.DataFrame, config: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    df_results.to_csv("results/evolution_history.csv", index=False)
    df_seqs.to_csv("results/top_sequences.csv", index=False)
    
    sns.set_theme(style="whitegrid")
    
    # 1. Fitness vs generation (mean +/- std)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_results, x='generation', y='best_fitness', hue='config_name', errorbar='sd')
    plt.title("Best Fitness vs Generation (Mean ± SD across runs)")
    plt.savefig(f"{output_dir}/fitness_vs_generation.png", dpi=300)
    plt.close()
    
    # 2. Diversity vs generation
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_results, x='generation', y='diversity', hue='config_name')
    plt.title("Sequence Diversity (Mean Hamming) vs Generation")
    plt.savefig(f"{output_dir}/diversity_vs_generation.png", dpi=300)
    plt.close()
    
    # Analyze final performance
    final_gen = df_results['generation'].max()
    df_final = df_results[df_results['generation'] == final_gen]
    
    # 4. Boxplot comparing configs
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_final, x='config_name', y='best_fitness')
    plt.title("Final Best Fitness Distribution across Configurations")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/config_boxplot.png", dpi=300)
    plt.close()
    
    # Statistics and best config
    best_config_name = df_final.groupby('config_name')['best_fitness'].mean().idxmax()
    
    # Improvment calculation
    initial_gen = df_results[df_results['generation'] == 0]
    improvement_records = []
    
    for cfg in df_final['config_name'].unique():
        cfg_final = df_final[df_final['config_name'] == cfg]
        cfg_initial = initial_gen[initial_gen['config_name'] == cfg]
        for run in cfg_final['run'].unique():
            fin = cfg_final[cfg_final['run'] == run]['best_fitness'].values[0]
            ini = cfg_initial[cfg_initial['run'] == run]['best_fitness'].values[0]
            imprv = ((fin - ini) / ini * 100) if ini > 0 else 0
            improvement_records.append({'config_name': cfg, 'run': run, 'improvement': imprv})
            
    df_improv = pd.DataFrame(improvement_records)
    
    # 5. Distribution of fitness improvement
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df_improv, x='config_name', y='improvement')
    plt.title("Fitness Improvement (%) across Configurations")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/improvement_distribution.png", dpi=300)
    plt.close()
    
    # Write report
    with open("results/summary_report.md", "w") as f:
        f.write("# Optimization Summary Report\n\n")
        f.write(f"- **Total Configurations Tested:** {len(df_final['config_name'].unique())}\n")
        f.write(f"- **Runs per Configuration:** {config['runs']}\n")
        
        evals = len(df_seqs) # not exact total evaluated, but top ones. For total evaluated, we need ga.get_evaluated_count()
        # let's estimate from generations * pop_size
        est_evals_per_run = config['generations'] * config['configurations'][0]['population_size']
        f.write(f"- **Total Candidate Sequences Evaluated (Est. max):** {est_evals_per_run * config['runs'] * len(df_final['config_name'].unique())}\n\n")
        
        f.write("## Best Configuration\n")
        f.write(f"The best configuration based on mean final fitness is: **{best_config_name}**\n\n")
        
        best_improv = df_improv[df_improv['config_name'] == best_config_name]['improvement']
        mean_imprv = best_improv.mean()
        std_imprv = best_improv.std()
        
        f.write(f"### Performance for {best_config_name}\n")
        f.write(f"- Mean Improvement: {mean_imprv:.2f}% ± {std_imprv:.2f}%\n")
        
        f.write("\n## Top 5 Optimized Sequences (Overall)\n")
        top5 = df_seqs.sort_values(by='fitness', ascending=False).drop_duplicates('sequence').head(5)
        f.write(top5[['sequence', 'fitness', 'gravy', 'charge_at_pH_7', 'instability_index', 'config_name']].to_markdown(index=False))
