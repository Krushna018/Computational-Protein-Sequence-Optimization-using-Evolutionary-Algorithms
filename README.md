# Computational Protein Sequence Optimization using Evolutionary Algorithms

## Overview
This project implements an evolutionary optimization framework to explore protein sequence space. It aims to generate protein sequences that meet specific physicochemical criteria: targeted hydrophobicity (GRAVY), net charge, stability (instability index), and sequence diversity, while penalizing unfavorable features like long homopolymer runs and excessive cysteine/proline content.

> **Note:** The fitness score used here is a computational proxy based on established bioinformatics metrics (Biopython ProtParam). It is designed to demonstrate evolutionary algorithms and is not an experimental validation of protein function.

## Features
- **Sequence Representation:** Fixed-length standard amino acid strings.
- **Genetic Operators:** Tournament/Roulette selection, Single-point/Two-point/Uniform crossover, Point mutation.
- **Fitness Evaluation:** Multi-objective weighted sum of molecular properties (GRAVY, Charge, Instability, Shannon entropy).
- **Experimentation:** Automated multi-run config comparison with statistical tracking.
- **Analysis:** Generates plots (fitness progress, diversity, property distributions) and a summary report.

## Installation

1. Clone this repository.
2. Ensure you have Python 3.10+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure parameters in `config.yaml` to set targets, weights, and algorithm hyperparameters.
2. Run the main experiment:
   ```bash
   python main.py --config config.yaml
   ```
3. Check `results/` for CSV logs and the summary report, and `figures/` for visualization plots.

## Project Structure
- `config.yaml`: Central configuration.
- `src/`: Core modules (ga, fitness, operators, sequence, properties, diversity, analysis, experiment).
- `main.py`: Entry point.
- `tests/`: Pytest suite.

## Testing
Run unit tests with pytest:
```bash
pytest tests/
```

## Methodology
The algorithm maintains a population of random sequences. In each generation, fitness is evaluated using `src/fitness.py`. High-fitness sequences are selected to breed the next generation through crossover and mutation. The process drives the population towards sequences that maximize the weighted reward terms and minimize penalties.

## Limitations & Future Work
- **Limitations:** The fitness function is heuristic. Sequences optimized this way might not fold correctly in reality since 3D structure is not directly modeled.
- **Future Work:** Integrate structural prediction or pre-trained protein language models (like ESM) to evaluate sequence plausibility. Add varying-length sequences with insertion/deletion mutations.
