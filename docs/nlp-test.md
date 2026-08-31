---
title: 🧪 Testing the Natural Language Processing Layer
nav_order: 7
---

# 🧪 Testing the Natural Language Processing Layer

## 📋 Introduction

This section documents the evaluation of the natural language processing layer used in the NeSy-X framework. The role of this layer is to extract symptoms from unstructured English text and organize them into two structured lists: present symptoms and absent symptoms.

The main challenge is strict symptom extraction. The model must identify relevant medical symptoms, preserve negation, avoid adding symptoms that are not explicitly mentioned, and avoid grouping separate symptoms into broader disease-like or syndrome-like expressions.

The goal of testing is to identify which LLM provides the most reliable structured symptom extraction before the results are passed to the embedding layer and then to the symbolic graph-based reasoning layer.

Seven large language models were evaluated under the same prompt and test conditions, including five locally executed models and two cloud-based models. The following models were evaluated:

- 🤖 **llama3.2:3b** (local)
- 🤖 **llama3.3:8** (local)
- 🤖 **mistral-nemo:12b** (local)
- 🤖 **qwen2.5:14b** (local)
- 🤖 **phi4:14b** (local)
- ☁️ **meta-llama/llama-4-scout-17b-16e-instruct** (cloud)
- ☁️ **openai/gpt-oss-120b** (cloud)

## 📐 Evaluation Methodology

The evaluation was performed on a test set of 100 English input examples. For each model, the extracted symptoms were compared with the manually defined expected symptoms:

- **Precision** — measures how many extracted symptoms are correct.
- **Recall** — measures how many expected symptoms were successfully extracted.
- **F1 Score** — F1 Score — the harmonic mean of precision and recall.

> The reported values are macro-averages: metrics were calculated for each test case and then averaged across the complete test set.

## 🎯 Target Metrics

| Metric    | Success Threshold | Formula                                                        |
|-----------|-------------------|----------------------------------------------------------------|
| Precision | ✅ ≥ 80%          | TP / (TP + FP) — or 0 if no symptoms extracted                |
| Recall    | ✅ ≥ 80%          | TP / (TP + FN) — or 0 if no symptoms expected                 |
| F1 Score  | ✅ ≥ 80%          | 2 × (Precision × Recall) / (Precision + Recall) — or 0 if both are 0 |

### ⚙️ Test Environment

| Property   | Value                                               |
|------------|-----------------------------------------------------|
| OS         | Windows-11-10.0.26200-SP0                           |
| CPU        | AMD64 Family 23 Model 113 Stepping 0, AuthenticAMD  |
| RAM        | 17.1 GB                                             |
| GPU        | NVIDIA GeForce RTX 3060                             |
| VRAM       | 12.0 GB                                             |
| Python     | 3.12.9                                              |
| Test Cases | 100                                                 |

## 🧪 Test 1

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | llama3.2:3b (local)                    |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-1.txt        |

### 🔍 Model Overview — `llama3.2:3b`

| Property         | Value                          |
|------------------|--------------------------------|
| Developer        | Meta                           |
| Released         | September 2024                 |
| Architecture     | Dense · Decoder-only Transformer |
| Parameters       | 3.21B                          |
| Attention        | GQA + RoPE                     |
| Context Window   | 128K tokens                    |
| Quantization     | Q4_K_M (Ollama)                |
| Intended Use     | On-device / edge deployment    |
| License          | Llama 3.2 Community License    |

> Lightweight text-only model optimized for mobile and edge environments. Supports 8 languages. Smallest model in the Llama 3.2 family.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.747 |
| Recall    | 0.730 |
| F1 Score  | 0.731 |

### ⏱️ Performance

| Metric        | Value   |
|---------------|---------|
| Total Time    | 39.14s  |
| Avg/Case      | 0.39s   |

### 💬 Commentary

The `llama3.2:3B` model offers surprisingly robust baseline extraction capabilities for its size, characterized by a balanced precision-recall profile. However, its utility in strict ontology-based systems is limited by its tendency to generate pre-coordinated, hyper-specific clinical phrases (e.g., `chest pain on inhalation`) and its occasional, yet significant, failures in accurately resolving logical negations (**case 10** and **41**) within complex clinical narratives.

## 🧪 Test 2

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | llama3:8b (local)                      |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-2.txt        |

### 🔍 Model Overview — `llama3:8b`

