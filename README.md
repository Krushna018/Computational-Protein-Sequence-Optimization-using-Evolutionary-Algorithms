# 🧬 Computational Protein Sequence Optimization using Evolutionary Algorithms

> **An evolutionary optimization framework for exploring protein sequence space using Genetic Algorithms and physicochemical constraints.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python\&logoColor=white)](https://www.python.org/) [![Biopython](https://img.shields.io/badge/Biopython-Sequence%20Analysis-4C8CBF)](https://biopython.org/) [![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy\&logoColor=white)](https://numpy.org/) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🔬 Overview

**Computational Protein Sequence Optimization** is a Python-based framework that uses **Evolutionary Algorithms** to explore and optimize protein sequences according to configurable computational objectives.

The system evolves candidate sequences through **selection, crossover, mutation, and constraint handling**. Each sequence is evaluated using physicochemical properties such as **GRAVY, net charge, instability index, molecular weight, amino-acid composition, and sequence diversity**.

The framework is designed to study how evolutionary search can improve a defined computational fitness score while maintaining valid and diverse protein sequences.


---

## 🎯 Project Objectives

The project focuses on four main goals:

1. **Explore protein sequence space** using evolutionary search.
2. **Optimize multiple sequence-level properties** through a configurable fitness function.
3. **Analyze evolutionary behavior** including convergence and population diversity.
4. **Evaluate robustness** through multiple independent optimization runs.

The complete experiment is designed to evaluate **1,000+ candidate sequences across 30 independent runs**.

---

## 🧠 How It Works

```text
                 Reference Protein
                        │
                        ▼
              Population Initialization
                        │
                        ▼
                 Fitness Evaluation
                        │
                        ▼
                    Selection
                        │
                        ▼
               Crossover + Mutation
                        │
                        ▼
               Constraint Validation
                        │
                        ▼
                  New Population
                        │
                        ▼
                 Repeat Generations
                        │
                        ▼
            Best Computational Sequence
```

Each generation evaluates the population and uses the highest-performing candidates to produce the next generation.

---

## 🧬 Genetic Algorithm

The framework implements the main components of a Genetic Algorithm:

### Selection

* Tournament Selection
* Roulette Wheel Selection
* Elitism

### Crossover

* Single-point crossover
* Two-point crossover
* Uniform crossover

### Mutation

* Point mutation
* Multiple-point mutation

All operators are configurable, allowing different evolutionary strategies to be compared experimentally.

---

## 🎯 Computational Fitness

The fitness function combines several normalized objectives:

$$
F(S) =
w_1R_{hydrophobicity}
+w_2R_{stability}
+w_3R_{charge}
+w_4R_{composition}
-P(S)
$$

Where:

* \(S\) = candidate protein sequence
* \(R\) = normalized reward
* \(w\) = configurable objective weight
* \(P(S)\) = constraint penalty

The framework supports both **target-based objectives** and **maximization/minimization objectives**.

### Properties considered

| Property                   | Description                        |
| -------------------------- | ---------------------------------- |
| **GRAVY**                  | Overall hydrophobicity             |
| **Net Charge**             | Charge-related sequence property   |
| **Instability Index**      | Sequence-based stability heuristic |
| **Molecular Weight**       | Estimated molecular mass           |
| **Isoelectric Point**      | Theoretical pI                     |
| **Aromaticity**            | Aromatic residue fraction          |
| **Amino-acid Composition** | Residue distribution               |
| **Sequence Diversity**     | Population-level variation         |

---

## ⚙️ Constraints

Candidate sequences can be evaluated against configurable constraints such as:

* Valid amino-acid alphabet
* Fixed sequence length
* Maximum distance from reference
* Hydrophobicity range
* Charge range
* Molecular-weight range
* pI range
* Instability-index threshold
* Maximum homopolymer length
* Cysteine/proline limits

Sequences that violate configured constraints can receive penalties or be rejected.

---

## 📊 Experiments & Evaluation

To reduce dependence on a single stochastic run, the framework performs **30 independent optimization runs** using different random seeds.

For each run, it records:

* Initial fitness
* Final fitness
* Fitness improvement
* Best sequence
* Best generation
* Final population diversity
* Number of unique sequences
* Runtime
* Configuration parameters

The results are then aggregated to calculate:

* Mean and median fitness
* Standard deviation
* Minimum and maximum fitness
* Improvement percentage
* Confidence intervals
* Statistical comparisons where appropriate

---

## 📈 Analysis & Visualizations

The project generates visualizations to understand both optimization performance and evolutionary behavior.

### Fitness Analysis

* Best fitness vs. generation
* Average fitness vs. generation
* Fitness distribution across runs

### Diversity Analysis

* Unique sequences over generations
* Average Hamming distance
* Population entropy

### Sequence Analysis

* Reference vs. optimized properties
* Amino-acid composition
* Mutation positions
* Physicochemical property changes

### Configuration Comparison

Different mutation rates, crossover strategies, and population settings can be compared based on:

**Fitness • Diversity • Convergence • Runtime**

All generated figures are stored in:

```text
results/figures/
```

---

## 🏆 Optimized Sequence Analysis

The best computational sequence identified across the experiments is analyzed against the original reference sequence.

The final analysis includes:

```text
Reference Sequence
       ↓
Optimized Sequence
       ↓
Sequence Distance
       ↓
Mutation Positions
       ↓
Property Comparison
       ↓
Fitness Improvement
```

The framework reports the actual measured improvement rather than using hard-coded performance values.

---

## 🛠️ Technology Stack

| Technology               | Purpose                    |
| ------------------------ | -------------------------- |
| **Python**               | Core implementation        |
| **Biopython**            | Protein sequence analysis  |
| **NumPy**                | Numerical computation      |
| **Pandas**               | Experiment data processing |
| **SciPy**                | Statistical analysis       |
| **Matplotlib / Seaborn** | Visualization              |
| **PyYAML**               | Configuration management   |
| **Pytest**               | Unit testing               |
| **Streamlit**            | Interactive dashboard      |

---

## 📁 Project Structure

```text
protein-sequence-optimization/
│
├── data/
│   ├── input/
│   └── results/
│
├── src/
│   └── protein_optimizer/
│       ├── sequence_utils.py
│       ├── fitness.py
│       ├── constraints.py
│       ├── mutation.py
│       ├── crossover.py
│       ├── selection.py
│       ├── genetic_algorithm.py
│       ├── experiment.py
│       ├── metrics.py
│       └── visualization.py
│
├── notebooks/
├── scripts/
├── tests/
├── app/
├── results/
├── config.yaml
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/protein-sequence-optimization.git
cd protein-sequence-optimization
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Run a single optimization

```bash
python scripts/run_optimization.py
```

### Run the complete experiment

```bash
python scripts/run_experiments.py --runs 30
```

### Analyze results

```bash
python scripts/analyze_results.py
```

### Run tests

```bash
pytest tests/
```

### Launch the interactive dashboard

```bash
streamlit run app/streamlit_app.py
```

---

## ⚙️ Configuration

Experiment parameters are controlled through `config.yaml`, including:

```yaml
population:
  size: 50

evolution:
  generations: 50
  mutation_rate: 0.05
  crossover_rate: 0.80
  elite_size: 2

experiment:
  runs: 30
```

This allows experiments to be modified without changing the core source code.

---

## ⚠️ Limitations

This project focuses on **computational sequence-level optimization**.

The current fitness function does not directly model:

* Protein 3D structure
* Folding dynamics
* Binding affinity
* Cellular environment
* Experimentally measured biological activity

Therefore, an increase in computational fitness should **not** be interpreted as proof of improved biological performance.

---

## 🔭 Future Work

Potential extensions include:

* 🤖 Protein Language Models such as ESM
* 🧬 Structure-aware fitness functions
* 🎯 Multi-objective optimization using NSGA-II
* 🔗 Protein structure and binding analysis
* 🔄 Insertion/deletion-based variable-length evolution
* 📈 Machine-learning surrogate fitness models

---




---

<p align="center">

⭐ **If you find this project interesting, consider starring the repository!**

</p>
