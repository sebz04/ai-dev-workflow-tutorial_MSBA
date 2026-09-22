# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ShopSmart Streamlit sales dashboard (KPI cards, monthly trend chart, category/region breakdowns) from `data/sales-data.csv`.

**Architecture:** A pure-pandas module (`sales_data.py`) does all loading and aggregation and is unit tested with pytest; a thin Streamlit module (`app.py`) calls into it and only handles layout and Plotly rendering, verified by running the app.

**Tech Stack:** Python 3.11+, Streamlit, Plotly (Express), Pandas, pytest, plain `venv`.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

## Global Constraints

- Work on the existing `feature/sales-dashboard` branch — do not create a worktree or new branch.
- Dependencies via plain `venv/` + `requirements.txt` only — no uv, no conda.
- All calculation logic lives in `sales_data.py` and is covered by pytest tests in `test_sales_data.py`. `app.py` contains no calculation logic and has no unit tests of its own.
- `sales_data.py` does minimal CSV validation: let pandas raise its natural errors. Do not add custom schema-validation code.
- Every commit message includes the relevant milestone ID from `TASKS.md` (TASK-1 through TASK-6).
- TASK-7 (deployment to Streamlit Community Cloud) is **out of scope for this plan**. The plan stops after TASK-6; the user deploys manually from `main` after merge.

---

### Task 1: Environment setup and project initialization *(TASK-1)*

**Files:**
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `app.py`

**Interfaces:**
- Consumes: nothing
- Produces: a runnable `app.py` skeleton (page config + title) that later tasks add sections to

- [ ] **Step 1: Create `requirements.txt`**

```
streamlit
plotly
pandas
pytest
```

- [ ] **Step 2: Create the virtual environment and install dependencies**

Run:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Expected: install completes with no errors.

- [ ] **Step 3: Create `.gitignore`**

```
venv/
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 4: Create the `app.py` skeleton**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 5: Verify the app runs**

Run:
```bash
source venv/bin/activate
streamlit run app.py --server.headless true &
SERVER_PID=$!
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "Dashboard responded OK"
kill $SERVER_PID
```
Expected: prints `Dashboard responded OK`, no traceback in the terminal output.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt .gitignore app.py
git commit -m "TASK-1: set up project environment and app skeleton"
```

---

### Task 2: Data loading and basic structure *(TASK-2)*

**Files:**
- Create: `sales_data.py`
- Create: `test_sales_data.py`

**Interfaces:**
- Consumes: nothing
- Produces: `load_sales_data(path: str) -> pd.DataFrame`, with `date` parsed as a datetime column. Columns: `date, order_id, product, category, region, quantity, unit_price, total_amount`.

- [ ] **Step 1: Write the failing test**

```python
# test_sales_data.py
from sales_data import load_sales_data


def test_load_sales_data_parses_columns_and_dtypes(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n"
        "2024-01-04,ORD-002,Phone Case,Accessories,South,3,24.99,74.97\n"
    )

    df = load_sales_data(str(csv_path))

    assert list(df.columns) == [
        "date", "order_id", "product", "category",
        "region", "quantity", "unit_price", "total_amount",
    ]
    assert len(df) == 2
    assert str(df["date"].dtype) == "datetime64[ns]"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test_sales_data.py -v`
Expected: FAIL with `ImportError` or `ModuleNotFoundError` (`sales_data` / `load_sales_data` doesn't exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# sales_data.py
import pandas as pd


def load_sales_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=["date"])
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test_sales_data.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add sales_data.py test_sales_data.py
git commit -m "TASK-2: load sales data from CSV"
```

---

### Task 3: KPI cards implementation *(TASK-3)*

**Files:**
- Modify: `sales_data.py`
- Modify: `test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data` (Task 2)
- Produces: `get_total_sales(df: pd.DataFrame) -> float`, `get_total_orders(df: pd.DataFrame) -> int`; a KPI row in `app.py`

- [ ] **Step 1: Write the failing tests**

```python
# add to test_sales_data.py
import pandas as pd
from sales_data import get_total_sales, get_total_orders


def _sample_df():
    return pd.DataFrame({
        "total_amount": [159.98, 74.97, 299.99],
    })


def test_get_total_sales_sums_total_amount():
    assert get_total_sales(_sample_df()) == 534.94


def test_get_total_orders_counts_rows():
    assert get_total_orders(_sample_df()) == 3
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest test_sales_data.py -v`
Expected: FAIL with `ImportError` (`get_total_sales`, `get_total_orders` don't exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# add to sales_data.py
def get_total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def get_total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest test_sales_data.py -v`
Expected: PASS (5 tests total)

