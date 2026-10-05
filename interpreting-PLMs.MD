# Interpreting Protein Language Models with Biological Evidence: A Case Study of Membrane-Spanning Regions

**Status: Project proposal — implementation has not yet begun.**

## Project description

Protein language models learn patterns from amino-acid sequences, but understanding what their internal representations capture remains challenging. Sparse autoencoders offer a way to extract features from these representations, while retrieval-augmented generation (RAG) allows a language model to consult external sources when explaining them. This project will investigate **whether retrieving biological literature improves the accuracy and evidential support of explanations of protein-language-model features.**

The initial biological focus will be **transmembrane helices**: coiled stretches of a protein that pass through a cell membrane. These provide a relatively accessible starting point because their locations can be marked along a protein sequence and compared visually with feature activations. UniProt records these regions, although the supporting evidence must be checked because some annotations are computational predictions.

The project will explore the question:

> Do selected model features respond specifically to membrane-spanning regions, and does access to biological evidence help a language model interpret those responses correctly?

Using a small pretrained ESM-2 model and existing sparse autoencoders from InterPLM, the student will examine a handful of features across a small collection of well-annotated proteins. A feature's *activation* measures how strongly it responds at each position in a sequence. This will provide an introduction to representation analysis without requiring the student to train a protein language model or sparse autoencoder from scratch.

The student will build a simple RAG system to retrieve relevant passages from a curated collection of UniProt entries and selected primary papers. The same language model will then interpret feature activations both **with and without retrieved evidence**. Explanations will be assessed against a small, manually checked reference set for biological correctness, whether citations support the claims made, and whether uncertainty is acknowledged appropriately.

Separate proteins will be used for developing interpretations and evaluating them, with close homologues kept together when splitting the collection. The student will assess whether the proposed interpretations explain feature behaviour on held-out proteins, rather than merely reproduce annotations for the examples used to develop them. Agreement with annotations will be treated as evidence of association; establishing how a feature influences the model's computation will remain an optional extension.

## Initial scope

The student will aim to work with:

- Approximately **20–30 proteins**, including membrane proteins and comparison proteins.
- **One model layer and two or three candidate features**, selected through a preliminary exploration.
- A small document collection, with straightforward retrieval and cited explanations.
- Sequence plots showing feature activations alongside annotated membrane-spanning regions.
- A short comparative evaluation, including examples where retrieval helps, fails or introduces unsupported claims.

The first version will be an exploratory study intended to remain manageable for a student with a machine-learning background who is new to RAG, mechanistic interpretability and protein biology. A successful outcome will be a clear, reproducible assessment of the method, including its limitations; improvement from retrieval will be a question to test rather than an assumed result.

## Expected outputs

The student will produce a documented code repository, reproducible analysis notebooks or scripts, visualisations of selected feature activations, and a concise report comparing explanations generated with and without retrieval. The repository will acknowledge the pretrained models and tools used and identify the student's contribution as the retrieval pipeline, evaluation and analysis.

## Possible extensions

If time permits, the student may investigate whether features distinguish membrane-spanning regions from other hydrophobic—water-avoiding—protein regions, compare additional model layers, or separate the effects of retrieving UniProt annotations from those of retrieving primary literature. A more ambitious extension could test what happens to model predictions when selected features are suppressed, allowing the work to progress from interpreting associations towards examining how the model uses its representations.

## Starting resources

- [InterPLM paper](https://arxiv.org/abs/2412.12101)
- [InterPLM code and pretrained sparse autoencoders](https://github.com/ElanaPearl/InterPLM)
- [UniProt documentation: transmembrane regions](https://www.uniprot.org/help/transmem)
