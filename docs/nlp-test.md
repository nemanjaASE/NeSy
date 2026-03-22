# 🧪 Testing the Natural Language Processing Layer (NLP)

## 📋 Introduction

This report documents the testing and evaluation of the Natural Language Processing (NLP) layer, whose primary role is the automatic extraction of medical symptoms from unstructured text in English.

The core challenge of this layer is accurately **identifying symptoms** in complex sentences, **distinguishing confirmed** from **negated conditions**, and **normalizing extracted terms** to canonical English equivalents compatible with medical ontologies (SYMP/DOID).

The goal of testing is to identify the optimal combination of LLM architecture and system prompt configuration in order to achieve high precision and reliability before data is passed to the next layer — **the embedding (vectorization) layer**.

Testing was conducted across 7 phases, varying model size (from 3B to 120B parameters) and instruction complexity, with a focus on reaching an 80% success threshold across key metrics. The following models were evaluated:

- 🤖 **llama3.2:3b** (local)
- 🤖 **llama3.3:8** (local)
- 🤖 **mistral-nemo:12b** (local)
- 🤖 **qwen2.5:14b** (local)
- 🤖 **phi4:14b** (local)
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
| Precision | 0.747 |
| Recall    | 0.730 |
| F1 Score  | 0.731 |

### 💬 Commentary

The `llama3.2:3B` model offers surprisingly robust baseline extraction capabilities for its size, characterized by a balanced precision-recall profile. However, its utility in strict ontology-based systems is limited by its tendency to generate pre-coordinated, hyper-specific clinical phrases (e.g., ***chest pain on inhalation***) and its occasional, yet significant, failures in accurately resolving logical negations (**case 10** and **41**) within complex clinical narratives.

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
| Precision | 0.809 |
| Recall    | 0.806 |
| F1 Score  | 0.800 |

### 💬 Commentary

The `llama3:8B` model achieved a solid `80% F1-score` across the `100 test cases`. While it excels at identifying standard symptoms like ***fever*** and ***headache***, it struggles with semantic mapping—often extracting a clinically accurate term (e.g., ***paresthesia***) that doesn't perfectly match the expected "gold standard" label (e.g., ***hypoesthesia***), or failing to split compound descriptions into separate entities. Despite these mapping nuances, the **zero negation errors** indicate high reliability in distinguishing between present and absent symptoms.

## 🧪 Test 3

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | mistral-nemo:12b (local)                    |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-3.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.784 |
| Recall    | 0.810 |
| F1 Score  | 0.790 |

### 💬 Commentary

The `mistral-nemo:12b` model achieved a nearly identical `79% F1-score`, showing slightly better recall than `llama3:8b` but frequently losing points due to overly technical synonym mapping (e.g., ***presyncope*** for ***lightheadedness***) and a tendency to combine separate symptoms into single compound entities.

## 🧪 Test 4

| Field          | Value                                          |
|----------------|------------------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json           |
| Model          | qwen2.5:14b (local)                            |
| System Prompt  | symptom-extraction-prompt-1.txt                |
| Results        | symptom-extraction-result-4.txt                |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.835 |
| Recall    | 0.825 |
| F1 Score  | 0.825 |

### 💬 Commentary

The `qwen2.5:14b` model is the current top performer with a `0.825 F1-score`, showing a superior ability to map descriptive symptoms into formal clinical terminology while maintaining perfect accuracy in negation handling, though it still occasionally penalizes itself by grouping separate symptoms into single compound terms.

## 🧪 Test 5

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | phi4:14b (local)                       |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-5.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.771 |
| Recall    | 0.783 |
| F1 Score  | 0.772 |

### 💬 Commentary

The `phi4:14B model` demonstrates high clinical intelligence with an `F1-score of 0.772`, though it frequently loses points by using advanced medical terminology (e.g., ***presyncope*** instead of ***faint***) that causes mismatches with your dataset's expected labels. While it excels at handling negations and complex symptoms, its primary challenge is over-specification, as it often provides more detailed anatomical descriptions than your ground truth requires.

## 🧪 Test 6

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | meta-llama/llama-4-scout-17b-16e-instruct (cloud) |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-6.txt        |

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.746 |
| Recall    | 0.799 |
| F1 Score  | 0.763 |

### 💬 Commentary

The `llama-4-scout-17b` model shows a solid baseline for symptom extraction with an average `F1-score of 0.763`, but it frequently encounters "False Positives" due to its high clinical precision. Much like the previous model, it tends to extract more detailed or technical terms (e.g., ***presyncope*** or ***hyperhidrosis***) when the ground truth expects simpler descriptions (e.g., ***lightheadedness*** or ***diaphoresis***). While its negation detection is nearly perfect, the overall score is primarily capped by this semantic gap between the model's medical vocabulary and your dataset's specific labels.

## 📊 Overall Results

| Model                                    | Size | Type  | Precision | Recall | F1    |
|------------------------------------------|------|-------|-----------|--------|-------|
| llama3.2:3b                              | 3B   | Local | 0.747     | 0.730  | 0.731 |
| llama3:8b                                | 8B   | Local | 0.809     | 0.806  | 0.800 |
| mistral-nemo:12b                         | 12B  | Local | 0.784     | 0.810  | 0.790 |
| qwen2.5:14b                              | 14B  | Local | 0.835     | 0.825  | 0.825 |
| phi4:14b                                 | 14B  | Local | 0.771     | 0.783  | 0.772 |
| meta-llama/llama-4-scout-17b-16e-instruct| 17B  | Cloud | 0.746     | 0.799  | 0.763 |
| openai/gpt-oss-120b                      | 120B | Cloud | 0.0     | 0.0  | 0.0 |

> ✅ `qwen2.5:14b` achieved the highest F1 score across all tested models, surpassing the 80% target threshold and outperforming models up to 8x larger.

## 🔍 Conclusion

While the NLP layer achieved satisfactory performance (F1 ≥ 0.80 for the best model), several challenges remain that directly impact the embedding layer.

The most critical issue is the lack of **strict canonical normalization**, which leads to **semantic fragmentation**. Different lexical representations of the same clinical concept (e.g., *"lightheadedness"*, *"dizziness"*, *"presyncope"*) result in distinct vector embeddings, reducing similarity accuracy and negatively affecting downstream disease matching.

Therefore, the effectiveness of the embedding layer is not solely dependent on the embedding model itself, but is heavily constrained by the **consistency and standardization of the NLP output**.
