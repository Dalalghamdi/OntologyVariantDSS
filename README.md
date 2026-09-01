# Ontology Variant DSS

**An ontology-driven research prototype for explainable genomic variant classification and clinical decision support**

Ontology Variant DSS is a research software prototype developed to support the study **“Leveraging ontologies for variant classification and decision support system.”** The system demonstrates how biomedical ontologies, semantic knowledge graphs, provenance-aware evidence representation, SPARQL querying, literature discovery, and ACMG/AMP evidence-combination logic can be integrated into a single framework for genomic variant interpretation.

The prototype is designed as an **explainable semantic decision-support environment**. Rather than storing variant evidence as disconnected database records, it represents variants, genes, diseases, phenotypes, publications, evidence statements, and classifications as interconnected RDF resources. This allows evidence to be queried, traced, and inspected through explicit semantic relationships.

> **Important:** This software is a research prototype. It is **not a medical device and must not be used for clinical diagnosis or patient management.** The current version combines ACMG/AMP criteria that have already been assessed; it does not independently determine whether biological evidence satisfies a particular ACMG/AMP criterion.

---

## Table of Contents

- [Overview](#overview)
- [Research Motivation](#research-motivation)
- [System Architecture](#system-architecture)
- [Implemented Features](#implemented-features)
- [Scientific Scope and Limitations](#scientific-scope-and-limitations)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Windows](#windows)
  - [macOS and Linux](#macos-and-linux)
- [Running the Application](#running-the-application)
- [How to Use the System](#how-to-use-the-system)
  - [1. Add a Variant](#1-add-a-variant)
  - [2. Review the Variant and Classification](#2-review-the-variant-and-classification)
  - [3. Import Variants from CSV](#3-import-variants-from-csv)
  - [4. Search PubMed](#4-search-pubmed)
  - [5. Query the Knowledge Graph with SPARQL](#5-query-the-knowledge-graph-with-sparql)
  - [6. Export the RDF Knowledge Graph](#6-export-the-rdf-knowledge-graph)
  - [7. Use the REST API](#7-use-the-rest-api)
- [ACMG/AMP Classification Logic](#acmgamp-classification-logic)
- [Knowledge Graph Model](#knowledge-graph-model)
- [GraphDB Integration](#graphdb-integration)
- [Example Workflow](#example-workflow)
- [Testing](#testing)
- [Data and Provenance](#data-and-provenance)
- [Current Limitations](#current-limitations)
- [Planned Development](#planned-development)
- [Research Use](#research-use)
- [Citation](#citation)
- [License](#license)
- [Authors](#authors)
- [Acknowledgment](#acknowledgment)
- [Disclaimer](#disclaimer)

---

## Overview

Clinical interpretation of genomic variants requires evidence from multiple heterogeneous resources. Relevant information may include:

- variant pathogenicity assertions;
- gene–disease relationships;
- population allele frequencies;
- patient phenotypes;
- functional evidence;
- segregation evidence;
- computational evidence;
- inheritance patterns;
- published biomedical literature; and
- evidence provenance.

These data are normally distributed across independent databases and publications and may use different identifiers, terminologies, and data models.

Ontology Variant DSS explores a semantic approach to this problem. The prototype represents genomic evidence in an **RDF knowledge graph** and links evidence to the variant being interpreted. ACMG/AMP evidence codes can then be recorded with their source and combined by a transparent rule-based classification engine.

The primary goals of the prototype are to demonstrate:

1. semantic integration of heterogeneous variant evidence;
2. explicit representation of relationships among variants, genes, diseases, phenotypes, evidence, and publications;
3. provenance and traceability of evidence;
4. ontology-based knowledge representation;
5. semantic querying using SPARQL;
6. transparent ACMG/AMP evidence combination; and
7. an architecture that can be extended toward automated evidence acquisition and reasoning.

---

## Research Motivation

Next-generation sequencing has substantially increased the number of variants encountered in clinical genomics. Variant interpretation, however, remains dependent on the synthesis of evidence distributed across genomic databases, disease resources, phenotype ontologies, population datasets, functional studies, and the biomedical literature.

The Ontology Variant DSS prototype investigates whether an ontology-driven architecture can provide a common semantic layer for this evidence.

Conceptually, the workflow is:

```text
Genomic and biomedical evidence
            |
            v
   Semantic representation
            |
            v
      RDF knowledge graph
            |
            +--------------------+
            |                    |
            v                    v
     SPARQL querying       Evidence provenance
            |                    |
            +---------+----------+
                      |
                      v
             ACMG/AMP evidence
                      |
                      v
             Rule-based reasoning
                      |
                      v
          Explainable classification
```

The system is intentionally designed so that evidence and reasoning remain inspectable rather than producing only an unexplained classification.

---

## System Architecture

The prototype contains several functional layers:

### 1. Evidence Input Layer

Variant-related information can be entered manually through the web interface or imported from a CSV file.

Supported fields include:

- HGVS variant description;
- gene;
- disease;
- phenotype terms;
- population allele frequency;
- ClinVar significance;
- ACMG/AMP evidence criteria;
- evidence description;
- evidence source; and
- PubMed identifier.

### 2. Semantic Knowledge Layer

The application converts the submitted information into an RDF knowledge graph.

The graph can represent entities such as:

```text
Variant
Gene
Disease
Phenotype
Evidence
Publication
ACMG/AMP Criterion
Classification
```

Relationships between these resources are represented explicitly rather than being implied by table structure.

### 3. Evidence and Provenance Layer

Evidence statements can retain information describing where the evidence originated, including a source description and PubMed identifier when supplied.

This enables a classification to be associated with its supporting evidence rather than existing as an isolated output.

### 4. Reasoning Layer

The application includes a rule-based ACMG/AMP combination engine.

The engine accepts already-assessed evidence codes such as:

```text
PVS1
PS3
PM2
PP1
BA1
BS3
BP4
```

and determines whether their combination satisfies the implemented categorical ACMG/AMP rules for:

- Pathogenic;
- Likely pathogenic;
- Variant of uncertain significance;
- Likely benign; or
- Benign.

### 5. Query Layer

The RDF graph can be queried using **SPARQL 1.1** through the application's SPARQL page.

### 6. Interoperability Layer

The knowledge graph can be exported as Turtle (`.ttl`) and subsequently imported into an RDF platform such as GraphDB.

---

## Implemented Features

The current prototype includes:

- RDF-based representation of genomic variant information;
- representation of variants, genes, diseases, phenotypes, evidence, publications, and classifications;
- persistent URI-based graph entities;
- ACMG/AMP criterion representation;
- rule-based ACMG/AMP evidence-combination logic;
- detection of conflicting pathogenic and benign evidence;
- evidence provenance;
- PubMed identifier storage;
- PubMed search through NCBI E-utilities when internet access is available;
- SPARQL 1.1 querying;
- CSV batch import;
- Turtle/RDF export;
- local RDF storage using RDFLib;
- browser-based interface;
- REST API for variant listing and classification;
- automated tests for the ACMG classification component; and
- an RDF/OWL starter ontology in Turtle format.

---

## Scientific Scope and Limitations

The distinction between **evidence assessment** and **evidence combination** is fundamental to this project.

### What the current system does

If a qualified user or validated external process determines that a variant satisfies criteria such as:

```text
PVS1 + PM2
```

the application can combine those criteria using the implemented ACMG/AMP categorical rules and return an explainable result.

For example:

```text
PVS1 + PM2
```

is classified by the current engine as:

```text
Likely pathogenic
```

### What the current system does not do

The prototype does **not** currently examine a raw variant and independently determine that:

```text
this variant satisfies PVS1
```

or:

```text
this allele frequency satisfies PM2
```

or:

```text
this publication provides PS3-level functional evidence
```

Those decisions require criterion-specific biological logic, gene/disease context, evidence calibration, and validation.

Therefore, this version should be described as an **ontology-driven evidence integration and ACMG/AMP evidence-combination prototype**, rather than a fully autonomous clinical variant interpreter.

---

## Technology Stack

The project uses:

- **Python**
- **FastAPI** — web application and REST API
- **Uvicorn** — ASGI server
- **RDFLib** — RDF graph construction, storage, serialization, and querying
- **SPARQL 1.1** — semantic graph querying
- **Jinja2** — HTML templates
- **HTML/CSS** — user interface
- **NCBI E-utilities** — PubMed search
- **Turtle/RDF** — knowledge graph serialization

The exported RDF is suitable for subsequent use with **GraphDB** or another standards-compliant RDF triplestore.

---

## Project Structure

```text
ontology_variant_dss/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- graph.py
|   |-- acmg.py
|   |-- pubmed.py
|   |
|   |-- static/
|   |   `-- style.css
|   |
|   `-- templates/
|       |-- base.html
|       |-- index.html
|       |-- new_variant.html
|       |-- variant.html
|       |-- pubmed.html
|       |-- sparql.html
|       `-- import_done.html
|
|-- data/
|   `-- sample_variants.csv
|
|-- ontology/
|   `-- variant_dss.ttl
|
|-- tests/
|   `-- test_acmg.py
|
|-- requirements.txt
|-- run.bat
|-- run.sh
`-- README.md
```

### Main files

**`app/main.py`**

Defines the FastAPI application, web routes, CSV import, RDF export, PubMed page, SPARQL interface, and REST endpoints.

**`app/graph.py`**

Implements the RDF knowledge graph and operations for creating and retrieving semantic resources.

**`app/acmg.py`**

Contains the ACMG/AMP evidence-strength mapping and categorical evidence-combination logic.

**`app/pubmed.py`**

Provides PubMed literature searching through NCBI E-utilities.

**`ontology/variant_dss.ttl`**

Contains the starter semantic model used by the project.

**`data/sample_variants.csv`**

Example input data for testing the import workflow.

---

# Installation

## Requirements

Before installation, make sure you have:

- Python 3.10 or later recommended;
- `pip`;
- a terminal or command prompt;
- a modern web browser; and
- internet access if you want to use live PubMed searching.

GraphDB is **not required** to run the prototype locally.

---

## Windows

### 1. Download or clone the repository

Using Git:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd ontology_variant_dss
```

Alternatively, download the repository as a ZIP file from GitHub, extract it, and open Command Prompt or PowerShell inside the extracted project directory.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Command Prompt:

```bash
.venv\Scripts\activate
```

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell prevents script execution, you can use Command Prompt instead.

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the application

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Open the application

Open the following address in your browser:

```text
http://127.0.0.1:8000
```

---

## macOS and Linux

### 1. Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd ontology_variant_dss
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate it

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Open the application

```text
http://127.0.0.1:8000
```

---

# Running the Application

After installation, the standard development command is:

```bash
uvicorn app.main:app --reload --port 8000
```

`--reload` automatically restarts the development server when source files change.

When the application starts successfully, Uvicorn should report that it is running locally.

Open:

```text
http://127.0.0.1:8000
```

To stop the server, press:

```text
Ctrl + C
```

---

# How to Use the System

## 1. Add a Variant

From the home page, open the form for adding a new variant.

The application accepts the following information.

### Variant

Enter the HGVS description.

Example:

```text
NM_000059.4:c.5946del
```

### Gene

Example:

```text
BRCA2
```

### Disease

Enter the associated disease or condition when known.

### Phenotypes

Enter phenotype terms separated by commas.

For example:

```text
Breast carcinoma, Ovarian carcinoma
```

### Allele Frequency

Enter a numeric population allele frequency if available.

### ClinVar Significance

Enter the relevant ClinVar clinical significance when it is being recorded as source information.

### ACMG/AMP Criteria

Enter already-assessed ACMG/AMP criteria separated by commas or semicolons.

Example:

```text
PVS1, PM2
```

### Evidence Notes

Describe why the evidence was recorded.

For example:

```text
Loss-of-function evidence assessed by reviewer.
```

### Evidence Source

Record the source from which the evidence was obtained.

Examples may include:

```text
ClinVar
gnomAD
PubMed
Manual expert review
```

### PMID

If the evidence is supported by a PubMed-indexed publication, enter the PMID.

After submission, the system:

1. creates or updates the semantic variant representation;
2. records the supplied evidence;
3. links ACMG/AMP evidence to the variant;
4. records provenance;
5. executes the evidence-combination engine;
6. stores the resulting classification; and
7. displays the variant record.

---

## 2. Review the Variant and Classification

After creating a variant, the application redirects to its variant detail page.

The page displays the information stored for the variant and its evidence-based classification.

The classification response includes the evidence codes used by the reasoning engine and the reason that the evidence combination produced the result.

This is intended to make the classification pathway inspectable.

---

## 3. Import Variants from CSV

The home page provides a CSV import function.

A sample file is included at:

```text
data/sample_variants.csv
```

The expected columns are:

```text
variant,
gene,
disease,
phenotypes,
allele_frequency,
clinvar_significance,
criteria,
evidence_notes,
evidence_source,
pmid
```

The actual header should appear on one line:

```csv
variant,gene,disease,phenotypes,allele_frequency,clinvar_significance,criteria,evidence_notes,evidence_source,pmid
```

### Multiple phenotypes

Separate phenotype values with:

```text
|
```

Example:

```text
HP:0003002|HP:0000726
```

### Multiple ACMG/AMP criteria

Separate criteria using commas or semicolons.

Example:

```text
PVS1;PM2;PP1
```

When the CSV is imported, each valid row is converted into semantic resources and its evidence criteria are passed to the classification engine.

---

## 4. Search PubMed

The application contains a PubMed search page.

You can search using combinations of:

- HGVS nomenclature;
- gene symbols;
- protein changes;
- disease names; and
- phenotype terms.

Example query:

```text
BRCA2 NM_000059.4:c.5946del
```

The module uses NCBI E-utilities and therefore requires internet access.

### Important

PubMed retrieval is currently an **evidence discovery function**.

The application does not automatically interpret a retrieved publication as satisfying PS3, PP1, BS3, or another ACMG/AMP criterion. Such evidence assessment must currently be performed separately.

---

## 5. Query the Knowledge Graph with SPARQL

Open the SPARQL page from the application.

A default query is provided.

Example:

```sparql
PREFIX dss: <https://example.org/variant-dss/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?variant ?classification
WHERE {
    ?v a dss:Variant ;
       rdfs:label ?variant .

    OPTIONAL {
        ?v dss:hasClassification ?classification
    }
}
ORDER BY ?variant
```

This retrieves variants and their stored classifications.

Because the underlying data are represented as RDF, more complex graph queries can be developed to investigate relationships between genomic entities and their evidence.

---

## 6. Export the RDF Knowledge Graph

The application provides an RDF export endpoint:

```text
/export/ttl
```

In a local installation, open:

```text
http://127.0.0.1:8000/export/ttl
```

The endpoint returns the current graph in **Turtle** format.

The exported graph can be saved as a `.ttl` file and imported into GraphDB or another RDF-compatible platform.

---

## 7. Use the REST API

The prototype exposes two basic API endpoints.

### List variants

```http
GET /api/variants
```

Local address:

```text
http://127.0.0.1:8000/api/variants
```

### Classify an ACMG/AMP evidence combination

```http
POST /api/classify
```

Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/classify \
  -H "Content-Type: application/json" \
  -d "{\"criteria\":[\"PVS1\",\"PM2\"]}"
```

On macOS/Linux shells, the following form is also commonly used:

```bash
curl -X POST http://127.0.0.1:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"criteria":["PVS1","PM2"]}'
```

Example response:

```json
{
  "classification": "Likely pathogenic",
  "reason": "One very-strong and one moderate pathogenic criterion are present.",
  "codes": [
    "PM2",
    "PVS1"
  ],
  "counts": {
    "moderate_pathogenic": 1,
    "very_strong": 1
  }
}
```

---

# ACMG/AMP Classification Logic

The system recognizes criterion strength from the ACMG/AMP code prefix.

| Prefix | Evidence strength |
|---|---|
| `PVS` | Very strong pathogenic |
| `PS` | Strong pathogenic |
| `PM` | Moderate pathogenic |
| `PP` | Supporting pathogenic |
| `BA` | Stand-alone benign |
| `BS` | Strong benign |
| `BP` | Supporting benign |

The current implementation combines recorded evidence according to categorical rules encoded in `app/acmg.py`.

### Example 1

Input:

```text
PVS1 + PM2
```

Output:

```text
Likely pathogenic
```

### Example 2

Input:

```text
PVS1 + PM2 + PP1
```

Output:

```text
Pathogenic
```

### Example 3

Input:

```text
BA1
```

Output:

```text
Benign
```

### Conflicting evidence

If both pathogenic and benign evidence codes are supplied, the current prototype conservatively returns:

```text
Variant of uncertain significance
```

with a reason indicating that conflicting pathogenic and benign evidence is present.

### No qualifying combination

If the supplied evidence does not satisfy an implemented pathogenic, likely pathogenic, benign, or likely benign combination, the result is:

```text
Variant of uncertain significance
```

---

# Knowledge Graph Model

The semantic model is designed around explicit relationships among biomedical entities.

A simplified conceptual example is:

```text
Variant
  |
  +-- associated with --> Gene
  |
  +-- associated with --> Disease
  |
  +-- has phenotype --> Phenotype
  |
  +-- has evidence --> Evidence Statement
                           |
                           +-- criterion --> ACMG/AMP Criterion
                           |
                           +-- source --> Evidence Source
                           |
                           +-- publication --> PMID
  |
  +-- has classification --> Classification
```

The use of RDF makes the evidence graph extensible. Additional biomedical ontologies and external identifiers can be incorporated without redesigning the entire data model.

The project includes:

```text
ontology/variant_dss.ttl
```

as the starter ontology/semantic model.

---

# GraphDB Integration

GraphDB is not necessary for local execution because the prototype uses RDFLib internally.

However, GraphDB can be used for a larger semantic deployment.

A basic workflow is:

1. run the Ontology Variant DSS;
2. add or import variant evidence;
3. export the graph using `/export/ttl`;
4. save the returned Turtle content as a `.ttl` file;
5. create a repository in GraphDB;
6. import the Turtle file into the repository; and
7. query the graph using GraphDB's SPARQL interface.

The current application does not require a live GraphDB connection to function.

For a production or publication-scale deployment, the persistence layer can be extended so that the application communicates directly with a GraphDB SPARQL endpoint.

---

# Example Workflow

A simple demonstration can be performed as follows.

### Step 1 — Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

### Step 2 — Open the web interface

```text
http://127.0.0.1:8000
```

### Step 3 — Create a variant

Enter:

```text
Variant:
NM_000059.4:c.5946del

Gene:
BRCA2

Criteria:
PVS1, PM2

Evidence source:
Manual expert assessment
```

### Step 4 — Submit

The application records the variant and evidence in the RDF graph.

### Step 5 — Review classification

The evidence combination:

```text
PVS1 + PM2
```

returns:

```text
Likely pathogenic
```

### Step 6 — Inspect the graph

Open the SPARQL interface and execute a query against the stored semantic data.

### Step 7 — Export

Open:

```text
http://127.0.0.1:8000/export/ttl
```

to retrieve the graph in Turtle format.

---

# Testing

The project includes tests for the ACMG/AMP evidence-combination component.

From the project directory, run:

```bash
pytest
```

If `pytest` is not already available in your environment, install it first:

```bash
pip install pytest
```

The tests are located in:

```text
tests/test_acmg.py
```

Testing should be expanded as the evidence-assessment and external-data integration layers are developed.

---

# Data and Provenance

Evidence provenance is a central design requirement of the system.

Where available, evidence records can include:

- evidence source;
- descriptive evidence notes; and
- PubMed identifier.

This allows evidence to remain linked to its origin.

For a publication-grade implementation, provenance should be expanded to include, where applicable:

- source database identifier;
- database version;
- retrieval date;
- publication identifier;
- assertion author or process;
- evidence extraction method;
- ontology identifier;
- confidence or review status; and
- rule version used for classification.

---

# Current Limitations

The current prototype has several important limitations.

### 1. ACMG criteria are not automatically assigned

The software combines already-assessed criteria. It does not yet implement validated criterion-specific engines for determining PVS1, PS3, PM2, PP3, or other evidence codes directly from biological observations.

### 2. No autonomous clinical interpretation

The output must not be treated as a clinical diagnosis or final laboratory interpretation.

### 3. PubMed search is discovery only

Retrieved publications are not automatically converted into ACMG/AMP evidence.

### 4. External genomic resources are not fully automated

Automated ingestion from ClinVar, gnomAD, OMIM, HPO, GO, and other resources is a planned extension rather than a complete feature of the current prototype.

### 5. Ontology mappings require further formalization

The included semantic model is a starter implementation. A publication-grade version should map concepts to exact reusable ontology IRIs where appropriate and formally document ontology reuse.

### 6. No clinical performance claims

Accuracy, sensitivity, specificity, concordance, reduction in VUS, or improvement over commercial interpretation systems should not be claimed until the system is evaluated against an independently curated benchmark dataset.

---

# Planned Development

The intended next stage is an automated, provenance-aware evidence acquisition and assessment pipeline.

Planned components include:

### Automated ClinVar Integration

Retrieve:

- clinical significance;
- review status;
- associated conditions;
- submitter assertions; and
- variant identifiers.

### Automated gnomAD Integration

Retrieve population allele frequencies and use validated disease/gene-aware thresholds to support population evidence assessment.

### HPO Integration

Normalize phenotype information using Human Phenotype Ontology identifiers and support phenotype-driven semantic querying.

### Disease Knowledge Integration

Connect variants and genes with standardized disease concepts and disease–gene relationships.

### Literature Mining

Extend PubMed retrieval with:

- named entity recognition;
- gene recognition;
- variant recognition;
- disease recognition;
- phenotype recognition;
- relationship extraction; and
- evidence statement extraction.

### Criterion-Specific ACMG/AMP Engines

Implement and validate individual evidence assessment modules rather than inferring evidence codes solely from user input.

Potential examples include:

- PVS1 decision logic;
- population-frequency evidence;
- phenotype-specific evidence;
- segregation evidence;
- computational prediction evidence; and
- functional-study evidence.

### Provenance Expansion

Represent the complete reasoning chain from source evidence to criterion to final classification.

Conceptually:

```text
Source
   |
   v
Evidence statement
   |
   v
Normalized semantic entity
   |
   v
ACMG/AMP criterion
   |
   v
Evidence combination
   |
   v
Variant classification
```

### Benchmark Validation

Evaluate the framework using an independently curated variant dataset and report performance only after a predefined validation protocol has been completed.

---

# Research Use

This repository is intended to support research on:

- biomedical ontologies;
- clinical decision support systems;
- genomic variant interpretation;
- semantic knowledge graphs;
- explainable decision support;
- evidence provenance;
- Semantic Web technologies;
- RDF and SPARQL;
- ACMG/AMP evidence representation; and
- integration of structured and literature-derived genomic evidence.

Researchers are encouraged to distinguish clearly between:

1. **retrieval of evidence**;
2. **semantic representation of evidence**;
3. **assessment of evidence against an ACMG/AMP criterion**; and
4. **combination of assessed criteria into a classification**.

These are separate computational and scientific tasks and should be validated independently.

---

# Citation

If you use this repository in academic work, please cite the associated manuscript:

```text
Alghamdi D, AlFaiz A.
Leveraging ontologies for variant classification and decision support system.
Manuscript in preparation.
```

A formal journal citation should replace the text above once the article is published.

A `CITATION.cff` file can also be added to the repository after the final publication metadata and DOI are available.



---

# Authors

**Dalia Alghamdi**  
King Fahad Medical City  
Riyadh, Saudi Arabia

**Ali AlFaiz**  
King Fahad Medical City  
Riyadh, Saudi Arabia

---

# Acknowledgment

This research was funded by **King Fahad Medical City (KFMC)**.

---

# Disclaimer

Ontology Variant DSS is provided for **research, software development, and academic demonstration purposes only**.

It is not validated for clinical use and must not be used as a substitute for professional genomic interpretation, laboratory validation, medical judgement, or established clinical variant interpretation procedures.

All variant classifications produced by this prototype depend on the evidence criteria supplied to the system. Users are responsible for independently validating the underlying evidence and its applicability before drawing scientific or clinical conclusions.
