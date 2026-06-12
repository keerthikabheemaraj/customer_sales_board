import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Sales Dashboard & Customer Insights")


df = pd.read_csv("Sample - Superstore.csv", encoding="cp1252")


df["Order Date"] = pd.to_datetime(df["Order Date"])

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]


total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer Name"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Orders", total_orders)
col4.metric("Customers", total_customers)

st.subheader("Monthly Sales Trend")

monthly_sales = filtered_df.groupby(
    filtered_df["Order Date"].dt.month
)["Sales"].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sales by Category")

category_sales = filtered_df.groupby(
    "Category"
)["Sales"].sum().reset_index()

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales"
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Profit by Region")

region_profit = filtered_df.groupby(
    "Region"
)["Profit"].sum().reset_index()

fig3 = px.bar(
    region_profit,
    x="Region",
    y="Profit"
)

st.plotly_chart(fig3, use_container_width=True)

st.subheader("Top 10 Customers")

top_customers = filtered_df.groupby(
    "Customer Name"
)["Sales"].sum().sort_values(
    ascending=False
).head(10)

st.bar_chart(top_customers)