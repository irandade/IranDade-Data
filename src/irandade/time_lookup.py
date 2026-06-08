import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

CAL_DIR = Path("data/basic")
console = Console()


def lookup_and_show(calendar: str, year: int, month: int | None = None, day: int | None = None):
    # 1. Load queried calendar JSON
    try:
        with open(CAL_DIR / f"{calendar}_calendar.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        console.print(f"[red]{calendar}_calendar.json not found[/red]")
        return

    # 2. Look up hierarchy records by numeric fields
    century_num = year // 100
    century_rec = next((c for c in data["centuries"] if c["century"] == century_num), None)
    year_rec = next((y for y in data["years"] if y["year"] == year), None)
    month_rec = next((m for m in data["months"] if m["year"] == year and m["month"] == month), None) if month is not None else None

    # 3. Build title
    parts = [str(year)]
    if month is not None:
        parts.append(f"{month:02d}")
    if day is not None:
        parts.append(f"{day:02d}")
    title = f"{calendar.title()} — {'/'.join(parts)}"

    table = Table(title=title)
    table.add_column("UUID", style="dim")
    table.add_column("Gregorian", style="blue")
    table.add_column("Jalali", style="magenta")

    def row(rec):
        if calendar == "gregorian":
            return [rec["uid"] if rec else "—", rec["name"] if rec else "—", "—"]
        else:
            return [rec["uid"] if rec else "—", "—", rec["name"] if rec else "—"]

    table.add_row(*row(century_rec))
    table.add_row(*row(year_rec))
    if month is not None:
        table.add_row(*row(month_rec))

    # 4. Day record (only if day is given)
    if day is not None:
        try:
            with open(CAL_DIR / "days_calendar.json") as f:
                days_data = json.load(f)
        except FileNotFoundError:
            console.print("[red]days_calendar.json not found[/red]")
            return

        if calendar == "gregorian":
            day_rec = next(
                (d for d in days_data["days"]
                 if d["grg_year"] == year and d["grg_month"] == month and d["grg_day"] == day),
                None
            )
        else:
            jal_day_str = f"{year}-{month:02d}-{day:02d}"
            day_rec = next(
                (d for d in days_data["days"] if d["jal_name"] == jal_day_str), None
            )

        if not day_rec:
            console.print("[red]Day not found[/red]")
            return

        table.add_row(day_rec["day_dimension_uid"], day_rec["grg_name"], day_rec["jal_name"])

    console.print(table)
