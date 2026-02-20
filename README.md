# Cloud Infrastructure Drift Detection & Remediation in Multi-Cloud Environments

> **A Systematic Literature Review (SLR) following PRISMA 2020 guidelines**
> Covering 96 peer-reviewed studies published between 2019 and 2025.

---

## Overview

This repository contains all artefacts associated with a Systematic Literature Review (SLR) on **cloud infrastructure drift** — the divergence between the desired state declared in Infrastructure as Code (IaC) configurations and the actual deployed state in cloud environments.

The review addresses six research questions spanning drift detection accuracy, remediation strategies, IaC tool capabilities, multi-cloud challenges, policy-driven compliance, and state reconciliation mechanisms.

---

##  Interactive Homepage

Open **`cloud_infra_drift_slr/index.html`** in any modern browser for the interactive research homepage featuring:

- **Stats dashboard** — key metrics at a glance (96 studies, 44 full-text reviewed, 380% research growth 2019→2025)
- **Searchable papers table** — filter by year, PDF availability, or free-text search across titles, authors, and summaries
- **Inline PDF preview** — click any paper to read it right in the page (no new tab needed)
- **Read SLR tab** — full embedded PDF of the complete review document (`SLR.pdf`)

> **Note:** For PDF previews to work, open the file via a local HTTP server or directly in Chrome/Edge. Copy your final review PDF as `cloud_infra_drift_slr/SLR.pdf`.

---

## Repository Structure

```
slr/
├── cloud_infra_drift_slr/          # Main project directory
│   ├── index.html                  # Interactive SLR homepage (open this!)
│   ├── SLR.pdf                     # Full SLR document (add your PDF here)
│   ├── pdf_viewer.html             # Standalone PDF viewer utility
│   ├── Cloud_Infrastructure_Drift_SLRV2.txt  # Raw SLR text source
│   ├── Revised_SLR_Protocol_Cloud_Infrastructure_Drift (1).md
│   │
│   ├── 43_base_papers/             # 43 PDF papers included in full-text review
│   ├── 104-paper_for_full_text_review/  # 104 candidates assessed for eligibility
│   │
│   ├── 44_papers_fulltext_included.csv      # Metadata for full-text included papers
│   ├── 156_papers_after_screening.csv       # Papers after abstract screening
│   ├── 683_papers_after_deduplication_with_abstract.csv
│   ├── fulltext_screening_results.csv
│   ├── full_text_analysis_104_available_pdf_after_abstract_screening.csv
│   ├── deduplication_statistics.json
│   ├── final_included_papers.json
│   ├── fulltext_screening_report.json
│   │
│   ├── Query_Results/              # Raw database query outputs
│   ├── Study_Selection/            # Selection decision logs
│   │
│   ├── images/                     # Generated SLR visualisation charts (PNG, 600 DPI)
│   │   ├── prisma_flow_diagram.png
│   │   ├── temporal_distribution.png
│   │   ├── study_types_distribution.png
│   │   ├── publication_venues.png
│   │   ├── geographic_distribution.png
│   │   ├── drift_detection_comparison.png
│   │   ├── remediation_strategies_comparison.png
│   │   ├── iac_tools_comparison.png
│   │   ├── thematic_clusters.png
│   │   └── key_metrics_dashboard.png
│   │
│   └── scripts/
│       ├── generate_slr_charts.py  # Generates all 10 charts (white bg, 600 DPI)
│       └── build_website.py        # Legacy site builder script
│
├── authors.csv                     # Paper number → author → PDF filename mapping
├── build_index.py                  # Python script to regenerate index.html
├── verify_index.py                 # Verification script for index.html correctness
└── README.md                       # This file
```

---

## Research Design

### Search Strategy (PRISMA 2020)

| Stage | Count | Notes |
|---|---|---|
| Initial retrieval | 830 | SciSpace (600), Google Scholar (110), arXiv (120) |
| After deduplication | 683 | 147 duplicates removed (17.7%) |
| After year filter (2019–2025) | 391 | 292 excluded |
| After abstract screening (relevance ≥ 3.0) | 156 | 235 excluded |
| Full-text assessed for eligibility | 104 | |
| **Final included studies** | **96** | 44 full-text + 52 abstract-only |

### Research Questions

| ID | Question |
|---|---|
| **RQ1** | What drift detection methods exist and how do they compare on accuracy, latency, and coverage? |
| **RQ2** | Which remediation strategies achieve the best MTTR and automation level? |
| **RQ3** | What are the capabilities and limitations of current IaC tools for drift management? |
| **RQ4** | What unique challenges arise in multi-cloud environments for drift detection? |
| **RQ5** | How do policy-as-code frameworks support compliance and drift prevention? |
| **RQ6** | What state management and reconciliation mechanisms are most effective? |

---

## Key Findings

| Metric | Value | Source |
|---|---|---|
| AI-augmented drift detection accuracy | **97%** (pass@3) | Yang et al., 2025 (NSync) |
| Security misconfiguration reduction via policy-as-code | **78%** | Ahuja, 2025; Paul et al., 2024 |
| Fewer audit findings with IaC compliance automation | **83%** | Paul et al., 2024 |
| MTTR reduction with full automation | **50–67%** | Laheri, 2025; Nelloru, 2025 |
| Terraform market share (2025) | **62%** | Davidson et al., 2025 |
| Research publication growth (2019→2025) | **380%** | This SLR |
| Multi-cloud adoption in tech sector | **94%** | Multiple sources |
| Faster infrastructure deployment with IaC | **60%** | Challa, 2025; Marella, 2024 |

### Six Thematic Clusters

1. **IaC Tool Evolution** (25%) — Terraform dominance, CDK/Pulumi growth, LLM-assisted generation
2. **AI-Augmented Drift Reconciliation** (18%) — NSync API trace analysis, RL self-healing
3. **Multi-Cloud Orchestration** (15%) — provider abstraction, cross-cloud state sync
4. **Policy-Driven Frameworks** (16%) — OPA, Sentinel, preventive + detective controls
5. **GitOps Methodologies** (14%) — ArgoCD, Flux, 30s–5min reconciliation cycles
6. **State Management** (12%) — defect taxonomy, reconciliation validation

---

##  Regenerating Charts

Requires Python 3.8+ with matplotlib and numpy:

```bash
pip install matplotlib numpy
python cloud_infra_drift_slr/scripts/generate_slr_charts.py
```

Charts are saved to `cloud_infra_drift_slr/images/` at **600 DPI** with a white background, suitable for publication.

| Chart | File |
|---|---|
| PRISMA Flow Diagram | `prisma_flow_diagram.png` |
| Temporal Distribution | `temporal_distribution.png` |
| Study Types | `study_types_distribution.png` |
| Publication Venues | `publication_venues.png` |
| Geographic Distribution | `geographic_distribution.png` |
| Drift Detection Radar | `drift_detection_comparison.png` |
| Remediation Strategies | `remediation_strategies_comparison.png` |
| IaC Tools Comparison | `iac_tools_comparison.png` |
| Thematic Clusters | `thematic_clusters.png` |
| Key Metrics Dashboard | `key_metrics_dashboard.png` |

---

##  Citation

If you use this dataset, visualisations, or review protocol in your work, please cite:

```
Cloud Infrastructure Drift Detection and Remediation in Multi-Cloud Environments:
A Systematic Literature Review (2019–2025).
[Andy Amponsah], [University of Ghana], 2026.
```

---

##  License

The SLR protocol, scripts, and artefacts in this repository are available for academic use.
PDF papers in `43_base_papers/` and `104-paper_for_full_text_review/` retain their original publishers' copyright.
