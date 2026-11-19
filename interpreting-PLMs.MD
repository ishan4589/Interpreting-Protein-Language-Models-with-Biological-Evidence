# Interpreting Protein Language Models with Biological Evidence: A Case Study of Membrane-Spanning Regions

**Status: Exploratory analysis in progress; automated retrieval and comparative evaluation are planned.**

## Project description

This project investigates **whether biological evidence improves the accuracy and support of explanations of protein-language-model features**. It uses pretrained ESM-2 representations and InterPLM sparse autoencoders (SAEs), with an initial focus on transmembrane helices: regions of a protein that cross a cell membrane.

The central question is:

> Do selected model features respond specifically to membrane-spanning regions, and does access to biological evidence help a language model interpret those responses correctly?

## Approach

- Examine SAE feature activations across membrane proteins and comparison proteins, and plot them alongside UniProt annotations.
- Develop hypotheses about what features respond to, including amino-acid identity, membrane regions and sequence context.
- Build a retrieval-augmented generation (RAG) pipeline using relevant passages from UniProt entries and primary papers.
- Compare explanations from the same language model **with and without retrieved evidence**.

Protein and feature selection will follow the hypotheses being tested. UniProt annotations will retain their evidence codes and source references, since some membrane boundaries are predicted or inferred.

## Evaluation

Assess explanations against manually checked biological evidence for correctness, citation support and appropriate uncertainty. Include cases where retrieval helps, fails or introduces unsupported claims.

Use separate proteins to develop and evaluate interpretations, keeping close homologues in the same split. Test whether hypotheses explain feature responses on held-out proteins. Agreement with annotations supports an association; it does not establish a feature's causal role in the model.

The aim is a reproducible assessment of the method and its limitations. Improvement from retrieval is a question to test.

## Expected outputs

- Reproducible notebooks, analysis helpers and feature-activation plots.
- A retrieval pipeline with source provenance and cited explanations.
- A comparative evaluation of explanations with and without retrieval.

The project's contributions are the analysis, retrieval pipeline and evaluation, building on credited pretrained models, tools and data sources.

## Possible extensions

Compare membrane-spanning regions with other hydrophobic regions, examine additional model layers, or compare retrieval from UniProt with retrieval from primary literature. Feature suppression experiments could test how selected features influence model predictions.

## Starting resources

- [InterPLM paper](https://doi.org/10.1038/s41592-025-02836-7)
- [InterPLM code and pretrained sparse autoencoders](https://github.com/ElanaPearl/InterPLM)
- [UniProt documentation: transmembrane regions](https://www.uniprot.org/help/transmem)
