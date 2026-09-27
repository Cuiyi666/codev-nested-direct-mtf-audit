from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "MANIFEST_SHA256.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    files = [p for p in ROOT.rglob("*") if p.is_file() and p.name != OUT.name]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path", "bytes", "sha256"])
        for p in sorted(files):
            w.writerow([p.relative_to(ROOT).as_posix(), p.stat().st_size, sha256(p)])
    print(f"wrote {len(files)} entries to {OUT}")


if __name__ == "__main__":
    main()

