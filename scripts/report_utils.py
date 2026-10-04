"""Shared readers and formatting for reports generated from analysis outputs."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def pct(value, digits=2):
    return f"{100 * float(value):.{digits}f}"
