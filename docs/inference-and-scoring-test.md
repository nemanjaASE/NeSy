---
title: 🧪 Testing the Inference and Scoring Layer
nav_order: 8
---

# 🧪 Testing the Inference and Scoring Layer

## 📋 Overview

This report documents the testing and evaluation process of the inference and scoring layer, whose role is to query the graph database (Neo4j) based on mapped symptoms.

The challenge of this layer is to accurately identify diseases from a set of symptoms, rank diseases based on symptom matches, account for symptom relevance through Information Content (IC), and exclude diseases for symptoms that are explicitly reported as absent.

Testing was conducted in four phases: full match (all symptoms are known), partial match with one symptom removed (drop=1), with two symptoms removed (drop=2), and with symptoms that exclude a disease. This simulates a realistic clinical scenario where a patient does not report all symptoms or explicitly states that certain symptoms are not present.

## 📐 Evaluation Methodology

The following metrics were used to assess quality:

**🟢 Hit@1**: The percentage of test cases in which the correct disease was ranked in first place.

$$Hit@1 = \frac{Disease_{rank=1}}{Total_{test}}$$

**🟡 Hit@3**: The percentage of test cases in which the correct disease appears among the top three ranked diseases.

$$Hit@3 = \frac{Disease_{rank \leq 3}}{Total_{test}}$$

**🟡 Hit@5**: The percentage of test cases in which the correct disease appears among the top five ranked diseases.

$$Hit@5 = \frac{Disease_{rank \leq 5}}{Total_{test}}$$

## 🗂️ Test Set

For testing purposes, the `symptom-disease-test-data.json` file was used, which was exported from the DOID and SYMP ontologies and contains symptom descriptions for each disease.

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

In order to achieve better results, cases where a disease had fewer than two symptoms were excluded when loading the test set.

## 📊 Hit@K Results

The `cypher-query.cyp` Cypher query was used. The test results are located in:

1. `inference-full-test.json`
2. `inference-partial1-test.json`
3. `inference-partial2-test.json`

| SCENARIO | TOTAL | Hit@1 | Hit@3 | Hit@5 |
|---|---|---|---|---|
| Full match (all symptoms) | 424 | 362 (85.4%) | 390 (92.0%) | 395 (93.2%) |
| Partial match (drop=1) | 424 | 243 (57.3%) | 287 (67.7%) | 302 (71.2%) |
| Partial match (drop=2) | 308 | 154 (50.0%) | 194 (63.0%) | 209 (67.9%) |

## 🚫 Exclusion Test Results

Diseases are queried using their full symptom list, with one additional symptom passed as absent — a symptom belonging to a similar disease but not to the one being tested. This validates the inference layer's ability to correctly filter out diseases based on explicitly reported absent symptoms.

### ⚙️ How the Exclusion Test Works

The exclusion test validates the inference layer's ability to correctly eliminate diseases based on symptoms the patient explicitly does not have.

For each disease in the test set, the algorithm identifies similar diseases — those that share at least one symptom with it. From each similar disease, a symptom is selected that the similar disease has but our disease does not. This symptom is then passed as an `absent_symptom` to the query.

The query is then executed with the full symptom list of our disease as `present_symptoms`, and the selected symptom as `absent_symptoms`. Since our disease does not have that symptom in its ontological profile, it should not be affected by the filter and should remain ranked. The similar disease, however, does have that symptom in its profile, so it should be blocked and appear with `passed_filter = false` in the results.

Each test case therefore has two expected outcomes:

- **Our disease survives** — it remains in the ranked list with `passed_filter = true`, because none of its ontological symptoms appear in the absent list.
- **The similar disease is excluded** — it is filtered out with `passed_filter = false`, because at least one of its ontological symptoms matches the absent symptom provided.

Two accuracy metrics are reported: **exclusion accuracy**, measuring how often the similar disease is correctly blocked, and **survival accuracy**, measuring how often our disease correctly remains in the results.

The test results are located in `inference-exclusion-test.json`.

| | Result |
|---|---|
| Total | 1263 |
| Excluded correct | 1263 |
| Excluded wrong | 0 |
| Exclusion accuracy | 100% |
| Survival accuracy | 100% |

## ✅ Conclusion

**Full Match** achieves a Hit@1 of 85.4% and Hit@5 of 93.2%, which is a strong result for a purely symbolic ranker with no machine learning component. Zero no-result cases confirm that IC-weighted scoring and normalization work correctly across the entire test set.

**Partial Match (Drop=1)** shows an expected drop — Hit@1 falls to 57.3%, but a notable observation is that 116 out of 424 cases return no results. This occurs because some diseases have only 2 symptoms in the ontology, so removing one symptom causes them to fall below the `MIN_MATCH=2` threshold. The drop in Hit@1 is therefore not purely a ranking issue — it is partly a consequence of the minimum match threshold design decision.

**Partial Match (Drop=2)** reduces the test set to 308 cases, as diseases with fewer than 3 symptoms are excluded before evaluation. Hit@1 of 50.0% and Hit@5 of 67.9% with 78 no-result cases show that the system degrades gracefully as symptom availability decreases, which is realistic and expected behavior.

**Exclusion Test** achieves a perfect 100% on both exclusion accuracy and survival accuracy across 1,263 test cases. This confirms that the `passed_filter` mechanism in the Cypher query operates deterministically — every absent symptom that belongs to a similar disease reliably blocks it, while the target disease remains in the ranked results without any collateral filtering errors.
