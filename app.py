# =========================================
# Supermarket Sales Interactive Dashboard
# =========================================

import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
from config import DATA_DIR

# -----------------------
# LOAD & CLEAN DATA
# -----------------------
datapath = DATA_DIR / "supermarket_sales.csv"

# Skip first 3 lines (extra commas at the top)
df = pd.read_csv(datapath, skiprows=3)

# Convert date to datetime format
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month_name()

# Compute derived metrics
df["Profit"] = df["gross income"]
df["Gross Margin %"] = (df["Profit"] / df["Total"]) * 100

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("🔍 Filter Options")

city = st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

branch = st.sidebar.multiselect(
    "Select Branch:",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

product_line = st.sidebar.multiselect(
    "Select Product Line:",
    options=df["Product line"].unique(),
    default=df["Product line"].unique()
)

filtered_df = df[
    (df["City"].isin(city)) &
    (df["Branch"].isin(branch)) &
    (df["Product line"].isin(product_line))
]

# -----------------------
# KPI SUMMARY SECTION
# -----------------------
st.title("🛒 Supermarket Sales Dashboard")

st.markdown("### 📈 Key Metrics")

total_sales = int(filtered_df["Total"].sum())
avg_rating = round(filtered_df["Rating"].mean(), 2)
total_gross_income = int(filtered_df["gross income"].sum())
total_profit = int(filtered_df["Profit"].sum())
avg_margin = round(filtered_df["Gross Margin %"].mean(), 2)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales ($)", f"{total_sales:,.0f}")
col2.metric("Average Rating", f"{avg_rating}")
col3.metric("Gross Income ($)", f"{total_gross_income:,.0f}")
col4.metric("Total Profit ($)", f"{total_profit:,.0f}")
col5.metric("Avg Margin (%)", f"{avg_margin}%")

st.markdown("---")
st.subheader("🧾 Filtered Data Preview")
st.dataframe(filtered_df.head(10))
st.caption(f"Data last updated on: {df['Date'].max().strftime('%B %d, %Y')}")

# -----------------------
# SALES INSIGHTS
# -----------------------
st.markdown("---")
st.header("📊 Sales Insights")

# 1️⃣ Sales by Product Line
sales_by_product = (
    filtered_df.groupby("Product line")["Total"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_product = px.bar(
    sales_by_product,
    x="Product line",
    y="Total",
    title="💰 Total Sales by Product Line",
    text_auto=".2s",
    color="Product line",
)
st.plotly_chart(fig_product, use_container_width=True)

# 2️⃣ Sales Over Time
sales_by_date = (
    filtered_df.groupby("Date")["Total"]
    .sum()
    .reset_index()
    .sort_values("Date")
)

fig_time = px.line(
    sales_by_date,
    x="Date",
    y="Total",
    title="📆 Sales Trend Over Time",
    markers=True
)
st.plotly_chart(fig_time, use_container_width=True)

# 3️⃣ Average Rating by City
rating_by_city = (
    filtered_df.groupby("City")["Rating"]
    .mean()
    .reset_index()
)

fig_rating = px.bar(
    rating_by_city,
    x="City",
    y="Rating",
    title="⭐ Average Rating by City",
    color="City",
    text_auto=".2f"
)
st.plotly_chart(fig_rating, use_container_width=True)

# -----------------------
# PROFITABILITY INSIGHTS
# -----------------------
st.markdown("---")
st.header("💹 Profitability Insights")

# Profit by Product Line
profit_by_product = (
    filtered_df.groupby("Product line")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_profit = px.bar(
    profit_by_product,
    x="Product line",
    y="Profit",
    title="💸 Total Profit by Product Line",
    color="Product line",
    text_auto=".2s"
)
st.plotly_chart(fig_profit, use_container_width=True)

# Monthly Sales Trend
monthly_sales = (
    filtered_df.groupby("Month")["Total"]
    .sum()
    .reindex([
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ])
    .dropna()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Total",
    title="📅 Monthly Sales Trend",
    markers=True,
    color_discrete_sequence=["#636EFA"]
)
st.plotly_chart(fig_monthly, use_container_width=True)

# Average Profit Margin by City
margin_by_city = (
    filtered_df.groupby("City")["Gross Margin %"]
    .mean()
    .reset_index()
)

fig_margin = px.bar(
    margin_by_city,
    x="City",
    y="Gross Margin %",
    title="🏙️ Average Gross Margin by City",
    color="City",
    text_auto=".2f"
)
st.plotly_chart(fig_margin, use_container_width=True)
st.markdown("---")
# Footer
st.caption("Built with ❤️ by Crispin Oigara | Data Scientist & Analyst | — Data source: Supermarket Sales Sample Dataset")