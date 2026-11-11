"""Sequence retrieval and activation summaries for the protein analysis notebooks."""

import numpy as np
import pandas as pd
import requests


def get_amino_acid_sequence(proteins: list[str]):
    """Fetch canonical sequences for a non-empty list of UniProt accession strings.
    
    Return a dictionary mapping accessions to amino-acid sequences.
    """

    # Check every entry before making any requests to UniProt.
    if not isinstance(proteins, list):
        raise TypeError("Please supply a list of UniProt accession strings.")
    if not proteins:
        raise ValueError("Please supply at least one UniProt accession.")
    if not all(isinstance(protein, str) for protein in proteins):
        raise TypeError("Every UniProt accession must be a string.")
    if any(not protein.strip() for protein in proteins):
        raise ValueError("UniProt accessions must not be empty or blank.")

    amino_acid_dict = {}

    for protein in proteins:
        accession = protein
        url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"
    
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Stop if UniProt returns an HTTP error.
        record = response.json()  # Convert the JSON response into Python data.

        if protein in amino_acid_dict:
            pass
        else:
            amino_acid_dict[f'{protein}'] = record['sequence']['value']

    return amino_acid_dict


def summarise_activations(
    protein: str,
    feature_id: int,
    *,
    amino_acid_dict: dict[str, str],
    activations_by_protein: dict[str, np.ndarray],
) -> pd.DataFrame:
    """Print and return amino-acid counts and statistics for a protein and feature.

    Uses supplied sequence/activation dictionaries; statistics are scaled by 100.
    """
    if not isinstance(protein, str):
        raise TypeError("Please supply a UniProt accession string.")
    if not isinstance(feature_id, (int, np.integer)) or isinstance(feature_id, bool):
        raise TypeError("The feature ID must be an integer.")
    if protein not in amino_acid_dict or protein not in activations_by_protein:
        raise KeyError(f"{protein}: load its sequence and activations first.")

    sequence = amino_acid_dict[protein]
    protein_activations = activations_by_protein[protein]
    if not isinstance(protein_activations, np.ndarray):
        raise TypeError(f"{protein}: activations must be a NumPy array.")
    if (
        not sequence
        or protein_activations.ndim != 2
        or protein_activations.shape[0] != len(sequence)
    ):
        raise ValueError("Expected a non-empty sequence and one activation row per residue.")
    if not 0 <= feature_id < protein_activations.shape[1]:
        raise ValueError(f"Feature {feature_id} is outside the activation array.")

    values = protein_activations[:, feature_id].astype(np.float64) * 100
    if not np.isfinite(values).all():
        raise ValueError("Activations must not contain NaN or infinite values.")

    residues = pd.DataFrame({"Amino acid": list(sequence), "Activation": values})
    summary = residues.groupby("Amino acid")["Activation"].agg(
        Count="count",
        Mean="mean",
        Q1=lambda values: values.quantile(0.25),
        Median="median",
        Q3=lambda values: values.quantile(0.75),
    )

    print(f"{protein} — feature {feature_id}; activation statistics ×100 (not percentages)")
    print(summary.to_string(float_format=lambda value: f"{value:.4f}"))
    return summary
