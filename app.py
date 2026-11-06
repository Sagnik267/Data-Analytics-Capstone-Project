import os
import streamlit as st
import pandas as pd

from src.data_cleaning import load_data, clean_data, save_to_db, load_from_db
from src.kpi_calculations import (
    calculate_overall_kpis,
    calculate_channel_kpis,
    calculate_campaign_kpis
)
from src.analysis import get_daily_trend
from src.visualizations import (
    plot_trend,
    plot_channel_spend_vs_revenue,
    plot_channel_roas,
    plot_funnel,
    plot_campaign_scatter,
    plot_spend_donut,
    plot_revenue_donut
)

# set up page layout
st.set_page_config(page_title="Marketing Performance Dashboard", layout="wide")

# load data from sqlite or csv
def get_app_data():
    db_path = "database/marketing.db"
    if os.path.exists(db_path):
        df = load_from_db(db_path)
    else:
        df = load_data()
        df = clean_data(df)
        save_to_db(df, db_path)
    return df

df_all = get_app_data()

# sidebar filters
st.sidebar.title("Dashboard Filters")

# date filter
min_date = df_all["date"].min().date()
max_date = df_all["date"].max().date()
selected_dates = st.sidebar.date_input("Date Range", [min_date, max_date])

if isinstance(selected_dates, (list, tuple)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date, end_date = min_date, max_date

# channel filter
channels = sorted(df_all["channel"].unique().tolist())
selected_channels = st.sidebar.multiselect("Channels", channels, default=channels)

# campaign filter based on selected channels
campaigns = sorted(df_all[df_all["channel"].isin(selected_channels)]["campaign_name"].unique().tolist())
selected_campaigns = st.sidebar.multiselect("Campaigns", campaigns, default=campaigns)

# target benchmark
target_roas = st.sidebar.slider("Target ROAS Benchmark", 1.0, 6.0, 3.0, 0.5)

# filter dataframe based on sidebar inputs
mask = (
    (df_all["date"].dt.date >= start_date) &
    (df_all["date"].dt.date <= end_date) &
    (df_all["channel"].isin(selected_channels)) &
    (df_all["campaign_name"].isin(selected_campaigns))
)
df = df_all[mask].copy()

if df.empty:
    st.warning("No data found for the selected filters. Please adjust your filter choices.")
    st.stop()

# calculate metrics
kpis = calculate_overall_kpis(df)
channel_df = calculate_channel_kpis(df)
camp_df = calculate_campaign_kpis(df)
daily_df = get_daily_trend(df)

# main dashboard header
st.title("Marketing Performance Dashboard")
st.caption(f"Module 3: Dashboard Development | Active Filter: {start_date} to {end_date}")

# kpi scorecard row
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Spend", f"${kpis['total_spend']:,.0f}")
col2.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
col3.metric("Net Profit", f"${kpis['net_profit']:,.0f}")
col4.metric("ROAS", f"{kpis['roas']:.2f}x")
col5.metric("Conversions", f"{kpis['total_conversions']:,}")
col6.metric("Average CPA", f"${kpis['cpa']:.2f}")

st.write("")

# 1. daily trend chart
st.subheader("Daily Engagement and Revenue Trends")
st.plotly_chart(plot_trend(daily_df), use_container_width=True)

# 2. channel comparisons
st.subheader("Channel-Wise Comparison")
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.plotly_chart(plot_channel_spend_vs_revenue(channel_df), use_container_width=True)
with chart_col2:
    st.plotly_chart(plot_channel_roas(channel_df, target_roas), use_container_width=True)

# 3. funnel and campaign efficiency
st.subheader("Funnel and Campaign Performance")
funnel_col, scatter_col = st.columns(2)
with funnel_col:
    funnel_fig = plot_funnel(kpis["total_impressions"], kpis["total_clicks"], kpis["total_conversions"])
    st.plotly_chart(funnel_fig, use_container_width=True)
with scatter_col:
    scatter_fig = plot_campaign_scatter(camp_df)
    st.plotly_chart(scatter_fig, use_container_width=True)

# 4. share of channel donuts
st.subheader("Channel Budget and Revenue Distribution")
donut_col1, donut_col2 = st.columns(2)
with donut_col1:
    st.plotly_chart(plot_spend_donut(channel_df), use_container_width=True)
with donut_col2:
    st.plotly_chart(plot_revenue_donut(channel_df), use_container_width=True)

# 5. channel summary table
st.subheader("Channel Summary")
st.dataframe(channel_df, use_container_width=True)
