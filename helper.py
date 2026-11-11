"""Sequence retrieval, saved analysis data, and protein activation summaries."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import requests


def _validate_analysis_data(sequences, embeddings, activations, model_settings):
    """Check that protein identities and array dimensions agree before reuse."""
    if not sequences or set(sequences) != set(embeddings) or set(sequences) != set(activations):
        raise ValueError("Sequences, embeddings, and activations must contain the same proteins.")
    for accession, sequence in sequences.items():
        if not isinstance(accession, str) or not isinstance(sequence, str) or not sequence:
            raise ValueError("Each protein must have an accession and a non-empty sequence string.")
        for name, arrays, width in (
            ("embeddings", embeddings, model_settings["embedding_dim"]),
            ("activations", activations, model_settings["sae_dict_size"]),
        ):
            array = arrays[accession]
            if not isinstance(array, np.ndarray) or not np.issubdtype(array.dtype, np.floating):
                raise TypeError(f"{accession}: {name} must be a floating-point NumPy array.")
            if array.shape != (len(sequence), width):
                raise ValueError(f"{accession}: {name} shape does not match its sequence/model settings.")
            if not np.isfinite(array).all():
                raise ValueError(f"{accession}: {name} contain NaN or infinite values.")


def save_analysis(
    path,
    *,
    amino_acid_dict,
    embeddings_by_protein,
    activations_by_protein,
    model_settings,
):
    """Save sequences, full-precision arrays, and metadata in a compressed NPZ archive."""
    _validate_analysis_data(
        amino_acid_dict, embeddings_by_protein, activations_by_protein, model_settings,
    )
    path = Path(path)
    if path.suffix != ".npz":
        raise ValueError("Please use a .npz filename.")

    metadata = {
        "format_version": 1,
        "saved_at_utc": datetime.now(timezone.utc).isoformat(),
        "accessions": list(amino_acid_dict),
        "model_settings": model_settings,
        "sequence_sources": {
            accession: {
                "url": f"https://rest.uniprot.org/uniprotkb/{accession}.json",
                "sha256": hashlib.sha256(sequence.encode("utf-8")).hexdigest(),
                "retrieved_at_utc": None,  # Not retained by the original downloader.
            }
            for accession, sequence in amino_acid_dict.items()
        },
    }
    arrays = {"metadata_json": np.array(json.dumps(metadata))}
    for accession, sequence in amino_acid_dict.items():
        arrays[f"{accession}_sequence"] = np.array(list(sequence), dtype="U1")
        arrays[f"{accession}_embeddings"] = embeddings_by_protein[accession]
        arrays[f"{accession}_activations"] = activations_by_protein[accession]

    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path, **arrays)
    return path


def load_analysis(path):
    """Return sequence, embedding, activation dictionaries and metadata from an NPZ archive."""
    with np.load(path, allow_pickle=False) as archive:
        metadata = json.loads(archive["metadata_json"].item())
        if metadata["format_version"] != 1:
            raise ValueError("Unsupported analysis archive format.")
        sequences, embeddings, activations = {}, {}, {}
        for accession in metadata["accessions"]:
            sequences[accession] = "".join(archive[f"{accession}_sequence"].tolist())
            embeddings[accession] = archive[f"{accession}_embeddings"]
            activations[accession] = archive[f"{accession}_activations"]
            sequence_hash = hashlib.sha256(sequences[accession].encode("utf-8")).hexdigest()
            if sequence_hash != metadata["sequence_sources"][accession]["sha256"]:
                raise ValueError(f"{accession}: saved sequence does not match its recorded hash.")

    _validate_analysis_data(sequences, embeddings, activations, metadata["model_settings"])
    return sequences, embeddings, activations, metadata


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
