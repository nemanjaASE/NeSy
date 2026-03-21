# 🧪 Testing the Natural Language Processing Layer (NLP)

## 📋 Introduction

This report documents the testing and evaluation of the Natural Language Processing (NLP) layer, whose primary role is the automatic extraction of medical symptoms from unstructured text in English.

The core challenge of this layer is accurately **identifying symptoms** in complex sentences, **distinguishing confirmed** from **negated conditions**, and **normalizing extracted terms** to canonical English equivalents compatible with medical ontologies (SYMP/DOID).

The goal of testing is to identify the optimal combination of LLM architecture and system prompt configuration in order to achieve high precision and reliability before data is passed to the next layer — **the embedding (vectorization) layer**.

Testing was conducted across 5 phases, varying model size (from 3B to 120B parameters) and instruction complexity, with a focus on reaching an 80% success threshold across key metrics. The following models were evaluated:

- 🤖 **llama3.2:3b** (local)
- 🤖 **llama3.3:8** (local)
- 🤖 **qwen2.5:14b** (local)
- ☁️ **meta-llama/llama-4-scout-17b-16e-instruct** (cloud)
- ☁️ **openai/gpt-oss-120b** (cloud)

## 📐 Evaluation Methodology

Standard NLP metrics were used to assess extraction quality:

- **Precision** — the model's ability to extract only relevant and correct symptoms without introducing noise
- **Recall** — the model's ability to identify all symptoms mentioned in the text without omissions
- **F1 Score** — the harmonic mean of precision and recall, representing the overall accuracy of the model

## 🎯 Target Metrics

| Metric    | Success Threshold | Formula                                                        |
|-----------|-------------------|----------------------------------------------------------------|
| Precision | ✅ ≥ 80%          | TP / (TP + FP) — or 0 if no symptoms extracted                |
| Recall    | ✅ ≥ 80%          | TP / (TP + FN) — or 0 if no symptoms expected                 |
| F1 Score  | ✅ ≥ 80%          | 2 × (Precision × Recall) / (Precision + Recall) — or 0 if both are 0 |

## 🧪 Test 1

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | llama3.2:3b (local)                    |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-1.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.751 |
| Recall    | 0.729 |
| F1 Score  | 0.732 |

### 💬 Commentary

The `llama3.2:3b` model achieved an average `F1` score of `0.732`, demonstrating solid reliability in identifying core symptoms. While the model handles explicit negations (e.g., ***"no fever"***) correctly in most cases, negation errors were identified in **cases 021** and **041**, where the model incorrectly flagged present symptoms as negated.

The primary performance bottleneck remains terminological variance — the model tends to extract literal descriptions (e.g., ***"throat burn"***) instead of expected canonical medical terms (e.g., ***"pharynx inflammation"***). A post-processing mapping layer is recommended to align natural language outputs with formal ontologies.

## 🧪 Test 2

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | llama3:8b (local)                      |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-2.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.793 |
| Recall    | 0.787 |
| F1 Score  | 0.782 |

### 💬 Commentary

The `llama3:8b` model achieved an average `F1` score of `0.782`, showing improved overall extraction accuracy compared to the 3B version. Notably, this model handled negations perfectly across all **100 test cases** (Negation Error: False for all entries), successfully distinguishing between present and absent symptoms even in complex phrasing.

However, it still exhibits challenges with terminological mapping (e.g., extracting ***"hyperhidrosis"*** instead of ***"diaphoresis"***) and occasionally fails to capture symptoms in more nuanced inputs (e.g., **cases 083** and **088**). The results suggest that while the larger model is more robust in logic and negation handling, terminological alignment with formal ontologies remains an open challenge.

## 🧪 Test 3

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | qwen2.5:14b (local)                    |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-3.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.836 |
| Recall    | 0.825 |
| F1 Score  | 0.826 |

### 💬 Commentary

The `qwen2.5:14b` model demonstrated a high level of linguistic sophistication, achieving an average `F1` score of `0.826`. A defining characteristic of this model is its tendency toward autonomous clinical normalization — it frequently maps natural language descriptions to formal medical terminology (e.g., converting ***"runny nose"*** to `rhinorrhea` or ***"sore throat"*** to `pharyngitis`) even when not explicitly prompted.

While this resulted in lower scores in cases where the expected labels were more generic (e.g., **cases 013** and **033**), it highlights a superior understanding of medical context. Furthermore, the model maintained 100% accuracy in negation logic, successfully filtering out all symptoms the patient denied having.

These results indicate that `qwen2.5:14b` is highly effective for processing real-world patient narratives where complex phrasing and medical synonyms are common.

## 🧪 Test 4

| Field          | Value                                          |
|----------------|------------------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json           |
| Model          | meta-llama/llama-4-scout-17b-16e-instruct (cloud)     |
| System Prompt  | symptom-extraction-prompt-1.txt                |
| Results        | symptom-extraction-result-4.txt                |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.743 |
| Recall    | 0.801 |
| F1 Score  | 0.763 |

### 💬 Commentary

The `llama-4-scout-17b` model is a highly capable engine with a deep understanding of medical context, but its tendency toward hyper-specific clinical vocabulary and concept grouping makes it slightly less compatible with simpler, rigid ontologies.

The overall `F1` score of `0.763` is largely a reflection of terminology mismatch rather than poor comprehension — the model's output is often more clinically precise than the expected ground truth, suggesting that its extractions may in practice be more useful than the raw score implies.

## 🧪 Test 5

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | openai/gpt-oss-120b (cloud)            |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-5.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.711 |
| Recall    | 0.717 |
| F1 Score  | 0.708 |

### 💬 Commentary

The `gpt-oss-120b` model operates more like an experienced clinician than a raw data parser. Its ability to navigate medical context and negation is top-tier; however, its tendency toward generating complex, pre-coordinated clinical terms necessitates a robust post-processing layer or a "fuzzy" mapping strategy to fully align its output with rigid, atomic ontologies.

Notably, despite being the largest model tested (120B parameters), it achieved the lowest F1 score among all evaluated models — further reinforcing that raw model size is not the primary driver of performance in structured extraction tasks.

## 📊 Overall Results

| Model                                    | Size | Type  | Precision | Recall | F1    |
|------------------------------------------|------|-------|-----------|--------|-------|
| llama3.2:3b                              | 3B   | Local | 0.751     | 0.729  | 0.732 |
| llama3:8b                                | 8B   | Local | 0.793     | 0.787  | 0.782 |
| qwen2.5:14b                              | 14B  | Local | 0.836     | 0.825  | 0.826 |
| meta-llama/llama-4-scout-17b-16e-instruct| 17B  | Cloud | 0.743     | 0.801  | 0.763 |
| openai/gpt-oss-120b                      | 120B | Cloud | 0.711     | 0.717  | 0.708 |

> ✅ `qwen2.5:14b` achieved the highest F1 score across all tested models, surpassing the 80% target threshold and outperforming models up to 8x larger.
