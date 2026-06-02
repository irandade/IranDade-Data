# Iran Dade Service

Data platform for Iranian economic/social indicators. Currently data modeling and seed data only — no application code.

## Source of truth

- `docs/ddl/initialize_db.sql` — DDL
- `docs/design/Data Model.puml` — canonical enum codes in `Name<CODE>` format
- `schemas/*.schema.json` — 13 JSON Schema (draft-07) files

## Validation

```bash
python3 scripts/validate_meta_data.py
```

Auto-installs `jsonschema` if missing. Skips `data/meta/measure_kind/sample.json` (hardcoded).

## Directory layout

- `data/meta/<table>/` — seed data, validated against schemas
- `data/basic/` — reference data (geography, calendars), unvalidated
- `schemas/` — JSON Schema per table matching DDL
- `docs/ddl/` — master DDL + seed SQL per directory
- `docs/design/` — PUML diagrams (architecture + data model)

## Conventions

- Root-array format: `{ "tablename": [ ... ] }`
- UUID v7 for all PKs (Python 3.14 `uuid.uuid7()`)
- `created_at` excluded from schemas (DB: `DEFAULT NOW()`)
- `created_by` in schemas with `"default": "system"`
- Enum codes as `VARCHAR(3)`, validated via `"enum": [...]`
- `"additionalProperties": false` on every schema
- Data field mismatches fixed in data files, not schemas
- DDL uses `VARCHAR(3)` columns for enums, not PostgreSQL ENUM types

## Self-referencing FKs

`geography_dimension`, `time_dimension`, `concept`, `dimension_value`.

## No tests / linting / typechecking

Not yet configured. `pyproject.toml` is minimal.

## Missing schema

`indicator_concept_rel` table exists in DDL but has no schema file.
