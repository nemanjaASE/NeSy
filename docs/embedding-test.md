---
title: 🧪 Testing the Embedding Layer
nav_order: 7
---

# 🧪 Testing the Embedding Layer

## 📋 Overview

This section documents the evaluation of the embedding layer used in the **NeSy-X framework**. The embedding layer is responsible for generating vector representations of symptoms, which are then used for semantic mapping (cosine similarity) against symptom concepts stored in the knowledge graph.

The evaluation focuses on three types of symptom inputs::

- Canonical ontology terms (exact match)
- Synonyms and variations
- Descriptive and colloquial expressions

The goal of the test is to determine which `embedding model` provides the most reliable semantic mapping before the mapped symptoms are forwarded to the symbolic reasoning, scoring, and explanation layers.

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
Percentage of mappings with cosine similarity greater than or equal to 0.90.. This value includes both exact matches and semantically close mappings.

```
(total_usable / total_symptoms) × 100
```

**🔴 Bad Match Rate**
Percentage of cases where symptoms are mapped with confidence < 0.90. These mappings are treated as unreliable and are not forwarded to the symbolic layer.

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
A general-purpose sentence-transformers model used as a lightweight baseline for semantic similarity. It produces 384-dimensional embeddings and is suitable for fast sentence-level similarity, clustering, and semantic search tasks. Since it is not specifically optimized for medical terminology or ontology alignment, it was used to test how far a compact general model can go in this task.
- **Embedding size:** 384
- **Use case:** General semantic similarity, fast inference
- **HuggingFace:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

### `NeuML/pubmedbert-base-embeddings`
A biomedical embedding model based on the PubMedBERT/BiomedBERT family. It produces 768-dimensional embeddings and is intended for biomedical and scientific text. In this evaluation, it was used to test whether domain-oriented biomedical language modeling improves symptom-to-ontology mapping.
- **Embedding size:** 768
- **Use case:** Biomedical text, clinical terminology, scientific abstracts
- **HuggingFace:** [NeuML/pubmedbert-base-embeddings](https://huggingface.co/NeuML/pubmedbert-base-embeddings)

### `intfloat/multilingual-e5-large`
A large multilingual embedding model from the E5 family. It produces 1024-dimensional embeddings and is designed for multilingual semantic retrieval. Its training setup makes it suitable for mapping semantically related expressions even when their surface forms differ, which is important for connecting informal symptom descriptions to standardized ontology terms.
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

The model performs well on exact ontology labels, where all mappings reach a similarity score of 1.000. However, performance drops substantially for synonyms and colloquial expressions. EXACT entries hit a perfect 1.0 — expected, since those are verbatim ontology terms. LLM entries average 0.879, which is acceptable but with a meaningful tail of failures: 38 out of 119 fall below 0.85, and some are genuinely poor matches — `lacrimation` mapping to `decreased milk production` (0.502), `presyncope` to `precordial pain` (0.399), `tingling` to `shock` (0.537), and `pruritus` to `prostatic infection` (0.535) — suggesting the model has weak coverage of clinical terminology and is essentially guessing by surface form similarity when it doesn't recognize a medical term.

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

The biomedical model achieves a slightly higher overall average similarity than the general MiniLM model, but this improvement is not reflected in the usability of the mappings. While EXACT entries hit a perfect 1.0, the SYN group drops to 0.746 — lower than MiniLM's 0.758 on the same inputs — and produces genuinely nonsensical mappings like *"heart racing"* → *"wheelbarrowing"* (0.468) and *"hard to breathe"* → *"boil"* (0.559). These aren't near-misses — they're random-looking picks that suggest the model completely loses its footing on short informal phrases outside clinical prose context.

The LLM group at 0.894 is acceptable but still has 38 entries below 0.85, with recurring issues around morphological near-misses (`hiccup`/`hiccough`, `erythema`/`rash`) and directional specificity failures. The domain pretraining on PubMed abstracts clearly helps with well-formed clinical terminology but doesn't generalize to ontology alignment or lay-language input — if anything it seems to overfit to a narrow register of biomedical writing, making it brittle on anything that doesn't resemble an abstract. The model is therefore useful as a biomedical comparison point, but it does not provide the robustness required for the semantic mapping layer in NeSy-X.

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

`intfloat/multilingual-e5-large` clearly outperforms the other two models.. Overall average hits 0.978, the LLM group sits at 0.970, and even the SYN group — the hardest set with informal lay-language descriptions — reaches 0.934 with **zero entries falling below 0.85**. That's a dramatic improvement over both MiniLM (SYN: 0.758) and pubmedbert (SYN: 0.746) on the same inputs.

The model handles clinical terminology, ontology-style labels, and colloquial patient phrasing uniformly well, which is exactly what a production symptom mapping pipeline needs. The likely reason is that E5-large was trained with explicit instruction-tuned contrastive objectives across a much broader range of text types, making it robust to register variation in a way that domain-specific pretraining alone doesn't achieve. The results indicate that the E5 model is better suited to this task because it handles both formal ontology-style labels and more variable natural-language symptom expressions.

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

The evaluation shows that `intfloat/multilingual-e5-large` provides the most reliable semantic mapping between extracted symptom expressions and ontology symptoms. It significantly reduces the number of unusable mappings and performs especially well on synonyms, descriptive expressions, and LLM-generated symptom outputs. It is the recommended model for the production embedding layer, to be used as the default for all subsequent testing phases and downstream inference layers.

For the NeSy-X framework, this model is the most appropriate choice because the embedding layer acts as the bridge between the neural NLP component and the symbolic graph-based reasoning component. Reliable semantic mapping ensures that only sufficiently confident ontology matches are forwarded to the disease ranking, negation filtering, and XAI layers.
