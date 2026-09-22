# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

## In Progress

## Done

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the dashboard for stakeholder review per NFR-5.
- [x] App deployed and reachable via a public shareable URL
- [x] Public URL loads correctly in a fresh browser session

URL: https://ai-dev-workflow-tutorialmsba-ztzdaoy2wrupsunsfjkpbk.streamlit.app/

Commit: N/A (manual deployment via the Streamlit Community Cloud UI; no code commit)
Notes: Deployed from `main` — a manual step that can't be scripted, since it requires the user's GitHub-authenticated browser session. User confirmed the URL loads correctly in a fresh browser session.

### TASK-6: Testing and refinement
Verify the dashboard against the PRD's acceptance criteria and performance targets.
- [x] Dashboard loads within 5 seconds, charts render within 2 seconds
- [x] All PRD acceptance criteria verified against sample data
- [x] Dashboard runs with no errors or warnings

Commit: fb8d528
Notes: Added the integration smoke test against the real CSV (482 orders, ~$116,500 total sales, Electronics as top category) — all 7 tests pass. Walked the PRD's Acceptance Criteria section item by item; no bugs found, so no code changes were needed beyond the test. One gap: the Claude in Chrome extension wasn't connected this session, so "professional appearance" and exact chart-render timing were checked via the terminal (clean `streamlit run` log, response returned well inside the 3s startup window) and code review (wide layout, titled sections, `st.metric` KPIs) rather than an actual rendered screenshot — worth a quick manual look in a browser before merging.

### TASK-5: Category and region breakdowns
Build the category and region bar charts per FR-3 and FR-4.
- [x] Category bar chart shows all 5 categories, sorted by sales value descending
- [x] Region bar chart shows all 4 regions, sorted by sales value descending
- [x] Both charts have interactive tooltips with exact values

Commit: 0738530
Notes: The plan's `get_category_breakdown` test used sample data where two categories summed to an exact tie (30.0), and asserted a specific tie-break order. The PRD (FR-3/FR-4) only requires descending sort by value, with no tie-break rule, and pandas' groupby+sort_values doesn't produce the order the test assumed. Confirmed this was an unintentional tie in the plan's sample data, not an implementation bug, so the test's input values were adjusted to remove the tie rather than adding tie-break logic the PRD doesn't ask for.

### TASK-4: Sales trend chart
Build the sales-over-time line chart per FR-2.
- [x] Line chart shows sales over time (daily or monthly granularity)
- [x] Interactive tooltips display exact values
- [x] Axes are clearly labeled

Commit: 1f09238
Notes: clean

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders per FR-1.
- [x] Total Sales shown formatted as currency (e.g. $116,500)
- [x] Total Orders shown as a count
- [x] Values match expected output (~$116,500 / 482 orders)

Commit: e82fd1e
Notes: clean

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
