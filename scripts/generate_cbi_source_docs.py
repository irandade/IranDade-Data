#!/usr/bin/env python3
"""Generate data/source/source_document/cbi_pdfs.json from CBI Resources PDFs."""

import json
import uuid
from pathlib import Path

CBI_DIR = Path("/home/mehdi/irandade/CBI Resources")
OUTPUT = Path("data/source/source_document/cbi_pdfs.json")
PUBLISHER_UID = "019ea734-9bca-75ed-86d9-51d87a860a34"

DATASET_MAP = {
    "Economy Report and Balancesheet":                     "019eb067-6f84-77d0-99a4-0faf38aac851",
    "Namagarhaye Eghtesadi":                                "019eb067-6f84-77d0-99a4-0fb07f1a3c7a",
    "Summary of the country's economic developments":      "019eb067-6f84-77d0-99a4-0fb17513bad2",
    "Consumer Price Index":                                 "019eb060-21db-753d-8903-7b8bfcb82a91",
    "Export Price Index":                                   "019eb060-21db-753d-8903-7b8c4784d336",
    "Housing rental price index in urban areas":            "019eb060-21db-753d-8903-7b8db6d26fcc",
    "Producer Price Index":                                 "019eb060-21db-753d-8903-7b8af94899b2",
    "Household Budget Study":                               "019eb060-21db-753d-8903-7b8eae9c430a",
    "Report on developments in the housing transaction market in Tehran": "019eb067-6f84-77d0-99a4-0fb240c0a53d",
    "Survey of private sector construction activities in urban areas":   "019eb060-21db-753d-8903-7b908312d25a",
    "Quarterly and annual reports":                         "019eb067-6f84-77d0-99a4-0fb36782aafd",
    "Time series of industry indicators":                   "019eb067-6f84-77d0-99a4-0fb49aecf1bd",
    "Uses and recipients of preferential currency":         "019eb067-6f84-77d0-99a4-0fb549a19116",
}


def resolve_dataset(pdf_path: Path) -> str | None:
    for parent in pdf_path.parents:
        if parent.name in DATASET_MAP:
            return DATASET_MAP[parent.name]
    return None


def main():
    pdfs = sorted(CBI_DIR.rglob("*.pdf"))
    records = []

    for pdf in pdfs:
        if "meta data" in pdf.stem.lower():
            continue

        dataset_uid = resolve_dataset(pdf)
        if dataset_uid is None:
            print(f"  ⚠ No dataset match for: {pdf.relative_to(CBI_DIR)}")
            continue

        rel_path = str(pdf.relative_to(CBI_DIR.parent))
        records.append({
            "source_document_uid": str(uuid.uuid7()),
            "created_by": "system",
            "source_type": "PDF",
            "fetched_at": "2024-04-15T10:00:00+03:30",
            "publisher_uid": PUBLISHER_UID,
            "dataset_uid": dataset_uid,
            "os_path": rel_path,
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({"source_document": records}, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 40}")
    print(f"Total PDFs found: {len(pdfs)}")
    print(f"Skipped (meta data): {len(pdfs) - len(records)}")
    print(f"Records written: {len(records)}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
