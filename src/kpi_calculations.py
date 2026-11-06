import numpy as np
import pandas as pd

# calculate total summary metrics for the whole dataset
def calculate_overall_kpis(df):
    total_spend = df["spend"].sum()
    total_revenue = df["revenue"].sum()
    total_impressions = df["impressions"].sum()
    total_clicks = df["clicks"].sum()
    total_conversions = df["conversions"].sum()

    net_profit = total_revenue - total_spend

    # avoid dividing by zero
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    cpa = (total_spend / total_conversions) if total_conversions > 0 else 0
    cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    roas = (total_revenue / total_spend) if total_spend > 0 else 0

    return {
        "total_spend": total_spend,
        "total_revenue": total_revenue,
        "net_profit": net_profit,
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "ctr": ctr,
        "cpc": cpc,
        "cpa": cpa,
        "cvr": cvr,
        "roas": roas,
    }

# add kpi columns to each row
def add_kpi_columns(df):
    df = df.copy()

    # use np.where so we do not crash on zeros
    df["ctr"] = np.where(df["impressions"] > 0, (df["clicks"] / df["impressions"]) * 100, 0)
    df["cpc"] = np.where(df["clicks"] > 0, df["spend"] / df["clicks"], 0)
    df["cpa"] = np.where(df["conversions"] > 0, df["spend"] / df["conversions"], 0)
    df["cvr"] = np.where(df["clicks"] > 0, (df["conversions"] / df["clicks"]) * 100, 0)
    df["roas"] = np.where(df["spend"] > 0, df["revenue"] / df["spend"], 0)
    df["profit"] = df["revenue"] - df["spend"]

    return df

# group metrics by marketing channel
def calculate_channel_kpis(df):
    grouped = df.groupby("channel", as_index=False).agg({
        "spend": "sum",
        "revenue": "sum",
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum"
    })

    grouped["profit"] = grouped["revenue"] - grouped["spend"]
    grouped["roas"] = np.where(grouped["spend"] > 0, grouped["revenue"] / grouped["spend"], 0)
    grouped["ctr"] = np.where(grouped["impressions"] > 0, (grouped["clicks"] / grouped["impressions"]) * 100, 0)
    grouped["cpc"] = np.where(grouped["clicks"] > 0, grouped["spend"] / grouped["clicks"], 0)
    grouped["cpa"] = np.where(grouped["conversions"] > 0, grouped["spend"] / grouped["conversions"], 0)
    grouped["cvr"] = np.where(grouped["clicks"] > 0, (grouped["conversions"] / grouped["clicks"]) * 100, 0)

    # sort by revenue
    return grouped.sort_values(by="revenue", ascending=False).reset_index(drop=True)

# group metrics by campaign
def calculate_campaign_kpis(df):
    grouped = df.groupby(["campaign_name", "channel"], as_index=False).agg({
        "spend": "sum",
        "revenue": "sum",
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum"
    })

    grouped["profit"] = grouped["revenue"] - grouped["spend"]
    grouped["roas"] = np.where(grouped["spend"] > 0, grouped["revenue"] / grouped["spend"], 0)
    grouped["ctr"] = np.where(grouped["impressions"] > 0, (grouped["clicks"] / grouped["impressions"]) * 100, 0)
    grouped["cpc"] = np.where(grouped["clicks"] > 0, grouped["spend"] / grouped["clicks"], 0)
    grouped["cpa"] = np.where(grouped["conversions"] > 0, grouped["spend"] / grouped["conversions"], 0)
    grouped["cvr"] = np.where(grouped["clicks"] > 0, (grouped["conversions"] / grouped["clicks"]) * 100, 0)

    # sort by roas
    return grouped.sort_values(by="roas", ascending=False).reset_index(drop=True)
