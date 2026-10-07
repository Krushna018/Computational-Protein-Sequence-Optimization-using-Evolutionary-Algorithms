import argparse
from src.experiment import run_experiment
from src.analysis import analyze_and_plot

def main():
    parser = argparse.ArgumentParser(description="Computational Protein Sequence Optimization")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to YAML configuration file')
    args = parser.parse_args()
    
    print(f"Starting evolutionary optimization using config: {args.config}")
    df_results, df_seqs, config = run_experiment(args.config)
    
    print("Optimization complete. Analyzing results and generating plots...")
    analyze_and_plot(df_results, df_seqs, config, output_dir="figures")
    
    print("All tasks finished successfully. Check the 'results/' and 'figures/' directories.")

if __name__ == "__main__":
    main()
