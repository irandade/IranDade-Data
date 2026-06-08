import json
from pathlib import Path
from jsonschema import validate, ValidationError
from rich.console import Console
from rich.markup import escape

DATA_DIR = Path("data/meta")
SCHEMA_DIR = Path("schemas")
SKIP_FILES: set[str] = set()

console = Console()
schema_cache: dict[str, dict] = {}


def load_schema(key: str) -> dict | None:
    if key in schema_cache:
        return schema_cache[key]
    schema_path = SCHEMA_DIR / f"{key}.schema.json"
    if not schema_path.exists():
        console.print(f"  [red]✗ Schema not found: {schema_path}[/red]")
        return None
    with open(schema_path) as f:
        schema = json.load(f)
    schema_cache[key] = schema
    return schema


def validate_file(filepath: Path) -> bool:
    with open(filepath) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            console.print(f"  [red]✗ Invalid JSON: {e}[/red]")
            return False

    if not isinstance(data, dict) or len(data) != 1:
        console.print(f"  [red]✗ Root must be a single-key object (got {type(data).__name__})[/red]")
        return False

    key = next(iter(data))
    records = data[key]

    if not isinstance(records, list):
        console.print(f"  [red]✗ Value for '{key}' must be an array (got {type(records).__name__})[/red]")
        return False

    schema = load_schema(key)
    if schema is None:
        return False

    all_pass = True
    for i, record in enumerate(records):
        try:
            validate(instance=record, schema=schema)
        except ValidationError as e:
            console.print(f"  [red]✗ [{i}] {escape(e.message)}[/red]")
            all_pass = False

    return all_pass


def run_meta_validation() -> bool:
    meta_dirs = sorted(DATA_DIR.iterdir())
    total = passed = failed = 0

    for subdir in meta_dirs:
        if not subdir.is_dir():
            continue
        for json_file in sorted(subdir.glob("*.json")):
            rel = str(json_file)
            total += 1
            console.print(f"\n{rel}")
            if rel in SKIP_FILES:
                console.print(f"  [yellow]- SKIP (user requested)[/yellow]")
                continue
            if validate_file(json_file):
                console.print(f"  [green]✓ PASS[/green]")
                passed += 1
            else:
                failed += 1

    console.print(f"\n{'=' * 40}")
    console.print(f"Total: {total}  Passed: {passed}  Failed: {failed}")
    return failed == 0
