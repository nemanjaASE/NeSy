---
title: 🧪 Testing the Embedding Layer
nav_order: 7
---

# 🧪 Testing the Embedding Layer

## 📋 Overview

This report documents the testing and evaluation process of the **Embedding Layer**. The embedding layer is responsible for generating vector representations of symptoms, which are then used for semantic mapping (cosine similarity) against a symptom ontology stored in a **Neo4j** database.

The core challenge of this layer is achieving high semantic precision across:

- Canonical ontology terms (exact match)
- Synonyms and variations
- Descriptive and colloquial expressions

The goal of the testing is to identify the optimal `sentence-transformers` model and achieve high precision before results are forwarded to the next layer for inference and scoring.

Testing was conducted in three phases using different models for vector representation.

---

## 📐 Evaluation Methodology

The following metrics and approaches were used to assess the quality of the Embedding Layer, adapted for semantic symptom mapping:

**🔵 Semantic Similarity** *(Confidence Score)*
Cosine similarity between the vector representation of the user's symptom and the vector representation of the ontology symptom.

```
cosine_similarity(embedding_input, embedding_ontology) ∈ [0, 1]
```

**🟢 Exact Match Rate**
Percentage of cases where the best-mapped symptom is identical to the input symptom.

```
(total_exact / total_symptoms) × 100
```

**🟡 Usable Match Rate**
Percentage of cases where symptoms are mapped with confidence ≥ 0.90. This value includes both exact matches and semantically close mappings.

```
(total_usable / total_symptoms) × 100
```

**🔴 Bad Match Rate**
Percentage of cases where symptoms are mapped with confidence < 0.90. These mappings are considered unusable and are discarded from further processing.

```
(total_bad / total_symptoms) × 100
```

---

## 🗂️ Test Set

The test set (`symptom-full-test.json`) consists of **369 symptoms** divided into three groups:

| ID Prefix | Count | Description |
|-----------|-------|-------------|
| `EXACT` | 180 | Canonical terms from the ontology (verbatim) |
| `SYN` | 70 | Synonyms, descriptive and colloquial expressions |
| `LLM` | 119 | Symptoms extracted during NLP layer testing |

---

## 🤖 Models Tested

### `all-MiniLM-L6-v2`
A lightweight, general-purpose sentence transformer model developed by Microsoft and fine-tuned by the Sentence-Transformers team. It produces 384-dimensional embeddings and is optimized for speed and efficiency. It has no domain-specific medical training, making it a general baseline.
- **Embedding size:** 384
- **Use case:** General semantic similarity, fast inference
- **HuggingFace:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

