# Interpreting Protein Language Models with Biological Evidence

Exploratory notebooks examining pretrained ESM-2 representations and InterPLM sparse
autoencoder (SAE) features against UniProt protein sequences and annotations. The
current analysis uses ESM-2-8M layer 4, including features 5712 and 8893.

This project's contributions are the protein comparisons, analysis helpers, plots,
and preliminary evidence-assisted explanation exercise. The protein language model
and SAEs are pretrained resources from the authors credited below. Feature
interpretations remain exploratory associations. See [the project proposal](interpreting-PLMs.MD)
for the broader study and planned evaluation. Note the scope may change as the
project unfolds.

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

Notebook 01 records a manual comparison of LLM explanations with and without
supplied UniProt evidence; prompts are saved in
[`outputs/explanation_exercise/`](outputs/explanation_exercise/).
An automated retrieval/LLM pipeline is still planned. Model weights are downloaded
separately when first used.

The environment does not require CUDA. InterPLM defaults to CPU on macOS; an NVIDIA
GPU setup may need a PyTorch wheel matching the machine's CUDA configuration.
On macOS with an `x86_64` Python (Intel or Rosetta), the environment selects
PyTorch 2.2.2, the last release with macOS Intel wheels. Other platforms use 2.8.0.
NumPy is pinned to 1.26.4 to support PyTorch 2.2's tensor/NumPy conversions, and
Transformers is pinned to 4.57.1 to keep the ESM integration consistent.
This is an inference environment, rather than the full upstream training/dashboard setup.
Version ranges make this a starter environment rather than a complete dependency lock.

## References and acknowledgements

### Pretrained models and methods

