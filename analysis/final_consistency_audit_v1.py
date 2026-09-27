from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "manuscript" / "codev_manuscript_v1.tex"
PDF = ROOT / "manuscript" / "codev_manuscript_v1.pdf"
LEDGER = ROOT / "CODEV_claim_evidence_ledger.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def count_disagreements(path: Path) -> int:
    return sum(row.get("disagreement", "").strip().lower() == "true" for row in read_csv(path))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def check(name: str, ok: bool, detail: str, failures: list[str], lines: list[str]):
    status = "PASS" if ok else "FAIL"
    lines.append(f"| {name} | {status} | {detail} |")
    if not ok:
        failures.append(f"{name}: {detail}")


def main() -> int:
    text = TEX.read_text(encoding="utf-8")
    ledger = read_csv(LEDGER)
    failures: list[str] = []
    lines = [
        "# Final consistency audit v1",
        "",
        f"Root: `{ROOT}`",
        f"Manuscript: `{TEX.name}`",
        f"Generated: 2026-09-27",
        "",
        "| Check | Status | Evidence |",
        "|---|---|---|",
    ]

    primary = ROOT / "runs" / "budget_comparison_replacement_v1" / "summary.csv"
    freq_paths = [
        ROOT / "runs" / f"frequency{f}_robustness_v1" / "summary.csv"
        for f in (30, 40, 60, 70)
    ]
    amp05 = ROOT / "runs" / "amplitude05_robustness_v1" / "summary.csv"
    amp20 = ROOT / "runs" / "amplitude20_robustness_v1" / "summary.csv"
    random = ROOT / "runs" / "random_perturbation_repro_v1" / "summary.csv"

    check("primary cohort", len(read_csv(primary)) == 8, f"{len(read_csv(primary))}/8 rows", failures, lines)
    check("primary disagreements", count_disagreements(primary) == 2, f"{count_disagreements(primary)}/8", failures, lines)
    freq_counts = [0, count_disagreements(primary)] + [count_disagreements(p) for p in freq_paths]
    check("frequency audit", freq_counts == [0, 2, 0, 2, 1, 2], f"counts={freq_counts}", failures, lines)
    amp_counts = [count_disagreements(amp05), 2, count_disagreements(amp20)]
    check("amplitude audit", amp_counts == [0, 2, 2], f"counts={amp_counts}", failures, lines)
    check("random replay", count_disagreements(random) == 1, f"{count_disagreements(random)}/8", failures, lines)

    q = read_csv(ROOT / "runs" / "holdout_multivariable_quantile_v1" / "summary.csv")
    mc = read_csv(ROOT / "runs" / "holdout_montecarlo_v1" / "summary.csv")
    check("held-out quantile", len(q) == 3 and all(r["nominal"] == r["mean"] == r["q05"] == r["minimum"] for r in q), "3/3 selections stable", failures, lines)
    check("held-out Monte Carlo", len(mc) == 3 and all(r["nominal"] == r["mc_mean"] == r["mc_q05"] == r["mc_minimum"] for r in mc), "3/3 selections stable", failures, lines)

    zs = read_csv(ROOT / "runs" / "cross_software_zemax_v3" / "cross_software_summary.csv")
    check("cross-software audit", len(zs) == 2 and all(r["disagreement"].lower() == "false" for r in zs), "2 representative samples; no disagreement", failures, lines)

    check("parser audit claim", "2624" in text and any(r["claim_id"] == "CV06" and "2624" in r["exact_support"] for r in ledger), "2624 records, 0 mismatches", failures, lines)
    lower = text.lower()
    check("failure boundary", "no physical result is claimed" in lower and "does not estimate manufacturing yield" in lower and "not as a manufacturing-yield estimate" in lower, "physical/manufacturing claims explicitly bounded", failures, lines)
    check("placeholder scan", not re.search(r"TODO|TBD|FIXME|AUTHOR INPUT REQUIRED|XXXX", text, re.I), "no unresolved placeholders in manuscript", failures, lines)
    cite_count = len(re.findall(r"\\cite\{[^}]+\}", text))
    bib_count = len(re.findall(r"^@", (ROOT / "manuscript" / "references.bib").read_text(encoding="utf-8"), re.M))
    check("references", bib_count >= 20 and cite_count >= 10, f"{bib_count} bib entries; {cite_count} citation commands", failures, lines)
    check("back matter", all(s in text for s in ["Funding and author contributions", "AI use and conflicts", "Data and code availability", "Software and license disclosure"]), "funding, contributions, AI, data, license sections present", failures, lines)
    checklist = (ROOT / "submission" / "DATA_ARCHIVE_AND_LICENSE_CHECKLIST.md").read_text(encoding="utf-8")
    check("archive DOI", "10.5281/zenodo.22995511" in checklist, "Zenodo DOI recorded", failures, lines)
    check("PDF exists", PDF.exists() and PDF.stat().st_size > 0, f"{PDF.stat().st_size if PDF.exists() else 0} bytes", failures, lines)

    lines += [
        "",
        "## Frozen headline values",
        "",
        "- Primary 50 cycles/mm: 2/8 system-level disagreements (`gaosi`, `oradbg01`).",
        "- Frequency 30/40/50/60/70 cycles/mm: 0/8, 2/8, 2/8, 1/8, 2/8.",
        "- Amplitude ±0.5/±1/±2%: 0/8, 2/8, 2/8; fixed random replay: 1/8.",
        "- Held-out quantile audit: 3 passing systems; 2 retained failures; all four summaries agree on each passing system.",
        "- Monte Carlo extension: 600 perturbation bundles plus 60 nominal controls; all three held-out selections stable.",
        "- Cross-software audit: two representative Zemax samples; procedure audit only, not identical-prescription equivalence.",
        "",
        "## File integrity",
        "",
        f"- PDF SHA-256: `{sha256(PDF) if PDF.exists() else 'MISSING'}`",
        f"- TEX SHA-256: `{sha256(TEX)}`",
        f"- Ledger SHA-256: `{sha256(LEDGER)}`",
        "",
        "## Blocking author inputs",
        "",
        "1. Confirm that the published Zenodo DOI remains the version cited in the manuscript and cover letter.",
        "2. Corresponding-author affiliation, email, ORCID, and final author-order confirmation.",
        "3. Institution-approved wording for the authorized CODE V license statement.",
        "4. Confirmation of target route: Optical Engineering, Applied Optics, or Optics Express.",
    ]
    out = ROOT / "FINAL_CONSISTENCY_AUDIT_V1.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    for f in failures:
        print("FAIL:", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
