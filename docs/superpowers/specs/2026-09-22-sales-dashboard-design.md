# Design: E-Commerce Sales Dashboard

Source PRD: `prd/ecommerce-analytics.md`
Milestone tracker: `TASKS.md` (TASK-1 through TASK-7)

## Overview

A single-page Streamlit dashboard reading `data/sales-data.csv` that shows two KPI cards (Total Sales, Total Orders), a monthly sales trend line chart, and category/region bar charts, per Phase 1 of the PRD (FR-1 through FR-5).

## Decisions locked in during brainstorming

- **Trend granularity: monthly.** 12 points, matches the PRD's own mockup, avoids a noisy ~40-point daily line.
- **Module split: two modules.** `sales_data.py` (data loading + aggregations, pytest-tested) and `app.py` (Streamlit layout + Plotly calls, verified by running the app). No separate `charts.py` — the app is small enough that a third module would be over-splitting.
- **CSV validation: minimal.** The CSV is a fixed, known-good sample file. `sales_data.py` lets pandas raise its natural errors (missing file, bad dtypes) rather than adding custom schema-validation code and error classes.
- **Ground rules (from the original request):** work on the existing `feature/sales-dashboard` branch (no worktree), plain `venv/` + `requirements.txt` (no uv/conda), data calculations isolated in their own tested module, code kept simple and readable, deployment is a final hand-off step the user runs manually after merging to `main`.

## Project structure

```
├── app.py                  # Streamlit entry point (layout, KPI cards, Plotly charts)
├── sales_data.py           # CSV loading + aggregations (pure functions, unit tested)
├── test_sales_data.py      # pytest tests for sales_data.py
├── requirements.txt        # streamlit, plotly, pandas, pytest
├── venv/                   # plain venv, gitignored
├── data/sales-data.csv     # already exists
└── .gitignore              # venv/, __pycache__/, etc.
```

`sales_data.py` owns every pandas operation. Each function takes/returns plain data (a DataFrame or a scalar) and imports neither Streamlit nor Plotly, which is what makes it testable in isolation. `app.py` imports `sales_data.py`, calls its functions, and is responsible only for layout and rendering — no calculation logic lives there, so it has no unit tests; it's verified by running the app per the Definition of Done in `TASKS.md`.

## `sales_data.py`: functions

| Function | Signature | Returns |
|---|---|---|
| `load_sales_data` | `(path: str) -> pd.DataFrame` | Raw CSV loaded with `date` parsed as a datetime column and numeric columns as floats/ints |
| `get_total_sales` | `(df: pd.DataFrame) -> float` | Sum of `total_amount` |
| `get_total_orders` | `(df: pd.DataFrame) -> int` | Row count (one row per order) |
| `get_monthly_sales_trend` | `(df: pd.DataFrame) -> pd.DataFrame` | Columns `month`, `total_amount`; one row per calendar month, sorted chronologically |
| `get_category_breakdown` | `(df: pd.DataFrame) -> pd.DataFrame` | Columns `category`, `total_amount`; one row per category, sorted by `total_amount` descending |
| `get_region_breakdown` | `(df: pd.DataFrame) -> pd.DataFrame` | Columns `region`, `total_amount`; one row per region, sorted by `total_amount` descending |

All five aggregation functions take an already-loaded DataFrame (not a file path), so tests can build a small in-memory DataFrame fixture instead of depending on the real CSV.

## `app.py`: layout

1. `st.set_page_config` — wide layout, page title "ShopSmart Sales Dashboard".
2. Load data once via `load_sales_data`, wrapped in `st.cache_data` so re-running the script on interaction doesn't re-read the CSV.
3. KPI row: `st.columns(2)`, each using `st.metric` — Total Sales formatted as `$X,XXX,XXX`, Total Orders formatted with a thousands separator.
4. Trend section: `st.plotly_chart` with a Plotly Express line chart built from `get_monthly_sales_trend`, hover tooltips showing exact values.
5. Breakdown row: `st.columns(2)` — Plotly Express bar charts from `get_category_breakdown` and `get_region_breakdown`, both pre-sorted descending, hover tooltips with exact values.
6. Colors and chart styling follow the `dataviz` skill's palette guidance for a consistent, accessible look, applied at implementation time.

## Testing strategy

`test_sales_data.py` covers `sales_data.py` only, using a small hand-built DataFrame fixture (a handful of rows spanning 2+ months, 2+ categories, 2+ regions) rather than the full 482-row CSV, so tests stay fast and their expected values are easy to hand-verify:

- `get_total_sales` sums correctly
- `get_total_orders` counts rows correctly
- `get_monthly_sales_trend` groups by month, sums per month, and sorts chronologically
- `get_category_breakdown` groups by category, sums correctly, and sorts descending
- `get_region_breakdown` groups by region, sums correctly, and sorts descending

`app.py` is verified manually by running `streamlit run app.py` and checking it against `TASKS.md`'s acceptance criteria and the PRD's expected output (~$116,500 total sales, 482 orders, Electronics as top category) — this is what each milestone's Definition of Done checks.

## Milestone mapping (`TASKS.md`)

| Milestone | Design component |
|---|---|
| TASK-1 | Project structure, `venv/`, `requirements.txt`, blank `app.py` skeleton |
| TASK-2 | `load_sales_data` in `sales_data.py` |
| TASK-3 | `get_total_sales`, `get_total_orders` + KPI row in `app.py` |
| TASK-4 | `get_monthly_sales_trend` + trend chart in `app.py` |
| TASK-5 | `get_category_breakdown`, `get_region_breakdown` + breakdown row in `app.py` |
| TASK-6 | Full pytest suite for `sales_data.py`, manual verification against PRD acceptance criteria and performance targets |
| TASK-7 | Deployment to Streamlit Community Cloud — **out of scope for the implementation plan**, executed manually by the user from `main` after merge |

## Out of scope (per PRD Phase 2)

User authentication, database integration, export, alerts, filtering/date range selection, drill-down, mobile-responsive design.
