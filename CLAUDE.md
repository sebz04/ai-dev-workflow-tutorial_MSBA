# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A student tutorial project: a Streamlit e-commerce sales dashboard, built to teach a spec-driven
agentic workflow (PRD → `TASKS.md` → Superpowers brainstorming/writing-plans/executing-plans →
commit → push → review → deploy). The dashboard itself (`app.py`, `sales_data.py`) is the smaller
part of the repo; `TASKS.md`, `prd/ecommerce-analytics.md`, and `docs/superpowers/` are the
process artifacts the workflow produces and are as load-bearing as the code.

The top-level `.md` files (`pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`,
`capstone-tools.md`) are the tutorial's own instructional content for the student, not developer
docs — don't treat them as project documentation to keep in sync with the code.

## Commands

```bash
# Environment (plain venv only — no uv/conda/poetry)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Run the full test suite
pytest test_sales_data.py -v

# Run a single test
pytest test_sales_data.py::test_get_total_sales_sums_total_amount -v
```

There is no linter or type checker configured in this repo.

## Architecture

Two-module split, deliberately kept this small (see
`docs/superpowers/specs/2026-09-22-sales-dashboard-design.md` for the full rationale):

- **`sales_data.py`** — every pandas operation lives here as pure functions (DataFrame/scalar in,
  DataFrame/scalar out). Imports neither Streamlit nor Plotly, which is what makes it unit-testable
  in isolation. This is the only file `test_sales_data.py` covers.
- **`app.py`** — Streamlit layout and Plotly rendering only. Calls into `sales_data.py` for all
  calculations; contains no aggregation logic of its own and has no unit tests. It's verified by
  running the app and checking it against `TASKS.md`'s Definition of Done, not by pytest.

Do not add calculation logic to `app.py`, and do not add Streamlit/Plotly imports to
`sales_data.py` — that split is intentional and is what the tests depend on.

CSV validation is intentionally minimal: `load_sales_data` lets pandas raise its own errors
(missing file, bad dtypes) rather than adding custom schema-validation code. `data/sales-data.csv`
is a fixed, known-good sample file, not user-uploaded input.

### Testing convention

`test_sales_data.py` builds small hand-written DataFrame fixtures per test (a handful of rows) so
expected values are easy to hand-verify, rather than exercising the full 482-row CSV in every test.
One exception: `test_real_csv_matches_prd_expected_output` is an integration smoke test that loads
the real `data/sales-data.csv` and checks it against the PRD's expected output (~$116,500 total
sales, 482 orders, Electronics as the top category) — treat that test's assertions as ground truth
if `sales_data.py`'s aggregation logic is ever in question.

## The workflow this repo follows

Work is tracked in `TASKS.md` as milestones (`TASK-1` … `TASK-7`), each with checkbox acceptance
criteria pulled from `prd/ecommerce-analytics.md`. Every commit that completes a milestone includes
that milestone ID in the commit message (e.g. `TASK-3: add Total Sales and Total Orders KPI
cards`), which is what makes `git log` traceable back to a requirement.

`docs/superpowers/plans/` and `docs/superpowers/specs/` hold the design doc and implementation plan
produced by the Superpowers `brainstorming` and `writing-plans` skills before code was written —
consult the plan there before assuming a design decision (e.g. monthly vs. daily trend granularity,
the two-module split) is up for reconsideration; it was already made deliberately.

TASK-7 (deployment to Streamlit Community Cloud) is explicitly out of scope for the implementation
plan and is a manual step the user runs themselves from `main` after merge — Streamlit Cloud
deployment requires the user's own GitHub-authenticated browser session and cannot be scripted from
this repo.

## Lessons

Distilled from the "Notes" lines on completed milestones in `TASKS.md`:

- **Don't assert exact pandas dtype strings.** A plan's test asserted `str(df["date"].dtype) ==
  "datetime64[ns]"`, but pandas 3.0 infers `datetime64[us]` by default for
  `read_csv(parse_dates=...)`. Use `pd.api.types.is_datetime64_any_dtype(...)` (or similar type
  predicates) instead of literal dtype strings — the interface contract is "this column is a
  datetime," not a specific resolution, and pinning the literal string makes tests break on pandas
  version differences that aren't real bugs.
- **An unintentional tie in test fixture data is a fixture bug, not a spec gap.** When a sort-order
  test's sample data produces an exact tie and the PRD specifies no tie-break rule, fix the
  fixture's input values to remove the tie rather than inventing tie-break logic the spec doesn't
  require.
- **Terminal/log verification isn't a substitute for looking at the rendered app.** Checking a
  clean `streamlit run` log and reading the layout code isn't sufficient for UX-shaped acceptance
  criteria like "professional appearance" or perceived chart-render speed — do an actual manual
  browser check before merging when those criteria are in play.
- **Never regenerate `.gitignore` from scratch in an existing repo.** Scaffolding a new project
  structure previously overwrote this repo's existing, more complete `.gitignore` with a minimal
  generated one. Check `git status`/`git diff` before committing scaffolding changes, and extend an
  existing `.gitignore` rather than replacing it.