### `NeuML/pubmedbert-base-embeddings`
A BERT-based model pre-trained on PubMed abstracts and biomedical literature, fine-tuned by NeuML for producing semantic embeddings in the biomedical domain. It produces 768-dimensional embeddings and is specifically designed for clinical and scientific text.
- **Embedding size:** 768
- **Use case:** Biomedical text, clinical terminology, scientific abstracts
- **HuggingFace:** [NeuML/pubmedbert-base-embeddings](https://huggingface.co/NeuML/pubmedbert-base-embeddings)

### `intfloat/multilingual-e5-large`
A large multilingual embedding model from the E5 family (EmbEddings from bidirEctional Encoder rEpresentations), trained with instruction-tuned contrastive objectives across a wide range of text types and languages. It produces 1024-dimensional embeddings and is robust to register variation — handling formal clinical terms and informal patient language equally well.
- **Embedding size:** 1024
- **Use case:** Multilingual semantic search, mixed-register text, ontology alignment
- **HuggingFace:** [intfloat/multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)

---

## 🧪 Test 1 — General Model

**Test set:** `symptom-full-test.json`
**Model:** `all-MiniLM-L6-v2`
**Results:** `embedding-test-1.json`

| Metric | EXACT | SYN | LLM | Average |
|--------|-------|-----|-----|---------|
| ✅ Exact Match Rate | 100.0% | 17.1% | 57.1% | 70.5% |
| 🟡 Usable Match Rate | 100.0% | 22.9% | 61.3% | 72.9% |
| 📊 Average Confidence | 1.000 | 0.758 | 0.879 | 0.915 |
| ❌ Bad Match Rate | 0.0% | 77.1% | 38.7% | 27.1% |

The `all-MiniLM-L6-v2` model performs well overall with an average confidence of 0.915 across 369 mappings, but the results break down sharply by input type. EXACT entries hit a perfect 1.0 — expected, since those are verbatim ontology terms. LLM entries average 0.879, which is acceptable but with a meaningful tail of failures: 38 out of 119 fall below 0.85, and some are genuinely poor matches — `lacrimation` mapping to `decreased milk production` (0.502), `presyncope` to `precordial pain` (0.399), `tingling` to `shock` (0.537), and `pruritus` to `prostatic infection` (0.535) — suggesting the model has weak coverage of clinical terminology and is essentially guessing by surface form similarity when it doesn't recognize a medical term.

The SYN group is the real problem, averaging only 0.758, with 50 of 70 entries below 0.85. This is expected given that SYN inputs are informal lay-language descriptions — *"gurgling noises in belly"*, *"weird spit"*, *"short of breath when walking"* — and a general-purpose sentence model trained without medical context struggles to bridge colloquial phrasing to ontology labels.

Overall, `all-MiniLM-L6-v2` is a reasonable baseline for exact or near-exact term matching, but it's not suited for production use in a medical NLP pipeline where robustness to synonymy and lay language is required.

---

## 🧪 Test 2 — Medical Domain Model

**Test set:** `symptom-full-test.json`
**Model:** `NeuML/pubmedbert-base-embeddings`
**Results:** `embedding-test-2.json`

| Metric | EXACT | SYN | LLM | Average |
|--------|-------|-----|-----|---------|
| ✅ Exact Match Rate | 100.0% | 17.1% | 57.1% | 70.5% |
| 🟡 Usable Match Rate | 100.0% | 21.4% | 60.5% | 72.4% |
| 📊 Average Confidence | 1.000 | 0.746 | 0.893 | 0.917 |
| ❌ Bad Match Rate | 0.0% | 78.6% | 39.5% | 27.6% |

The model lands at an overall average confidence of 0.918, which on paper looks comparable to MiniLM, but the failure profile is considerably worse. While EXACT entries hit a perfect 1.0, the SYN group drops to 0.746 — lower than MiniLM's 0.758 on the same inputs — and produces genuinely nonsensical mappings like *"heart racing"* → *"wheelbarrowing"* (0.468) and *"hard to breathe"* → *"boil"* (0.559). These aren't near-misses — they're random-looking picks that suggest the model completely loses its footing on short informal phrases outside clinical prose context.

The LLM group at 0.894 is acceptable but still has 38 entries below 0.85, with recurring issues around morphological near-misses (`hiccup`/`hiccough`, `erythema`/`rash`) and directional specificity failures. The domain pretraining on PubMed abstracts clearly helps with well-formed clinical terminology but doesn't generalize to ontology alignment or lay-language input — if anything it seems to overfit to a narrow register of biomedical writing, making it brittle on anything that doesn't resemble an abstract. For this use case it's the weakest of the three models tested.

---

## 🧪 Test 3 — Multilingual Large Model

**Test set:** `symptom-full-test.json`
**Model:** `intfloat/multilingual-e5-large`
**Results:** `embedding-test-3.json`

| Metric | EXACT | SYN | LLM | Average |
|--------|-------|-----|-----|---------|
| ✅ Exact Match Rate | 100.0% | 17.1% | 57.1% | 70.5% |
| 🟡 Usable Match Rate | 100.0% | 80.0% | 93.3% | 94.0% |
| 📊 Average Confidence | 1.000 | 0.934 | 0.969 | 0.977 |
| ❌ Bad Match Rate | 0.0% | 20.0% | 6.7% | 6.0% |

`multilingual-e5-large` is the clear winner. Overall average hits 0.978, the LLM group sits at 0.970, and even the SYN group — the hardest set with informal lay-language descriptions — reaches 0.934 with **zero entries falling below 0.85**. That's a dramatic improvement over both MiniLM (SYN: 0.758) and pubmedbert (SYN: 0.746) on the same inputs.

The model handles clinical terminology, ontology-style labels, and colloquial patient phrasing uniformly well, which is exactly what a production symptom mapping pipeline needs. The likely reason is that E5-large was trained with explicit instruction-tuned contrastive objectives across a much broader range of text types, making it robust to register variation in a way that domain-specific pretraining alone doesn't achieve. For this use case it's the obvious choice.

---

## 📊 Model Comparison Summary

| Model | EXACT | SYN | LLM | Avg Confidence | Bad Match Rate |
|-------|-------|-----|-----|----------------|----------------|
| `all-MiniLM-L6-v2` | 1.000 | 0.758 | 0.879 | 0.915 | 27.1% |
| `NeuML/pubmedbert-base-embeddings` | 1.000 | 0.746 | 0.893 | 0.917 | 27.6% |
| `intfloat/multilingual-e5-large` | **1.000** | **0.934** | **0.969** | **0.977** | **6.0%** |

---

## ✅ Conclusion

**Selected model: `intfloat/multilingual-e5-large`**

The `multilingual-e5-large` model significantly outperforms both alternatives across all non-trivial input groups, with a usable match rate of 94.0% overall and 80.0% even on the most challenging informal SYN expressions. It is the recommended model for the production embedding layer, to be used as the default for all subsequent testing phases and downstream inference layers.
