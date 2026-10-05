# Interpreting Protein Language Models with Biological Evidence

See [the project proposal](interpreting-PLMs.MD) for the study's scope. Implementation has not yet begun.

## Environment setup

```bash
conda env create -f environment.yml
conda activate interpreting-plms
jupyter lab
```

The environment provides Python 3.11, ESM-2 and pretrained InterPLM SAE inference,
protein sequence handling, UniProt downloads, PDF extraction, BM25/TF-IDF retrieval,
analysis, and plotting. Its core requirements follow
[InterPLM's upstream dependencies](https://github.com/ElanaPearl/InterPLM/blob/5f4cbf90a0b3c1c031951ffd0b3b8e11b6f2ed61/requirements.txt).
InterPLM is pinned to a source commit and installed in editable mode to retain its
YAML model configurations; pip may create a local `src/interplm` checkout.

No LLM provider has been selected yet. Hugging Face Transformers supports local
models, and `requests` supports HTTP APIs; add a provider's SDK if the implementation
chooses one. Model weights are downloaded separately when first used.

The environment does not require CUDA. InterPLM defaults to CPU on macOS; an NVIDIA
GPU setup may need a PyTorch wheel matching the machine's CUDA configuration.
Version ranges make this a starter environment rather than a complete dependency lock.
