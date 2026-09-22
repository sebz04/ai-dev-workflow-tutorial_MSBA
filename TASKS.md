# Tasks

This file tracks all work for the ShopSmart e-commerce analytics dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

- Acceptance criteria for the milestone are met
- App runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message

## To Do

### TASK-2: Data loading and basic structure
Load `sales-data.csv` and prepare it for use in the dashboard.
- [ ] CSV loads into a Pandas DataFrame without errors
- [ ] Date, numeric, and categorical columns have correct dtypes
- [ ] Row count and columns match the expected data spec (482 records)

Commit:

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

### TASK-1: Environment setup and project initialization
Set up the project structure, dependencies, and a runnable Streamlit skeleton.
- [ ] Project structure created (`app.py`, `data/`, `requirements.txt`)
- [ ] Dependencies installed (Streamlit, Plotly, Pandas)
- [ ] `streamlit run app.py` launches without errors

Commit:

## Done
