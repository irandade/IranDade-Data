import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

META_DIR = Path("data/meta")
LEVEL_LABELS = {"CLS": "Cluster", "DOM": "Domain", "SDO": "Subdomain", "TOP": "Topic"}

console = Console()


def _load_all(table: str) -> list[dict]:
    records = []
    for f in sorted((META_DIR / table).glob("*.json")):
        with open(f) as fp:
            data = json.load(fp)
        records.extend(data.get(table, []))
    return records


def show_concepts():
    records = _load_all("concept")
    if not records:
        console.print("[yellow]No concepts found[/yellow]")
        return
    table = Table(title="Concepts")
    table.add_column("Name", style="cyan")
    table.add_column("English", style="green")
    table.add_column("Level", style="magenta")
    table.add_column("Description")
    for r in records:
        level_code = r.get("level_type", "")
        level_label = LEVEL_LABELS.get(level_code, level_code)
        table.add_row(
            r.get("name", ""),
            r.get("alt_name1", ""),
            level_label,
            r.get("description", "") or "",
        )
    console.print(table)


def show_measurement_units():
    records = _load_all("measurement_unit")
    if not records:
        console.print("[yellow]No measurement units found[/yellow]")
        return
    table = Table(title="Measurement Units")
    table.add_column("Name", style="cyan")
    table.add_column("Alt Name", style="green")
    table.add_column("Type", style="magenta")
    table.add_column("Coefficient", justify="right")
    table.add_column("Base Year", justify="right")
    for r in records:
        table.add_row(
            r.get("name", ""),
            r.get("alt_name", ""),
            r.get("unit_type", ""),
            str(r.get("unit_coefficient", "")),
            str(r.get("base_year", "")),
        )
    console.print(table)


def show_dimensions():
    classes = _load_all("dimension_class")
    if classes:
        class_by_uid = {r["dimension_class_uid"]: r["name"] for r in classes}
        table = Table(title="Dimension Classes")
        table.add_column("Name", style="cyan")
        table.add_column("Persian", style="green")
        table.add_column("Description")
        for r in classes:
            table.add_row(r.get("name", ""), r.get("alt_name1", ""), r.get("description", ""))
        console.print(table)

    values = _load_all("dimension_value")
    if values:
        table = Table(title="Dimension Values")
        table.add_column("Name", style="cyan")
        table.add_column("Persian", style="green")
        table.add_column("Class", style="magenta")
        for r in values:
            class_name = class_by_uid.get(r.get("dimension_class_uid", ""), "")
            table.add_row(
                r.get("name", ""),
                r.get("alt_name1", ""),
                class_name,
            )
        console.print(table)