| Property         | Value                          |
|------------------|--------------------------------|
| Developer        | Meta                           |
| Released         | April 2024                     |
| Architecture     | Dense · Decoder-only Transformer |
| Parameters       | 8.03B                          |
| Attention        | GQA + RoPE                     |
| Layers           | 32                             |
| Hidden Dim       | 4096                           |
| Context Window   | 8K tokens                      |
| Quantization     | Q4_0 (Ollama)                  |
| License          | Meta Llama 3 Community License |

> First generation of the Llama 3 family. Trained on 15T tokens. Strong reasoning and instruction following for its size class.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.809 |
| Recall    | 0.806 |
| F1 Score  | 0.800 |

### ⏱️ Performance

| Metric        | Value   |
|---------------|---------|
| Total Time    | 57.39s  |
| Avg/Case      | 0.57s   |

### 💬 Commentary

The `llama3:8B` model achieved a solid **80% F1-score** across the **100 test cases**. While it excels at identifying standard symptoms like `fever` and `headache`, it struggles with semantic mapping—often extracting a clinically accurate term (e.g., `paresthesia`) that doesn't perfectly match the expected "gold standard" label (e.g., `hypoesthesia`), or failing to split compound descriptions into separate entities. Despite these mapping nuances, the **zero negation errors** indicate high reliability in distinguishing between present and absent symptoms.

## 🧪 Test 3

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | mistral-nemo:12b (local)               |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-3.txt        |

### 🔍 Model Overview — `mistral-nemo:12b`

| Property         | Value                                  |
|------------------|----------------------------------------|
| Developer        | Mistral AI + NVIDIA (joint)            |
| Released         | July 2024                              |
| Architecture     | Dense · Decoder-only Transformer       |
| Parameters       | 12.2B                                  |
| Layers           | 40                                     |
| Attention        | GQA (32 heads / 8 KV heads)            |
| Context Window   | 128K tokens                            |
| Tokenizer        | Tekken (Tiktoken-based, 131K vocab)    |
| Quantization     | FP8-aware training                     |
| Training Infra   | NVIDIA Megatron-LM, 3072× H100 GPUs   |
| License          | Apache 2.0                             |

> Co-developed with NVIDIA on DGX Cloud. Drop-in replacement for Mistral 7B with significantly expanded context and multilingual capability across 11+ languages.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.784 |
| Recall    | 0.810 |
| F1 Score  | 0.790 |

### ⏱️ Performance

| Metric        | Value   |
|---------------|---------|
| Total Time    | 78.96s  |
| Avg/Case      | 0.79s   |

### 💬 Commentary

The `mistral-nemo:12b` model achieved a nearly identical **79% F1-score**, showing slightly better recall than `llama3:8b` but frequently losing points due to overly technical synonym mapping (e.g., `presyncope` for `lightheadedness`) and a tendency to combine separate symptoms into single compound entities.

## 🧪 Test 4

| Field          | Value                                          |
|----------------|------------------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json           |
| Model          | qwen2.5:14b (local)                            |
| System Prompt  | symptom-extraction-prompt-1.txt                |
| Results        | symptom-extraction-result-4.txt                |

### 🔍 Model Overview — `qwen2.5:14b`

| Property         | Value                                      |
|------------------|--------------------------------------------|
| Developer        | Alibaba Cloud (Qwen Team)                  |
| Released         | September 2024                             |
| Architecture     | Dense · Decoder-only Transformer           |
| Parameters       | 14.7B total / 13.1B non-embedding          |
| Layers           | 48                                         |
| Attention        | GQA (40 Q heads / 8 KV heads) + RoPE      |
| Activation       | SwiGLU                                     |
| Normalization    | RMSNorm                                    |
| Context Window   | 128K tokens (generates up to 8K)          |
| Pretraining Data | ~18 trillion tokens                        |
| Multilingual     | 29+ languages                              |
| License          | Qwen Research License                      |

> Dense open-weight model from the Qwen2.5 family. Pretrained on the largest dataset among local models tested (~18T tokens). Strong structured output and instruction-following capabilities.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.835 |
| Recall    | 0.825 |
| F1 Score  | 0.825 |

### ⏱️ Performance

| Metric        | Value   |
|---------------|---------|
| Total Time    | 95.29s  |
| Avg/Case      | 0.95s   |

### 💬 Commentary

The best result was achieved by qwen2.5:14b, with an F1 score of 0.825. This model also achieved the highest precision, which is especially important in the NeSy-X framework because false positive symptoms can be mapped to ontology nodes and then influence downstream disease ranking.

