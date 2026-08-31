---
title: 🧪 Testing the Inference and Scoring Layer
nav_order: 9
---

# 🧪 Testing the Inference and Scoring Layer
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 📋 Overview

This section documents the evaluation of the inference and scoring layer used in the NeSy-X framework. This layer receives symptoms that have already been extracted and semantically mapped to ontology concepts. It then queries the knowledge graph, identifies candidate diseases, applies symptom-based scoring, and separates diseases that are inconsistent with explicitly negated symptoms.

The main purpose of this layer is not to make an independent clinical diagnosis, but to provide a controlled symbolic ranking of potential diseases based on formal ontology relations. The scoring process combines graph-based retrieval of diseases connected to mapped symptoms, Information Content (IC) weights for matched symptoms, normalization based on the total number of symptoms associated with each disease, and filtering based on explicitly absent symptoms.

Testing was conducted through ranking evaluation under complete and incomplete symptom profiles, followed by a separate validation of the negated symptom filter.

## 📐 Evaluation Methodology

The inference and scoring layer was evaluated using Hit@k metrics. These metrics measure whether the expected disease appears in the ranked list produced by the symbolic scoring mechanism.

**🟢 Hit@1**: The percentage of test cases in which the expected disease is ranked in first place.

$$Hit@1 = \frac{Disease_{rank=1}}{Total_{test}}$$

**🟡 Hit@3**: The percentage of test cases in which the expected disease appears among the top three results.

$$Hit@3 = \frac{Disease_{rank \leq 3}}{Total_{test}}$$

**🟡 Hit@5**: The percentage of test cases in which the expected disease appears among the top five results.

$$Hit@5 = \frac{Disease_{rank \leq 5}}{Total_{test}}$$

## 🗂️ Test Set

The test set (`symptom-disease-test-data.json`) was generated from disease-symptom relations in the ontology-backed knowledge graph. For each disease, the system formed an input symptom set based on its ontology profile and then executed the same Cypher query and scoring mechanism used in the implemented system.

The test data is structured as follows:

```json
{
  "disease": ["<disease name>"],
  "symptoms": [
    ["<symptom 1>"],
    ["<symptom 2>"],
    ...
  ]
}
```

Cases with fewer than two available symptoms were not suitable for ranking evaluation with min_match = 2, because they could not satisfy the minimum matching threshold after symptom removal.

## 📊 Hit@K Results

The `cypher-query.cyp` Cypher query was used. The test results are located in:

1. `inference-full-test.json`
2. `inference-partial1-test.json`
3. `inference-partial2-test.json`

| SCENARIO | TOTAL | Hit@1 | Hit@3 | Hit@5 |
|---|---|---|---|---|
| Full match (all symptoms) | 424 | 362 (85.4%) | 390 (92.0%) | 395 (93.5%) |
| Partial match (drop=1) | 424 | 243 (57.3%) | 287 (67.7%) | 302 (71.2%) |
| Partial match (drop=2) | 308 | 154 (50.0%) | 194 (63.0%) | 209 (67.9%) |

## 🚫 Negated Symptom Filter

The negated symptom filter checks whether a candidate disease is connected to a symptom that the user explicitly reported as absent. If such a symptom exists in the disease profile, the disease is marked with `passed_filter = false` and treated as excluded.

### ⚙️ Exclusion Test Methodology

The exclusion test was designed to verify whether a related disease is correctly excluded when it contains a negated symptom, while the target disease remains in the results when its ontology profile does not contain that symptom.

For each disease in the test set, the algorithm identifies similar diseases — those that share at least one symptom with it. From each similar disease, a symptom is selected that the similar disease has but our disease does not. This symptom is then passed as an `absent_symptom` to the query.

The query is then executed with the full symptom list of our disease as `present_symptoms`, and the selected symptom as `absent_symptoms`. Since our disease does not have that symptom in its ontological profile, it should not be affected by the filter and should remain ranked. The similar disease, however, does have that symptom in its profile, so it should be blocked and appear with `passed_filter = false` in the results.

Each test case therefore has two expected outcomes:

- **The target disease remains in the ranked results with `passed_filter = true`.** — it remains in the ranked list with `passed_filter = true`, because none of its ontological symptoms appear in the absent list.
- **The related disease is excluded with `passed_filter = false`.** — it is filtered out with `passed_filter = false`, because at least one of its ontological symptoms matches the absent symptom provided.

Two metrics are used: exclusion accuracy, which measures how often the related disease is correctly excluded, and survival accuracy, which measures how often the target disease is correctly retained.

The test results are located in `inference-exclusion-test.json`.

| Measure | Value |
|---|---|
| Total test cases | 1263 |
| Correctly excluded related diseases | 1263 |
| Incorrectly retained related diseases | 0 |
| Correctly retained target diseases | 1263 |
| Incorrectly excluded target diseases | 0 |
| Exclusion accuracy | 100% |
| Survival accuracy | 100% |

## ✅ Conclusion

**Full Match** achieves a Hit@1 of 85.4% and Hit@5 of 93.5%, which is a strong result for a purely symbolic ranker with no machine learning component. Zero no-result cases confirm that IC-weighted scoring and normalization work correctly across the entire test set.

**Partial Match (Drop=1)** shows an expected drop — Hit@1 falls to 57.3%, but a notable observation is that 116 out of 424 cases return no results. This occurs because some diseases have only 2 symptoms in the ontology, so removing one symptom causes them to fall below the `MIN_MATCH=2` threshold. The drop in Hit@1 is therefore not purely a ranking issue — it is partly a consequence of the minimum match threshold design decision.

**Partial Match (Drop=2)** reduces the test set to 308 cases, as diseases with fewer than 3 symptoms are excluded before evaluation. Hit@1 of 50.0% and Hit@5 of 67.9% with 78 no-result cases show that the system degrades gracefully as symptom availability decreases, which is realistic and expected behavior.

**The negated symptom filter** achieves 100% accuracy in both exclusion and survival tests across 1,263 cases. This confirms that the `passed_filter` mechanism works deterministically and provides a reliable basis for explaining why certain diseases are excluded.

Overall, the evaluation shows that the symbolic inference layer provides a transparent and controllable ranking mechanism. Its results should be interpreted as a technical validation of graph-based scoring and filtering, not as a clinical validation of diagnostic accuracy.

---

**⬅ Previous:** [🧪 Testing the Embedding Layer](./embedding-test.md) &nbsp;|&nbsp; **Next ➡:** [🧪 Testing the Explainable AI (XAI) Layer](./xai-test.md)