- **InterPLM — SAE method, inference code, and pretrained SAE weights.** Simon, E.
  and Zou, J. (2025). *InterPLM: discovering interpretable features in protein
  language models via sparse autoencoders.* Nature Methods **22**, 2107–2117.
  [Published paper](https://doi.org/10.1038/s41592-025-02836-7),
  [code](https://github.com/ElanaPearl/InterPLM), and
  [SAE checkpoints](https://huggingface.co/Elana/InterPLM-esm2-8m).
  The notebooks also refer to the [2024 preprint](https://arxiv.org/abs/2412.12101);
  section numbers in those notes refer to that version. We use the pretrained
  `esm2-8m` layer-4 SAE, rather than training a new SAE.
- **ESM-2 — pretrained protein language model and residue embeddings.** Lin, Z.
  et al. (2023). *Evolutionary-scale prediction of atomic-level protein structure
  with a language model.* Science **379**, 1123–1130.
  [Paper](https://doi.org/10.1126/science.ade2574),
  [ESM code](https://github.com/facebookresearch/esm), and the exact
  [`facebook/esm2_t6_8M_UR50D` checkpoint](https://huggingface.co/facebook/esm2_t6_8M_UR50D).

### Protein data and biological evidence

- **UniProtKB — protein sequences, biological descriptions, membrane annotations,
  and their supporting evidence.** The UniProt Consortium (2025). *UniProt: the
  Universal Protein Knowledgebase in 2025.* Nucleic Acids Research **53**, D609–D617.
  [Paper](https://doi.org/10.1093/nar/gkae1010).
- **UniProt REST API — programmatic sequence and annotation retrieval.** Ahmad, S.
  et al. (2025). *The UniProt website API: facilitating programmatic access to
  protein knowledge.* Nucleic Acids Research **53**, W547–W553.
  [Paper](https://doi.org/10.1093/nar/gkaf394) and
  [API documentation](https://www.uniprot.org/api-documentation).

The introductory protein is [glycophorin A, P02724](https://www.uniprot.org/uniprotkb/P02724/entry).
Notebook 02 uses P06729, P02945, P26678, P50552, P00918, and P0DP23.
Notebook 04 adds P02786, P01732, P63027, P0AEN4, P06821, P29972, P08100,
P02920, P23895, P25874, P83755, and P32915, with individual entry links and
boundary-evidence references in that notebook.

The checked-in
[`feature_8893_uniprot_evidence.json`](data/reference/feature_8893_uniprot_evidence.json)
is an extract of UniProt records P06729, P26678, and P02945 retrieved on
**17 November 2026**. It preserves their sequences, entry/sequence versions, and
transmembrane feature objects; other entry fields and feature types were omitted.
Notebook 03 links the associated primary papers and PDB records. Notebook 04
records membrane boundaries, evidence codes, and entry versions checked on
**19 November 2026**. Earlier sequence downloads did not retain retrieval dates
or model-checkpoint revisions; live entries and checkpoints may change.

Biological claims should be read alongside the source entry's evidence:
[UniProt transmembrane documentation](https://www.uniprot.org/help/transmem),
[UniProt evidence documentation](https://www.uniprot.org/help/evidences), and
the [Evidence & Conclusion Ontology (ECO)](https://www.evidenceontology.org/).
The notebooks retain region-specific PubMed, PDB, and HAMAP references where
UniProt supplies them. These are annotation sources; the underlying experiments
have not been independently reassessed here.

### Images, learning resources, and software

[`uniprot-annotation.png`](uniprot-annotation.png) is a screenshot of the
[P02724 subcellular-location panel](https://www.uniprot.org/uniprotkb/P02724/entry#subcellular_location),
credited to UniProt. Its cell illustration is from **SwissBioPics**, Swiss-Prot
group, SIB Swiss Institute of Bioinformatics. SwissBioPics images are provided
under [CC BY 4.0](https://www.swissbiopics.org/help). Cite: Le Mercier, P. et al.
(2022). *SwissBioPics—an interactive library of cell images for the visualization
of subcellular location data.* Database **2022**, baac026.
[Paper](https://doi.org/10.1093/database/baac026).
The screenshot displays a citation to Gerber and Shai (2001),
[*In vivo detection of hetero-association of glycophorin-A and its mutants within
the membrane*](https://doi.org/10.1074/jbc.M101889200); it does not establish the
exact transmembrane boundaries used in the sequence plots.

Background explanations draw on the
[UniProtKB user manual](https://web.expasy.org/docs/userman.html),
[RCSB PDB membrane-protein resources](https://www.rcsb.org/docs/general-help/membrane-protein-resources),
and Alberts et al., *Molecular Biology of the Cell*, 4th edition (2002),
[“Membrane Proteins”](https://www.ncbi.nlm.nih.gov/books/NBK26878/).

The analysis also uses [PyTorch](https://pytorch.org/),
[Hugging Face Transformers](https://github.com/huggingface/transformers),
[NumPy](https://numpy.org/), [pandas](https://pandas.pydata.org/),
[Matplotlib](https://matplotlib.org/), [Requests](https://requests.readthedocs.io/),
and [Jupyter/IPython](https://jupyter.org/). The optional structure viewer is
[py3Dmol](https://pypi.org/project/py3Dmol/).
The full environment, including packages reserved for planned work, is listed in
[`environment.yml`](environment.yml). Notebook 01 records AI assistance and the
model label used for its manual explanation exercise; generated explanations are
experimental outputs, not biological evidence.

## License and third-party attribution

Original project code is available under the [MIT License](LICENSE).
Third-party software and pretrained weights retain their own licenses and notices;
the linked InterPLM code, InterPLM SAE model card, and ESM-2 model card identify
their licenses as MIT.

UniProt-derived sequences, annotation extracts, and annotation content reproduced
in notebooks and figures are credited to the UniProt Consortium under
[UniProt's CC BY 4.0 terms](https://www.uniprot.org/help/license)
([license text](https://creativecommons.org/licenses/by/4.0/)). Extracting fields,
summarising annotations, and overlaying them on activation plots are modifications
made by this project. The SwissBioPics illustration retains its separate source
credit above. These attributions accompany the relevant third-party material;
the project's MIT license does not replace its source terms.