- [ ] **Step 5: Wire the KPI row into `app.py`**

```python
# app.py — replace the file with:
import streamlit as st

from sales_data import get_total_orders, get_total_sales, load_sales_data

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def load_data():
    return load_sales_data("data/sales-data.csv")


df = load_data()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${get_total_sales(df):,.0f}")
col2.metric("Total Orders", f"{get_total_orders(df):,}")
```

- [ ] **Step 6: Verify the app runs and shows correct values**

Run:
```bash
source venv/bin/activate
streamlit run app.py --server.headless true &
SERVER_PID=$!
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "Dashboard responded OK"
kill $SERVER_PID
```
Expected: prints `Dashboard responded OK`. Open `http://localhost:8501` in a browser during development to confirm Total Sales reads ~$116,500 and Total Orders reads 482 (per the PRD's expected output).

- [ ] **Step 7: Commit**

```bash
git add sales_data.py test_sales_data.py app.py
git commit -m "TASK-3: add Total Sales and Total Orders KPI cards"
```

---

### Task 4: Sales trend chart *(TASK-4)*

**Files:**
- Modify: `sales_data.py`
- Modify: `test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data` (Task 2)
- Produces: `get_monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame` with columns `month` (Timestamp, first-of-month), `total_amount`, sorted chronologically; a trend chart section in `app.py`

- [ ] **Step 1: Write the failing test**

```python
# add to test_sales_data.py
from sales_data import get_monthly_sales_trend


def test_get_monthly_sales_trend_groups_and_sorts_by_month():
    df = pd.DataFrame({
        "date": pd.to_datetime([
            "2024-02-10", "2024-01-05", "2024-01-20",
        ]),
        "total_amount": [5.0, 10.0, 20.0],
    })

    trend = get_monthly_sales_trend(df)

    assert list(trend["month"]) == [
        pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01"),
    ]
    assert list(trend["total_amount"]) == [30.0, 5.0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest test_sales_data.py -v`
Expected: FAIL with `ImportError` (`get_monthly_sales_trend` doesn't exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# add to sales_data.py
def get_monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(month=df["date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)["total_amount"]
        .sum()
        .sort_values("month")
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest test_sales_data.py -v`
Expected: PASS (6 tests total)

- [ ] **Step 5: Wire the trend chart into `app.py`**

```python
# app.py — add near the top:
import plotly.express as px

# app.py — add after the KPI row:
st.subheader("Sales Trend Over Time")
trend = get_monthly_sales_trend(df)
trend_fig = px.line(trend, x="month", y="total_amount", markers=True)
trend_fig.update_layout(xaxis_title="Month", yaxis_title="Total Sales ($)")
st.plotly_chart(trend_fig, use_container_width=True)
```

Also add `get_monthly_sales_trend` to the `from sales_data import ...` line at the top of `app.py`.

- [ ] **Step 6: Verify the app runs**

Run:
```bash
source venv/bin/activate
streamlit run app.py --server.headless true &
SERVER_PID=$!
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "Dashboard responded OK"
kill $SERVER_PID
```
Expected: prints `Dashboard responded OK`. Open `http://localhost:8501` in a browser during development to confirm the line chart shows 12 months of data with hover tooltips.

- [ ] **Step 7: Commit**

```bash
git add sales_data.py test_sales_data.py app.py
git commit -m "TASK-4: add monthly sales trend chart"
```

---

### Task 5: Category and region breakdowns *(TASK-5)*

**Files:**
- Modify: `sales_data.py`
- Modify: `test_sales_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data` (Task 2)
- Produces: `get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame` and `get_region_breakdown(df: pd.DataFrame) -> pd.DataFrame`, both with columns `category`/`region` and `total_amount`, sorted by `total_amount` descending; a breakdown row in `app.py`

- [ ] **Step 1: Write the failing tests**

```python
# add to test_sales_data.py
from sales_data import get_category_breakdown, get_region_breakdown


def test_get_category_breakdown_sums_and_sorts_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Accessories", "Audio", "Wearables"],
        "total_amount": [10.0, 50.0, 20.0, 30.0],
    })

    breakdown = get_category_breakdown(df)

    assert list(breakdown["category"]) == ["Accessories", "Wearables", "Audio"]
    assert list(breakdown["total_amount"]) == [50.0, 30.0, 30.0]


def test_get_region_breakdown_sums_and_sorts_descending():
    df = pd.DataFrame({
        "region": ["North", "South", "North"],
        "total_amount": [40.0, 60.0, 10.0],
    })

    breakdown = get_region_breakdown(df)

    assert list(breakdown["region"]) == ["South", "North"]
    assert list(breakdown["total_amount"]) == [60.0, 50.0]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest test_sales_data.py -v`
Expected: FAIL with `ImportError` (`get_category_breakdown`, `get_region_breakdown` don't exist yet)

- [ ] **Step 3: Write minimal implementation**

```python
# add to sales_data.py
def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def get_region_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest test_sales_data.py -v`
Expected: PASS (8 tests total)

- [ ] **Step 5: Wire the breakdown row into `app.py`**

```python
# app.py — add after the trend chart section:
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    category = get_category_breakdown(df)
    category_fig = px.bar(category, x="category", y="total_amount")
    category_fig.update_layout(xaxis_title="Category", yaxis_title="Total Sales ($)")
    st.plotly_chart(category_fig, use_container_width=True)

with col4:
    st.subheader("Sales by Region")
    region = get_region_breakdown(df)
    region_fig = px.bar(region, x="region", y="total_amount")
    region_fig.update_layout(xaxis_title="Region", yaxis_title="Total Sales ($)")
    st.plotly_chart(region_fig, use_container_width=True)
```

Also add `get_category_breakdown, get_region_breakdown` to the `from sales_data import ...` line at the top of `app.py`.

- [ ] **Step 6: Verify the app runs**

Run:
```bash
source venv/bin/activate
streamlit run app.py --server.headless true &
SERVER_PID=$!
sleep 3
curl -sf http://localhost:8501 > /dev/null && echo "Dashboard responded OK"
kill $SERVER_PID
```
Expected: prints `Dashboard responded OK`. Open `http://localhost:8501` in a browser during development to confirm both bar charts show, sorted descending (Electronics tallest on the category chart), with hover tooltips.

- [ ] **Step 7: Commit**

```bash
git add sales_data.py test_sales_data.py app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

---

### Task 6: Testing and refinement *(TASK-6)*

**Files:**
- Create: `test_sales_data.py` (add one more test, to the existing file)
- No changes expected to `app.py` or `sales_data.py` unless verification below finds a bug

**Interfaces:**
- Consumes: every function from Tasks 2–5, exercised together against the real CSV
- Produces: a smoke test verifying the whole pipeline against the PRD's expected output

- [ ] **Step 1: Write an integration smoke test against the real CSV**

```python
# add to test_sales_data.py
def test_real_csv_matches_prd_expected_output():
    df = load_sales_data("data/sales-data.csv")

    assert get_total_orders(df) == 482
    assert get_total_sales(df) == pytest.approx(116_500, rel=0.02)
    assert get_category_breakdown(df)["category"].iloc[0] == "Electronics"
```

By this task, `test_sales_data.py` already imports `load_sales_data`, `get_total_orders`, `get_total_sales`, and `get_category_breakdown` from earlier tasks — check the top of the file and add any that are missing. Add `import pytest` at the top if it isn't already there.

- [ ] **Step 2: Run the full test suite**

Run: `pytest test_sales_data.py -v`
Expected: PASS (9 tests total). If `test_real_csv_matches_prd_expected_output` fails, check the aggregation logic in `sales_data.py` against the failing assertion before touching anything else — the PRD's expected output is the ground truth here.

- [ ] **Step 3: Run the app and check it against the PRD's performance targets**

Run:
```bash
source venv/bin/activate
time (streamlit run app.py --server.headless true & SERVER_PID=$!; sleep 3; curl -sf http://localhost:8501 > /dev/null; kill $SERVER_PID)
```
Expected: completes in well under 5 seconds (NFR-1). Then open `http://localhost:8501` in a browser and manually walk through `TASKS.md`'s Definition of Done and the PRD's Acceptance Criteria section: KPIs visible, trend chart correct, category/region charts correct and sorted, no errors or warnings in the terminal, professional appearance.

- [ ] **Step 4: Fix any issues found during manual review**

If Step 3 surfaces a problem (wrong sort order, a missing label, an off value), fix it directly in `sales_data.py` or `app.py`, and add a regression test to `test_sales_data.py` if the bug was in a calculation. Re-run Step 2 and Step 3 until both pass cleanly.

- [ ] **Step 5: Commit**

```bash
git add test_sales_data.py
git commit -m "TASK-6: add end-to-end smoke test and verify against PRD acceptance criteria"
```

---

## Hand-off

TASK-7 (deployment to Streamlit Community Cloud) is not part of this plan. Once Task 6 is committed, review the branch, run `/code-review` if desired, merge `feature/sales-dashboard` into `main`, and deploy from `main` yourself.
