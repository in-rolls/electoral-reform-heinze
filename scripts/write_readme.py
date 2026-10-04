"""Keep the README's numerical tables synchronized with analysis outputs."""

import argparse

from report_utils import ROOT, pct, rows


def update_table(document, name, lines):
    start = f"<!-- generated:{name} -->"
    end = f"<!-- /generated:{name} -->"
    if document.count(start) != 1 or document.count(end) != 1:
        raise ValueError(f"Expected one marker pair for {name}")
    before, rest = document.split(start)
    _, after = rest.split(end)
    return before + start + "\n\n" + "\n".join(lines) + "\n\n" + end + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "README.md"
    original = path.read_text()
    document = original
    means = {r["variable"]: r for r in rows("results/audit/raw-means.csv")}
    cohorts = {
        (r["variable"], r["period"]): r for r in rows("results/audit/cohort-means.csv")
    }
    labels = {
        "most_influential_gd": "President judged most influential",
        "prop_speakingtime_sarpanch": "President speaking share",
        "resignation": "President reports shared tenure",
        "resignation_reported": "Citizen reports shared tenure",
        "sarpanch_uncontested": "President reports unopposed selection",
    }
    table = [
        "| Outcome | Indirect | Direct | Observed councils, indirect / direct |",
        "|---|---:|---:|---:|",
    ]
    for variable in ("most_influential_gd", "prop_speakingtime_sarpanch"):
        result = means[variable]
        table.append(
            f"| {labels[variable]} | {pct(result['indirect_mean'], 1)}% | "
            f"{pct(result['direct_mean'], 1)}% | "
            f"{result['indirect_n']} / {result['direct_n']} |"
        )
    document = update_table(document, "authority", table)
    table = [
        "| Outcome | Early indirect | Direct | Later indirect |",
        "|---|---:|---:|---:|",
    ]
    for variable in ("resignation", "resignation_reported", "sarpanch_uncontested"):
        cells = []
        for period in ("early_indirect", "direct", "late_indirect"):
            result = cohorts[variable, period]
            cells.append(f"{pct(result['mean'], 1)}% ({result['sum']}/{result['n']})")
        table.append(f"| {labels[variable]} | " + " | ".join(cells) + " |")
    document = update_table(document, "cohorts", table)
    table = ["| Early indirect | Direct | Later indirect |", "|---:|---:|---:|"]
    cells = []
    for period in ("early_indirect", "direct", "late_indirect"):
        result = cohorts["avg_prop_land_held_sarpanch_caste", period]
        cells.append(f"{result['n']}/{result['total']} councils observed")
    table.append("| " + " | ".join(cells) + " |")
    document = update_table(document, "land", table)
    if args.check:
        if document != original:
            raise SystemExit("README tables are stale; run make readme")
        print("README numerical tables match analysis outputs.")
    else:
        path.write_text(document)


if __name__ == "__main__":
    main()
