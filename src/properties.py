from Bio.SeqUtils.ProtParam import ProteinAnalysis
import numpy as np
import collections

def compute_properties(seq: str) -> dict:
    """Computes various physicochemical properties for a given sequence."""
    pa = ProteinAnalysis(seq)
    
    # Handling sequences that might fail instability index (e.g., too short or specific unsupported combinations)
    try:
        instability = pa.instability_index()
    except Exception:
        instability = 100.0 # Assign high instability if fails

    # Calculate Shannon entropy
    counts = collections.Counter(seq)
    entropy = -sum((c / len(seq)) * np.log2(c / len(seq)) for c in counts.values())
    
    # Calculate charged and hydrophobic fractions
    charged = sum(counts[aa] for aa in "DEHKR") / len(seq)
    hydrophobic = sum(counts[aa] for aa in "AILMFVWY") / len(seq)
    
    return {
        "molecular_weight": pa.molecular_weight(),
        "isoelectric_point": pa.isoelectric_point(),
        "charge_at_pH_7": pa.charge_at_pH(7.0),
        "gravy": pa.gravy(),
        "instability_index": instability,
        "aromaticity": pa.aromaticity(),
        "aliphatic_index": get_aliphatic_index(counts, len(seq)),
        "charged_fraction": charged,
        "hydrophobic_fraction": hydrophobic,
        "shannon_entropy": entropy
    }

def get_aliphatic_index(counts: collections.Counter, length: int) -> float:
    """Calculates aliphatic index: A + 2.9 * V + 3.9 * (I + L)."""
    a = counts.get('A', 0) / length * 100
    v = counts.get('V', 0) / length * 100
    i = counts.get('I', 0) / length * 100
    l = counts.get('L', 0) / length * 100
    return a + 2.9 * v + 3.9 * (i + l)