## 🧪 Test 5

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | phi4:14b (local)                       |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-5.txt        |

### 🔍 Model Overview — `phi4:14b`

| Property         | Value                                      |
|------------------|--------------------------------------------|
| Developer        | Microsoft Research                         |
| Released         | December 2024                              |
| Architecture     | Dense · Decoder-only Transformer           |
| Parameters       | 14B                                        |
| Layers           | 40                                         |
| Attention        | GQA (24 heads / 8 KV heads) + RoPE        |
| Context Window   | 16K tokens (extendable to 64K)            |
| Tokenizer        | tiktoken (vocab size 100,352)              |
| Pretraining Data | ~9.8T tokens (incl. ~400B synthetic)      |
| Knowledge Cutoff | June 2024                                  |
| License          | MIT                                        |

> STEM-focused SLM (Small Language Model) from Microsoft. Distinguished by heavy use of **synthetic training data** for mathematical and scientific reasoning. Punches above its weight class on GPQA and MATH benchmarks.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.771 |
| Recall    | 0.783 |
| F1 Score  | 0.772 |

### ⏱️ Performance

| Metric        |  Value   |
|---------------|----------|
| Total Time    | 115.82s  |
| Avg/Case      |  1.16s   |

### 💬 Commentary

The `phi4:14B model` demonstrates high clinical intelligence with an **F1-score of 0.772**, though it frequently loses points by using advanced medical terminology (e.g., `presyncope` instead of `faint`) that causes mismatches with your dataset's expected labels. While it excels at handling negations and complex symptoms, its primary challenge is over-specification, as it often provides more detailed anatomical descriptions than your ground truth requires.

## 🧪 Test 6

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | meta-llama/llama-4-scout-17b-16e-instruct (cloud) |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-6.txt        |

### 🔍 Model Overview — `meta-llama/llama-4-scout-17b-16e-instruct`

| Property           | Value                                              |
|--------------------|----------------------------------------------------|
| Developer          | Meta                                               |
| Released           | April 2025                                         |
| Architecture       | **Mixture-of-Experts (MoE)** · Auto-regressive     |
| Active Parameters  | 17B (Top-2 routing per token)                      |
| Total Parameters   | 109B (distributed across experts)                  |
| MoE Experts        | 16 specialized + 1 shared (always active)          |
| Transformer Layers | 40 total (20 MoE blocks)                           |
| Activation         | SwiGLU                                             |
| Multimodality      | ✅ Early fusion (up to 5 images per prompt)        |
| Context Window     | 128K tokens (cloud)                                |
| Knowledge Cutoff   | August 2024                                        |
| Multilingual       | 12 languages                                       |
| License            | Llama 4 Community License                          |

> First MoE model in the Llama family. Each token activates only 2 of 16 experts, giving the inference cost of a 17B dense model with the knowledge capacity of 109B parameters. Natively multimodal via early fusion architecture.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.749 |
| Recall    | 0.806 |
| F1 Score  | 0.769 |

### ⏱️ Performance

| Metric        |  Value   |
|---------------|----------|
| Total Time    | 206.58s  |
| Avg/Case      |  2.07s   |

### 💬 Commentary

The `llama-4-scout-17b` model shows a solid baseline for symptom extraction with an average **F1-score of 0.769**, but it frequently encounters "False Positives" due to its high clinical precision. Much like the previous model, it tends to extract more detailed or technical terms (e.g., `presyncope` or `hyperhidrosis`) when the ground truth expects simpler descriptions (e.g., `lightheadedness` or `diaphoresis`). While its negation detection is nearly perfect, the overall score is primarily capped by this semantic gap between the model's medical vocabulary and your dataset's specific labels.

## 🧪 Test 7

| Field          | Value                                  |
|----------------|----------------------------------------|
| Test Set       | symptom-extraction-test-data-en.json   |
| Model          | openai/gpt-oss-120b (cloud)            |
| System Prompt  | symptom-extraction-prompt-1.txt        |
| Results        | symptom-extraction-result-7.txt        |

### 🔍 Model Overview — `openai/gpt-oss-120b`

| Property         | Value                              |
|------------------|------------------------------------|
| Developer        | OpenAI                             |
| Architecture     | Dense · Decoder-only Transformer   |
| Parameters       | ~120B                              |
| Deployment       | Cloud (API)                        |

> Large-scale dense model. Highest parameter count among all tested models. Exhibits the most pronounced Tendency toward over-inference — consistently extracts more clinically nuanced and anatomically precise terms than the ground truth labels require.

