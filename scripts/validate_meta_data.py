#!/usr/bin/env python3
"""Validate all data/meta_data/ JSON files against schemas/ JSON schemas."""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("Installing jsonschema...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "jsonschema"])
    from jsonschema import validate, ValidationError

DATA_DIR = Path("data/meta")
SCHEMA_DIR = Path("schemas")

schema_cache = {}

def load_schema(key: str) -> dict:
    if key in schema_cache:
        return schema_cache[key]
    schema_path = SCHEMA_DIR / f"{key}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    with open(schema_path) as f:
        schema = json.load(f)
    schema_cache[key] = schema
    return schema

def validate_file(filepath: Path) -> bool:
    with open(filepath) as f:
        data = json.load(f)

    if not isinstance(data, dict) or len(data) != 1:
        print(f"  ✗ Root must be a single-key object (got {type(data).__name__})")
        return False

    key = next(iter(data))
    records = data[key]

    if not isinstance(records, list):
        print(f"  ✗ Value for '{key}' must be an array (got {type(records).__name__})")
        return False

    try:
        schema = load_schema(key)
    except FileNotFoundError as e:
        print(f"  ✗ {e}")
        return False

    all_pass = True
    for i, record in enumerate(records):
        try:
            validate(instance=record, schema=schema)
        except ValidationError as e:
            print(f"  ✗ [{i}] {e.message}")
            all_pass = False

    return all_pass

def main():
    meta_dirs = sorted(DATA_DIR.iterdir())
    total = 0
    passed = 0
    failed = 0

    skip_files = {"data/meta/measurement_unit/sample.json"}

    for subdir in meta_dirs:
        if not subdir.is_dir():
            continue
        for json_file in sorted(subdir.glob("*.json")):
            rel = str(json_file)
            if rel in skip_files:
                print(f"\n{rel}")
                print(f"  - SKIP (user requested)")
                total += 1
                continue
            rel = str(json_file)
            print(f"\n{rel}")
            total += 1
            if validate_file(json_file):
                print(f"  ✓ PASS")
                passed += 1
            else:
                failed += 1

    print(f"\n{'='*40}")
    print(f"Total: {total}  Passed: {passed}  Failed: {failed}")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
