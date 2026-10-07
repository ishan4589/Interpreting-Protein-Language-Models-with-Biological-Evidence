# Interpreting Protein Language Models with Biological Evidence

See [the project proposal](interpreting-PLMs.MD) for the study's scope. Implementation has not yet begun.

## Environment setup

```bash
conda env create -f environment.yml
conda activate interpreting-plms
jupyter lab
```

If a previous attempt created the Conda environment but failed during pip installation,
repair it without deleting it:

```bash
conda env update -n interpreting-plms -f environment.yml
conda activate interpreting-plms
```

The environment provides Python 3.11, ESM-2 and pretrained InterPLM SAE inference,
protein sequence handling, UniProt downloads, PDF extraction, BM25/TF-IDF retrieval,
analysis, and plotting. Its inference dependencies are based on
[InterPLM's upstream dependencies](https://github.com/ElanaPearl/InterPLM/blob/5f4cbf90a0b3c1c031951ffd0b3b8e11b6f2ed61/requirements.txt).
InterPLM is pinned to a source commit and installed in editable mode to retain its
YAML model configurations; pip may create a local `src/interplm` checkout.
The `git+https://...@<commit>#egg=interplm` entry is pip installation syntax;
the browsable repository is [ElanaPearl/InterPLM](https://github.com/ElanaPearl/InterPLM).

No LLM provider has been selected yet. Hugging Face Transformers supports local
models, and `requests` supports HTTP APIs; add a provider's SDK if the implementation
chooses one. Model weights are downloaded separately when first used.

The environment does not require CUDA. InterPLM defaults to CPU on macOS; an NVIDIA
GPU setup may need a PyTorch wheel matching the machine's CUDA configuration.
On macOS with an `x86_64` Python (Intel or Rosetta), the environment selects
PyTorch 2.2.2, the last release with macOS Intel wheels. Other platforms use 2.8.0.
NumPy is pinned to 1.26.4 to support PyTorch 2.2's tensor/NumPy conversions, and
Transformers is pinned to 4.57.1 to keep the ESM integration consistent.
This is an inference environment, rather than the full upstream training/dashboard setup.
Version ranges make this a starter environment rather than a complete dependency lock.
