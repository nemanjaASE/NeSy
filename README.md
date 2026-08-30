[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen?logo=github)](https://nemanjaase.github.io/NeSy-X/)
[![Backend CI](https://github.com/nemanjaASE/NeSy-X/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/nemanjaASE/NeSy-X/actions/workflows/backend-ci.yml)
[![Frontend CI](https://github.com/nemanjaASE/NeSy-X/actions/workflows/frontend-ci.yml/badge.svg)](https://github.com/nemanjaASE/NeSy-X/actions/workflows/frontend-ci.yml)

<h1 align="center">🌟 NeSy-X</h1>
<p align="center"><strong>Neuro-Symbolic eXplainable Framework for Diagnostic Support</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Neo4j-008CC1?style=for-the-badge&logo=neo4j&logoColor=white">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB">
  <br>
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white">
  <img src="https://img.shields.io/badge/Groq-1a1a1a?style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/Meta%20Llama-04ADFF?style=for-the-badge&logo=meta&logoColor=white">
  <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black">
  <br>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge">
</p>

---

NeSy-X is a research framework that integrates large language models, text vector representations, biomedical ontologies, and a knowledge graph to support symptom-based identification and ranking of candidate diseases.

Developed as part of a master's thesis, the framework separates neural language processing from symbolic reasoning. Language models extract symptoms from unstructured text, vector representations support their mapping to ontological concepts, and the symbolic layer evaluates candidate diseases using explicit graph relations, symptom weights, and filtering rules. An explanation layer converts the structured results into natural-language explanations.

## 🧭 Design Principles

NeSy-X is designed to support four complementary properties:

- **Traceability:** following the processing steps from user input through extracted symptoms and mapped concepts to ranked disease candidates.
- **Verifiability:** checking symbolic results against the graph relations, symptom weights, and rules used to obtain them.
- **Explainability:** presenting understandable reasons for disease ranking and exclusion.
- **Controllability:** configuring processing behavior through similarity thresholds, matching requirements, filtering rules, and result limits.

These properties support transparency of the overall workflow without assuming that the internal operation of a language model is fully interpretable.

## 🔄 Framework Workflow

NeSy-X operates through two phases: preparation and execution. The preparation phase establishes and enriches the knowledge graph, while the execution phase processes user input and produces ranked disease candidates with accompanying explanations.

![Preparation and execution phases of NeSy-X](./assets/images/NeSy-workflow.png)

### ⚙️ Preparation Phase

The preparation phase establishes an enriched knowledge graph based on the Human Disease Ontology (DO) and the Symptom Ontology (SYMP). Disease and symptom concepts are imported into Neo4j together with their ontological relations.

Symptom nodes are enriched with Information Content (IC) weights and vector representations of their textual labels. These precomputed properties support subsequent disease scoring and semantic mapping.

### ⚡ Execution Phase

1. **Symptom extraction:** a large language model identifies present and explicitly negated symptoms in the user's text.
2. **Semantic mapping:** extracted expressions are mapped to SYMP concepts using vector representations and a configurable cosine-similarity threshold.
3. **Symbolic reasoning:** graph queries retrieve candidate diseases, which are scored using matched symptom weights and square-root normalization. A negated-symptom filter separates included and excluded candidates.
4. **Explanation generation:** the XAI layer uses structured symbolic results to explain the ranking and filtering decisions.

The language model is not used as a standalone diagnostic mechanism. Candidate retrieval, scoring, and filtering are based on the knowledge graph and explicitly defined processing rules.

## 🏗️ Implementation

The prototype consists of a React client, a FastAPI backend, and a Neo4j knowledge graph. Neural processing uses pretrained language models and a text vector representation model, with integrations for local and cloud LLM execution.

The architecture separates language processing, semantic mapping, symbolic evaluation, and explanation generation, allowing these components to be configured and evaluated individually.

## 🔬 Research Scope and Evaluation

The research contribution lies in integrating these components into a unified diagnostic-support workflow and evaluating their behavior under controlled conditions.

Evaluation covers symptom extraction, semantic mapping, disease ranking, negated-symptom filtering, and explanation generation. The study also examines the practical trade-offs between local and cloud model execution.

> ⚠️ **NeSy-X is a research prototype, not a clinically validated diagnostic system.** Evaluation was conducted on controlled examples and ontology-derived datasets rather than real patient data. Ranking scores and cosine-similarity values are not calibrated disease probabilities. Results remain dependent on ontology coverage, extraction and mapping quality, and the reliability of generated explanations.

The framework must not be used for medical diagnosis or treatment decisions.

## 📚 Documentation

- [Neo4j and ontology setup](./docs/neo4j_setup.md)
- [Ontology structure and OWL representation](./docs/ontology.md)
- [Preparation and evaluation notebooks](./notebooks/README.md)
- [Local model setup with Ollama](./docs/ollama_setup.md)
- [Backend setup and configuration](./backend/README.md)
- [Frontend setup](./frontend/README.md)
- [Symptom extraction evaluation](./docs/nlp-test.md)
- [Semantic mapping evaluation](./docs/embedding-test.md)
- [Symbolic reasoning, scoring, and filtering evaluation](./docs/inference-and-scoring-test.md)
- [Explanation generation evaluation](./docs/xai-test.md)

## 📄 License

Distributed under the MIT License. See [LICENSE](./LICENSE).
