import plotly.express as px
import streamlit as st

from sales_data import (
    get_category_breakdown,
    get_monthly_sales_trend,
    get_region_breakdown,
    get_total_orders,
    get_total_sales,
    load_sales_data,
)

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def load_data():
    return load_sales_data("data/sales-data.csv")


df = load_data()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${get_total_sales(df):,.0f}")
col2.metric("Total Orders", f"{get_total_orders(df):,}")

st.subheader("Sales Trend Over Time")
trend = get_monthly_sales_trend(df)
trend_fig = px.line(trend, x="month", y="total_amount", markers=True)
trend_fig.update_layout(xaxis_title="Month", yaxis_title="Total Sales ($)")
st.plotly_chart(trend_fig, use_container_width=True)

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
