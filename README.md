# Nested direct-MTF decision audit (CODE V study)

This repository contains the public-safe analysis companion for:

> *Frequency- and Perturbation-Dependent Design Decisions from Nested Direct-MTF Evaluation: An Independent CODE V Study*

The study compares a nominal direct-MTF ranking rule with a nested perturbation-aware rule under a frozen equal-cost contract. The headline evidence is deliberately bounded to an eight-system CODE V cohort, three passing held-out systems, two retained screening failures, and a representative—not identical-prescription—Zemax procedure audit.

## Contents

- `analysis/` — author-written score parsing, public measured-data analysis, consistency audit, and manifest utilities.
- `protocols/` — frozen comparison, held-out, Monte Carlo, cross-software, and physical-validation protocols.
- `data/derived/` — license-cleared aggregate CSVs and the claim–evidence ledger. Proprietary native reports and prescriptions are not included.
- `figures/` — the decision heatmap used in the manuscript.
- `CITATION.cff` — citation metadata, including Yi Cui's ORCID.

## Reproducibility boundary

The CODE V and Zemax executables, license keys, commercial/library prescriptions, source lens files, and any native reports not cleared for redistribution are intentionally excluded. The automation scripts that require a licensed optical-design installation are retained in the private evidence archive; this public repository contains the parser and derived-analysis layer only. No manufacturing yield or physical as-built result is claimed.

## Running the public analysis

The parser and summary scripts use Python 3 and standard-library modules where possible. The public measured-data script additionally requires `openpyxl` and a separately obtained, license-compatible source workbook. The result CSVs in `data/derived/` are the frozen outputs used for manuscript checking.

The parser audit operates on the private evidence archive when that archive is available:

```text
python analysis/audit_mtf_score_parser_v1.py --evidence-root /path/to/private-evidence-root
```

The measured-data summary writes only derived outputs and does not redistribute the source workbook:

```text
python analysis/analyze_public_measured_mtf_v1.py /path/to/cleared.xlsx --out-dir data/derived
```

The scripts contain no workstation-specific paths. The private evidence archive remains the authority for licensed CODE V runs and native reports.

## License

The code/data license is intentionally pending author confirmation. Do not assume permission to redistribute proprietary optical files or vendor reports from this repository.

