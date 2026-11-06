import numpy as np
import pandas as pd
from src.kpi_calculations import calculate_campaign_kpis

# aggregate data by date for line charts
def get_daily_trend(df):
    if "date" not in df.columns or df.empty:
        return pd.DataFrame()

    daily = df.groupby(df["date"].dt.date).agg({
        "spend": "sum",
        "revenue": "sum",
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum"
    }).reset_index()

    daily["date"] = pd.to_datetime(daily["date"])
    daily["profit"] = daily["revenue"] - daily["spend"]
    daily["roas"] = np.where(daily["spend"] > 0, daily["revenue"] / daily["spend"], 0)
    daily["ctr"] = np.where(daily["impressions"] > 0, (daily["clicks"] / daily["impressions"]) * 100, 0)
    daily["cvr"] = np.where(daily["clicks"] > 0, (daily["conversions"] / daily["clicks"]) * 100, 0)

    return daily.sort_values(by="date").reset_index(drop=True)

# find top and bottom campaigns by any metric
def get_top_and_bottom_campaigns(df, metric="roas", n=5):
    camp_df = calculate_campaign_kpis(df)
    if camp_df.empty or metric not in camp_df.columns:
        return pd.DataFrame(), pd.DataFrame()

    top_camps = camp_df.sort_values(by=metric, ascending=False).head(n).reset_index(drop=True)
    bottom_camps = camp_df.sort_values(by=metric, ascending=True).head(n).reset_index(drop=True)

    return top_camps, bottom_camps

# label campaigns based on roas and cpa thresholds
def classify_campaigns(df, target_roas=3.0, max_cpa=35.0):
    camp_df = calculate_campaign_kpis(df)
    if camp_df.empty:
        return pd.DataFrame()

    def get_status(row):
        good_roas = row["roas"] >= target_roas
        good_cpa = row["cpa"] <= max_cpa

        if good_roas and good_cpa:
            return "Top Performer"
        elif good_roas and not good_cpa:
            return "High Value High Cost"
        elif not good_roas and good_cpa:
            return "Low Cost Opportunity"
        else:
            return "Underperforming"

    camp_df["status"] = camp_df.apply(get_status, axis=1)
    return camp_df

# calculate simple correlation between spend and revenue
def get_correlation(df):
    cols = ["spend", "revenue", "clicks", "conversions"]
    corr_df = df[cols].corr()
    return corr_df