### 📊 Results

| Metric    | Score |
|-----------|-------|
| Precision | 0.695 |
| Recall    | 0.697 |
| F1 Score  | 0.689 |

### ⏱️ Performance

| Metric        |  Value   |
|---------------|----------|
| Total Time    | 362.56s  |
| Avg/Case      |  3.63s   |

### 💬 Commentary

The `gpt-oss-120b` model achieves an average **F1-score of 0.689**, making it the most descriptive but least "label-compliant" model among those tested. Its primary failure mode is over-descriptive labeling, where it frequently includes anatomical details (e.g., `severe abdominal pain` or `arm rash`) that result in total mismatches with the simpler ground truth labels (e.g., `abdominal pain` or `rash`). While its extraction logic is **physically accurate** and **highly** sensitive to nuances like `productive cough` or `high fever`, its lack of constraint to your specific ontology leads to significantly lower precision and recall compared to the **llama** or **phi** models

## 📊 Overall Results

| Model                                    | Size | Type  | Precision | Recall | F1    | Total time (s) | Avg/case (s) |
|------------------------------------------|------|-------|-----------|--------|-------|----------------|--------------|
| llama3.2:3b                              | 3B   | Local | 0.747     | 0.730  | 0.731 |     39.14      |     0.39     |
| llama3:8b                                | 8B   | Local | 0.809     | 0.806  | 0.800 |     57.39      |     0.57     |
| mistral-nemo:12b                         | 12B  | Local | 0.784     | 0.810  | 0.790 |     78.96      |     0.79     |
| qwen2.5:14b                              | 14B  | Local | 0.835     | 0.825  | 0.825 |     95.29      |     0.95     |
| phi4:14b                                 | 14B  | Local | 0.771     | 0.783  | 0.772 |     115.82     |     1.16     |
| meta-llama/llama-4-scout-17b-16e-instruct| 17B  | Cloud | 0.749     | 0.806  | 0.769 |     206.58     |     2.07     |
| openai/gpt-oss-120b                      | 120B | Cloud | 0.695     | 0.697  | 0.689 |     362.56     |     3.63     |

> ✅ `qwen2.5:14b` achieved the highest F1 score across all tested models, surpassing the 80% target threshold and outperforming models up to 8x larger.

## Conclusion

The evaluation shows that `qwen2.5:14b` is the most suitable model for the NLP layer in the implemented NeSy-X system. It achieved the highest F1 score and the highest precision while remaining locally executable.

This result is important from both technical and privacy perspectives. Since the user input may contain sensitive health information, local execution reduces the need to send unstructured medical text to external services. At the same time, the model provides sufficiently reliable structured symptom extraction for the next stages of the pipeline.

---

### ⚠️ Semantic Fragmentation and Normalization

The most critical issue identified is the **lack of strict canonical normalization**, which leads to **semantic fragmentation**. Different lexical representations of the same clinical concept (e.g., `lightheadedness`, `dizziness`, `presyncope`) result in distinct vector embeddings. This divergence reduces similarity accuracy and negatively affects downstream disease matching in the graph database.

---

### 🧠 Interpretation of Model Performance

Larger models often normalize, combine, or enrich symptom expressions using their internal medical knowledge. In this task, lower scores often reflect a mismatch between free clinical interpretation and strict ontology-oriented extraction. Analysis of the extraction logs reveals a distinct **"Tendency toward over-inference"** in larger architectures:

- **Descriptive Precision:** Larger models often normalize, combine, or enrich symptom expressions using their internal medical knowledge (e.g., `productive cough` instead of just `cough`).
- **Metric Penalty:** Such outputs can be medically meaningful, but they are not ideal for the proposed pipeline because each forwarded symptom must be explicitly grounded in the user input and suitable for mapping to a specific ontology node.
- **Instruction Following:** Mid-sized models like `qwen2.5:14b` demonstrate superior balance between clinical extraction and adherence to formatting constraints, leading to higher benchmark scores.

The main remaining limitation is the need for stricter control of symptom granularity. Future improvements may include additional prompt constraints, domain-specific fine-tuning, or post-processing rules that prevent the model from merging separate symptoms or introducing clinically plausible but unstated information.

---

**⬅ Previous:** [🚀 FastAPI](./backend.md) &nbsp;|&nbsp; **Next ➡:** [🧪 Testing the Embedding Layer](./embedding-test.md)
