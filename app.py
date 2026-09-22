import plotly.express as px
import streamlit as st

from sales_data import (
    get_monthly_sales_trend,
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
