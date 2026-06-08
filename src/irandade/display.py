import json
from pathlib import Path
from rich.cells import cell_len
from rich.console import Console
from rich.table import Table

META_DIR = Path("data/meta")
LEVEL_LABELS = {"CLS": "Cluster", "DOM": "Domain", "SDO": "Subdomain", "TOP": "Topic"}

console = Console()


def _wrap_cell(text: str, max_width: int = 32, max_lines: int = 4) -> str:
    words = text.split()
    if not words:
        return ""
    lines = []
    cur = words[0]
    for word in words[1:]:
        candidate = cur + " " + word
        if cell_len(candidate) <= max_width:
            cur = candidate
        else:
            lines.append(cur)
            if len(lines) >= max_lines:
                lines[-1] += " ..."
                return "\n".join(lines)
            cur = word
    lines.append(cur)
    return "\n".join(lines)


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
    name_by_uid = {r.get("concept_uid", ""): r.get("name", "") for r in records}
    table = Table(title="Concepts")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("English", style="green")
    table.add_column("Level", style="magenta")
    table.add_column("Parent", style="yellow")
    table.add_column("Description")
    for r in records:
        level_code = r.get("level_type", "")
        level_label = LEVEL_LABELS.get(level_code, level_code)
        table.add_row(
            _wrap_cell(r.get("concept_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("alt_name1", "")),
            _wrap_cell(level_label),
            _wrap_cell(name_by_uid.get(r.get("parent_concept_uid", ""), "")),
            _wrap_cell(r.get("description", "") or ""),
        )
    console.print(table)


def show_measurement_units():
    records = _load_all("measurement_unit")
    if not records:
        console.print("[yellow]No measurement units found[/yellow]")
        return
    table = Table(title="Measurement Units")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("Alt Name", style="green")
    table.add_column("Type", style="magenta")
    table.add_column("Coefficient", justify="right")
    table.add_column("Base Year", justify="right")
    for r in records:
        table.add_row(
            _wrap_cell(r.get("measurement_unit_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("alt_name", "")),
            _wrap_cell(r.get("unit_type", "")),
            str(r.get("unit_coefficient", "")),
            str(r.get("base_year", "")),
        )
    console.print(table)


def _concept_path(concept_uid: str, concepts: list[dict]) -> str:
    by_uid = {r["concept_uid"]: r for r in concepts}
    parts = []
    uid = concept_uid
    while uid in by_uid:
        c = by_uid[uid]
        parts.append(c["name"])
        uid = c.get("parent_concept_uid", "")
    return " > ".join(reversed(parts))


def show_indicator():
    records = _load_all("indicator")
    if not records:
        console.print("[yellow]No indicators found[/yellow]")
        return
    concepts = _load_all("concept")
    table = Table(title="Indicators")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Topic Concept", style="yellow")
    for r in records:
        table.add_row(
            _wrap_cell(r.get("indicator_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("description", "") or ""),
            _wrap_cell(_concept_path(r.get("concept_uid", ""), concepts)),
        )
    console.print(table)


def show_series():
    records = _load_all("series")
    if not records:
        console.print("[yellow]No series found[/yellow]")
        return
    indicators = _load_all("indicator")
    indicator_by_uid = {r.get("indicator_uid", ""): r.get("name", "") for r in indicators}
    units = _load_all("measurement_unit")
    unit_by_uid = {r.get("measurement_unit_uid", ""): r.get("name", "") for r in units}
    FORMALITY_LABELS = {"FRM": "Formal", "SFM": "Semiformal", "INF": "Informal", "MIX": "Mixed"}
    TIME_GRAIN_LABELS = {"CEN": "Century", "YEA": "Year", "MON": "Month", "QRT": "Quarter", "WEE": "Week", "DAY": "Day"}
    table = Table(title="Series")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    table.add_column("Formality", style="magenta")
    table.add_column("Grain", style="magenta")
    table.add_column("Indicator", style="yellow")
    table.add_column("Unit", style="green")
    for r in records:
        table.add_row(
            _wrap_cell(r.get("series_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("description", "") or ""),
            _wrap_cell(FORMALITY_LABELS.get(r.get("formality_type", ""), r.get("formality_type", ""))),
            _wrap_cell(TIME_GRAIN_LABELS.get(r.get("time_dimension_type", ""), r.get("time_dimension_type", ""))),
            _wrap_cell(indicator_by_uid.get(r.get("indicator_uid", ""), "")),
            _wrap_cell(unit_by_uid.get(r.get("measurement_unit_uid", ""), "")),
        )
    console.print(table)


def show_dimensions():
    classes = _load_all("dimension_class")
    if not classes:
        console.print("[yellow]No dimension classes found[/yellow]")
        return
    class_by_uid = {r.get("dimension_class_uid", ""): r.get("name", "") for r in classes}
    table = Table(title="Dimension Classes")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("Persian", style="green")
    table.add_column("Description")
    for r in classes:
        table.add_row(
            _wrap_cell(r.get("dimension_class_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("alt_name1", "")),
            _wrap_cell(r.get("description", "")),
        )
    console.print(table)

    values = _load_all("dimension_value")
    if not values:
        console.print("[yellow]No dimension values found[/yellow]")
        return
    table = Table(title="Dimension Values")
    table.add_column("UUID")
    table.add_column("Name", style="cyan")
    table.add_column("Persian", style="green")
    table.add_column("Class", style="magenta")
    for r in values:
        class_name = class_by_uid.get(r.get("dimension_class_uid", ""), "")
        table.add_row(
            _wrap_cell(r.get("dimension_value_uid", "")[-12:]),
            _wrap_cell(r.get("name", "")),
            _wrap_cell(r.get("alt_name1", "")),
            _wrap_cell(class_name),
        )
    console.print(table)
