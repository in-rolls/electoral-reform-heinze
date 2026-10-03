"""Extract and verify the immutable, version-pinned Dataverse download."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def digest(path, algorithm="sha256"):
    return hashlib.new(algorithm, path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()
    archive = ROOT / "sources/dataverse-v1.0-original.zip"
    destination = ROOT / "original"
    with ZipFile(archive) as bundle:
        members = [member for member in bundle.infolist() if not member.is_dir()]
        for member in members:
            path = destination / member.filename
            if not path.resolve().is_relative_to(destination.resolve()):
                raise ValueError(f"Unsafe archive path: {member.filename}")
            if not path.exists():
                bundle.extract(member, destination)
            if path.read_bytes() != bundle.read(member):
                raise ValueError(f"Extracted source changed: {member.filename}")

    metadata = json.loads((ROOT / "sources/dataverse-metadata.json").read_text())
    version = metadata["data"]["latestVersion"]
    assert (version["versionNumber"], version["versionMinorNumber"]) == (1, 0)
    rows = []
    for entry in version["files"]:
        data = entry["dataFile"]
        name = data.get("originalFileName", data["filename"])
        path = destination / entry.get("directoryLabel", "") / name
        assert digest(path, "md5") == data["checksum"]["value"], path
        rows.append(
            {
                "file_id": data["id"],
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "dataverse_md5": data["checksum"]["value"],
                "restricted": entry["restricted"],
            }
        )
    expected = {row["path"].removeprefix("original/") for row in rows}
    actual = {member.filename for member in members}
    assert actual - expected <= {"MANIFEST.TXT"}, actual - expected
    assert not expected - actual
    hash_path = ROOT / "sources/SHA256SUMS"
    source_paths = [
        ROOT / "sources" / name
        for name in (
            "dataverse-v1.0-original.zip",
            "dataverse-metadata.json",
            "paper.pdf",
            "appendix.pdf",
        )
    ]
    checksums = "".join(
        f"{digest(path)}  {path.relative_to(ROOT)}\n" for path in source_paths
    )
    manifest_path = ROOT / "sources/file-manifest.csv"
    if args.initialize:
        if hash_path.exists() or manifest_path.exists():
            raise FileExistsError(
                "Preservation manifests already exist; verify instead"
            )
        hash_path.write_text(checksums)
        with manifest_path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    else:
        assert hash_path.read_text() == checksums, "Source checksum mismatch"
        with manifest_path.open(newline="") as stream:
            recorded = list(csv.DictReader(stream))
        assert recorded == [{k: str(v) for k, v in row.items()} for row in rows]
    print(f"Verified {len(rows)} deposited files, archive bytes, and four sources.")


if __name__ == "__main__":
    main()
