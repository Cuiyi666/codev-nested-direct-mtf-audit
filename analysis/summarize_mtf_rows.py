from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "runs" / "baseline_v2_ascii_source"
OUT = IN_DIR / "mtf_50_rows.csv"


def main() -> None:
    rows = []
    for path in sorted(IN_DIR.glob("*_mtf.txt")):
        lens = path.stem.removesuffix("_mtf")
        field = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.search(r"FIELD\s+(\d+)\s+\(ANG\)", line)
            if m:
                field = int(m.group(1))
                continue
            m = re.match(r"^\s*50\s+(.+?)\s*$", line)
            if m and field is not None:
                rows.append({"lens": lens, "field": field, "frequency_l_mm": 50, "raw_row": m.group(1)})
    with OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["lens", "field", "frequency_l_mm", "raw_row"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")


if __name__ == "__main__":
    main()

