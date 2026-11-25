#!/usr/bin/env python3
"""hol: byte-safe single-line entry exporter."""

import json
import os
from pathlib import Path

HARD_CAP = 160
SRC = "entry.txt"


def decode_best(blob):
    return blob.decode("utf-8", errors="strict")


def export_line():
    my_dir = Path(__file__).resolve().parent
    src_path = my_dir / SRC
    if not src_path.is_file():
        print(json.dumps({"exported": False, "why": f"{SRC} absent"}))
        return 3
    text = decode_best(src_path.read_bytes())
    chosen = ""
    for one in text.replace("\r\n", "\n").split("\n"):
        if one.strip():
            chosen = one
            break
    span = len(chosen)
    if span < 1 or span > HARD_CAP:
        print(json.dumps({"exported": False, "span": span, "cap": HARD_CAP}))
        return 1
    landing = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    landing.mkdir(parents=True, exist_ok=True)
    (landing / SRC).write_text(chosen, encoding="utf-8", newline="\n")
    print(json.dumps({"exported": True, "span": span, "cap": HARD_CAP}))
    return 0


if __name__ == "__main__":
    raise SystemExit(export_line())
