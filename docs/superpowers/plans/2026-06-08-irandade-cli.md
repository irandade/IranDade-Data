# Iran Dade CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI tool with typer + rich for validating meta data and displaying seed data.

**Architecture:** Single package `src/irandade/` with three modules: `cli.py` (typer commands), `validator.py` (validate logic), `display.py` (rich table rendering). Invoked via `uv run python -m irandade`.

**Tech Stack:** Python 3.12+, typer, rich, jsonschema

---

### Task 1: Initialize package structure

**Files:**
- Create: `src/irandade/__init__.py`
- Create: `src/irandade/__main__.py`
- Modify: `pyproject.toml`

- [ ] **Step 1: Create `src/irandade/__init__.py`** — empty file
- [ ] **Step 2: Create `src/irandade/__main__.py`** — entry point that calls `cli.app()`
- [ ] **Step 3: Update `pyproject.toml`** — add dependencies and update project name

### Task 2: Implement CLI structure

**Files:**
- Create: `src/irandade/cli.py`

- [ ] **Step 1: Create typer app with validate and show groups**
- [ ] **Step 2: Add validate subcommands (meta, data)**
- [ ] **Step 3: Add show subcommands (concept, measure, dimension)**
- [ ] **Step 4: Add short alias subcommands (v, s, m, d, c)**

### Task 3: Implement validator

**Files:**
- Create: `src/irandade/validator.py`

- [ ] **Step 1: Implement full validator** — reimplements `scripts/validate_meta_data.py` with rich output

### Task 4: Implement display module

**Files:**
- Create: `src/irandade/display.py`

- [ ] **Step 1: Implement helper to load records from data/meta/<table>/**
- [ ] **Step 2: Implement show_concepts() with level_type legend**
- [ ] **Step 3: Implement show_measurement_units()**
- [ ] **Step 4: Implement show_dimensions() with class name lookup**
- [ ] **Step 5: Verify -- uv run python -m irandade show concept works**
