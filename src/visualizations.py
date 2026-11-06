import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# line chart showing spend, revenue and profit over time
def plot_trend(daily_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_df["date"],
        y=daily_df["revenue"],
        mode="lines",
        name="Revenue ($)",
        line=dict(color="#10b981", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=daily_df["date"],
        y=daily_df["spend"],
        mode="lines",
        name="Spend ($)",
        line=dict(color="#ef4444", width=2, dash="dash")
    ))

    fig.add_trace(go.Scatter(
        x=daily_df["date"],
        y=daily_df["profit"],
        mode="lines",
        name="Net Profit ($)",
        line=dict(color="#3b82f6", width=2)
    ))

    fig.update_layout(
        title="Daily Spend, Revenue and Profit",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig

# bar chart comparing spend and revenue for each channel
def plot_channel_spend_vs_revenue(channel_df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=channel_df["channel"],
        y=channel_df["revenue"],
        name="Revenue ($)",
        marker_color="#10b981"
    ))

    fig.add_trace(go.Bar(
        x=channel_df["channel"],
        y=channel_df["spend"],
        name="Spend ($)",
        marker_color="#ef4444"
    ))

    fig.update_layout(
        title="Revenue vs Spend by Channel",
        barmode="group",
        xaxis_title="Channel",
        yaxis_title="Amount ($)",
        template="plotly_white"
    )
    return fig

# bar chart showing roas per channel with a target line
def plot_channel_roas(channel_df, target_roas=3.0):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=channel_df["channel"],
        y=channel_df["roas"],
        name="ROAS",
        marker_color="#6366f1"
    ))

    # add target line
    fig.add_hline(
        y=target_roas,
        line_dash="dot",
        line_color="#dc2626",
        annotation_text=f"Target ({target_roas}x)"
    )

    fig.update_layout(
        title="ROAS by Channel",
        xaxis_title="Channel",
        yaxis_title="ROAS (Multiplier)",
        template="plotly_white"
    )
    return fig

# funnel chart showing impressions to clicks to conversions
def plot_funnel(total_impressions, total_clicks, total_conversions):
    fig = go.Figure(go.Funnel(
        y=["Impressions", "Clicks", "Conversions"],
        x=[total_impressions, total_clicks, total_conversions],
        textinfo="value+percent initial"
    ))

    fig.update_layout(
        title="Conversion Funnel",
        template="plotly_white"
    )
    return fig

# scatter plot showing cpa vs roas for all campaigns
def plot_campaign_scatter(camp_df):
    fig = px.scatter(
        camp_df,
        x="cpa",
        y="roas",
        size="spend",
        color="channel",
        hover_name="campaign_name",
        title="Campaign Efficiency (CPA vs ROAS)",
        labels={"cpa": "CPA ($)", "roas": "ROAS (x)", "spend": "Total Spend ($)"},
        template="plotly_white"
    )
    return fig

# donut chart showing spend share by channel
def plot_spend_donut(channel_df):
    fig = px.pie(
        channel_df,
        names="channel",
        values="spend",
        title="Spend Share by Channel",
        hole=0.4,
        template="plotly_white"
    )
    return fig

# donut chart showing revenue share by channel
def plot_revenue_donut(channel_df):
    fig = px.pie(
        channel_df,
        names="channel",
        values="revenue",
        title="Revenue Share by Channel",
        hole=0.4,
        template="plotly_white"
    )
    return fig
