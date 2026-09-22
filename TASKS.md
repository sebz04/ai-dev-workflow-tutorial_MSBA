# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders per FR-1.
- [ ] Total Sales shown formatted as currency (e.g. $116,500)
- [ ] Total Orders shown as a count
- [ ] Values match expected output (~$116,500 / 482 orders)

Commit:

### TASK-4: Sales trend chart
Build the sales-over-time line chart per FR-2.
- [ ] Line chart shows sales over time (daily or monthly granularity)
- [ ] Interactive tooltips display exact values
- [ ] Axes are clearly labeled

Commit:

### TASK-5: Category and region breakdowns
Build the category and region bar charts per FR-3 and FR-4.
- [ ] Category bar chart shows all 5 categories, sorted by sales value descending
- [ ] Region bar chart shows all 4 regions, sorted by sales value descending
- [ ] Both charts have interactive tooltips with exact values

Commit:

### TASK-6: Testing and refinement
Verify the dashboard against the PRD's acceptance criteria and performance targets.
- [ ] Dashboard loads within 5 seconds, charts render within 2 seconds
- [ ] All PRD acceptance criteria verified against sample data
- [ ] Dashboard runs with no errors or warnings

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard for stakeholder review per NFR-5.
- [ ] App deployed and reachable via a public shareable URL
- [ ] Public URL loads correctly in a fresh browser session

Commit:

## In Progress

## Done

### TASK-2: Data loading and basic structure
Load `sales-data.csv` and prepare it for use in the dashboard.
- [x] CSV loads into a Pandas DataFrame without errors
- [x] Date, numeric, and categorical columns have correct dtypes
- [x] Row count and columns match the expected data spec (482 records)

Commit: 00010e6
Notes: The plan's test asserted `date` dtype as the literal string `datetime64[ns]`, but pandas 3.0 (installed in this env) infers `datetime64[us]` by default for `read_csv(parse_dates=...)`. Confirmed via a manual check that this is a pandas-version difference, not a bug — the interface contract only requires `date` to be a datetime column, not nanosecond-specific — so the assertion was changed to `pd.api.types.is_datetime64_any_dtype(...)` instead of forcing `sales_data.py` to fight the library's default resolution.

### TASK-1: Environment setup and project initialization
Set up the project structure, dependencies, and a runnable Streamlit skeleton.
- [x] Project structure created (`app.py`, `data/`, `requirements.txt`)
- [x] Dependencies installed (Streamlit, Plotly, Pandas)
- [x] `streamlit run app.py` launches without errors

Commit: 2bea6b6
Notes: Claude initially overwrote the repo's existing .gitignore with a minimal version; caught via `git status`/`git diff` and reverted before committing, so the original (more complete) .gitignore shipped unchanged.
