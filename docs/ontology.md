---
title: 🧬 Biomedical Ontologies and Graph Representation
nav_order: 3
---

# 🧬 Biomedical Ontologies and Graph Representation

NeSy-X uses the Human Disease Ontology (DO) and the Symptom Ontology (SYMP) to represent disease and symptom concepts and their relations. This provides an explicit basis for symbolic reasoning, but the results remain dependent on the coverage and quality of the imported knowledge.

## 🦠 Human Disease Ontology (DO)

> **(Human Disease Ontology):** A standardized map of human diseases. It allows the system to understand the relationships between different medical conditions.

![Diseases Graph Visualization](../assets/images/diseases.png)

### 🔍 Query for Disease Count

```cypher
MATCH (d:Disease)
RETURN count(d);
```
**Total Diseases Counted:** `14460`

## 🩺 SYMP

> **(Symptom Ontology)**: Provides a standardized vocabulary for clinical signs and symptoms. NeSy uses this to extract, classify, and mathematically weight the symptoms reported by the user.

![Symptoms Graph Visualization](../assets/images/symptoms.png)

### 🔍 Query for Symptom Count

```cypher
MATCH (s:Symptom)
RETURN count(s);
```
**Total Symptoms Counted:** `1019`

### 📅 Grounding Versions

The listed versions describe the ontology snapshot used in the thesis, not necessarily the latest available releases.

| Ontology | Local Version | Release Cycle | Status | Source |
| :--- | :--- | :--- | :--- | :--- |
| **DOID** | 2025-09-30 | Monthly | Stable | [Download](https://github.com/DiseaseOntology/HumanDiseaseOntology/tree/main/src/ontology) |
| **SYMP** | 2024-05-17 | Irregular | Up-to-date | [Download](https://github.com/DiseaseOntology/SymptomOntology/releases) |

## 🔗 The Connection (RO_0002452)

In the world of medical data, the link between a disease and its symptoms is formally called RO_0002452 (simply meaning `has symptom`).

`RO_0002452` is the formal identifier for the `has_symptom` relation defined in the **Relations Ontology (RO)** — a standard library of biomedical relations maintained by the OBO Foundry community. This relation formally connects the `Disease` class to the `Symptom` class and serves as the foundation for interoperability between biomedical ontologies such as **DOID** (Disease Ontology) and **SYMP** (Symptom Ontology).

![Graph Visualization](../assets/images/graph-visualization.png)

---

### 🤔 Why OWL Restriction Instead of a Direct Edge?

#### ➡️ Representation of Disease-Symptom Relations

In standard graph databases (e.g., Neo4j), a connection is modeled as a simple binary edge between two nodes:

```cypher
(:Disease)-[:HAS_SYMPTOM]->(:Symptom)
```

This is a **first-order atomic statement** — without quantification, without logical force:

$$has\_symptom(Disease, Symptom)$$

The edge merely states that a connection **exists**, but says nothing about **which instances** it applies to or **under what conditions**.

#### 🦉 OWL Restriction (Ontological Axiom)

Formal biomedical ontologies (DO, HP, SYMP) are authored in the **W3C OWL 2 DL** standard, which uses Description Logic (DL). The relation `RO_0002452` is not declared as a simple edge in OWL, but rather as an **existential restriction** (`owl:Restriction`):

$$Disease \sqsubseteq \exists\, RO\_0002452 . Symptom$$

| Symbol | OWL Correspondent | Meaning |
|--------|-------------------|---------|
| $\sqsubseteq$ | `SubClassOf` | every instance of Disease... |
| $\exists$ | `owl:someValuesFrom` | ...has **at least one** relation... |
| `RO_0002452` | `ObjectProperty` | ...via `has_symptom`... |
| `Symptom` | `owl:Class` | ...to an instance of the Symptom class |

Logical translation: *"Every instance of the `Disease` class must be connected to at least one instance of the `Symptom` class via the `has_symptom` relation."*

---

### 🧩 How `neosemantics` (n4sch) Translates OWL into Neo4j

When the **neosemantics** library parses an OWL/RDF file, it cannot directly represent anonymous OWL restrictions as simple Neo4j edges — because an OWL restriction is not a binary relation but a **complex logical structure**. Instead, it creates an **intermediate anonymous node** that represents the restriction itself:

```text
 ┌─────────────────────┐
 │   (d:Disease)       │  ← DOID term (e.g., DOID:9351 - diabetes mellitus)
 └──────────┬──────────┘
            │
            │  [:n4sch__SCO_RESTRICTION]
            │  r.onPropertyURI = "http://purl.obolibrary.org/obo/RO_0002452"
            ▼
 ┌─────────────────────┐
 │  [owl:Restriction]  │  ← Anonymous node (blank node)
 └──────────┬──────────┘
            │
            │  [:n4sch__SVF] (someValuesFrom)
            ▼
 ┌─────────────────────┐
 │   (s:Symptom)       │  ← SYMP term (e.g., SYMP:0000570 - polydipsia)
 └─────────────────────┘
```

This three-step structure is a direct consequence of the **RDF blank node** mechanism that OWL uses for anonymous restrictions, which neosemantics maps into Neo4j nodes and edges.

---

### 🔍 Cypher Query for Counting `has_symptom` Relations

```cypher
MATCH ()-[r:n4sch__SCO_RESTRICTION]->()
WHERE r.onPropertyURI = "http://purl.obolibrary.org/obo/RO_0002452"
RETURN count(r);
```

**Result:** `2259` relations of type `has_symptom` between DOID and SYMP terms.

---

**⬅ Previous:** [🔧 Neo4j Desktop Setup & n10s Installation](./neo4j_setup.md) &nbsp;|&nbsp; **Next ➡:** [📚 Notebook Directory & Workflow](../notebooks/README.md)
