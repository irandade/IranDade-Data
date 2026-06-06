# Iran Dade Service

Data platform for Iranian economic/social indicators. Currently data modeling and seed data only — no application code.

## Source of truth

- `docs/design/Data Model.puml` — **source of truth for schema design** (entities, attributes, enums with codes, relationships)
- `docs/ddl/initialize_db.sql` — DDL derived from PUML
- `schemas/*.schema.json` — 16 JSON Schema (draft-07) files derived from PUML

## Validation

```bash
python3 scripts/validate_meta_data.py
```

Auto-installs `jsonschema` if missing. Validates all `data/meta/<table>/*.json` against `schemas/<table>.schema.json`. Hardcoded skip of `data/meta/measurement_unit/sample.json`.

## Directory layout

- `data/meta/<table>/` — seed data, validated against schemas; may be split across multiple files per table (all validated against same schema)
- `data/basic/` — reference data (geography, calendars), section-based format (`"continents": [...]`), unvalidated
- `schemas/` — JSON Schema per table matching DDL
- `docs/ddl/` — master DDL + seed SQL per directory
- `docs/ddl/geography/` — seed INSERTs for `geography_dimension` (continents, countries, states)
- `docs/ddl/time/` — seed INSERTs for `time_dimension` (Gregorian + Jalali hierarchies, day-level granularity)
- `docs/design/` — PUML diagrams (architecture + data model)

## Conventions

- Root-array format: `{ "tablename": [ ... ] }`
- UUID v7 for all PKs (Python 3.14 `uuid.uuid7()`)
- `created_at` excluded from schemas (DB: `DEFAULT NOW()`)
- `created_by` in schemas with `"default": "system"`
- Enum codes as `VARCHAR(3)`, validated via `"enum": [...]`; PUML uses `Name<CODE>` format
- `"additionalProperties": false` on every schema
- Data field mismatches fixed in data files, not schemas
- DDL uses `VARCHAR(3)` columns for enums, not PostgreSQL ENUM types

## Self-referencing FKs

`geography_dimension`, `time_dimension`, `concept`, `dimension_value`.

## No tests / linting / typechecking

Not yet configured. `pyproject.toml` is minimal.

## Known schema/DDL inconsistencies

| Issue | Detail |
|---|---|
| `concept.alt_name1/2/3` | DDL has `NOT NULL`, schema does NOT require them |
| `currency_exchange_rate` | Exists in PUML but not in DDL or schema |
