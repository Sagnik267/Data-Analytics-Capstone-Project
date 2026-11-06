# create bullet point takeaways from our kpis
def generate_insights(kpis, channel_df):
    insights = []

    roas = kpis.get("roas", 0)
    profit = kpis.get("net_profit", 0)

    # overall roas check
    if roas >= 3.0:
        insights.append(f"Overall ROAS is {roas:.2f}x, which is profitable with ${profit:,.2f} in net profit.")
    else:
        insights.append(f"Overall ROAS is {roas:.2f}x. Some campaigns might be losing money.")

    # check channels if we have them
    if not channel_df.empty:
        # best revenue channel
        top_rev = channel_df.sort_values(by="revenue", ascending=False).iloc[0]
        insights.append(f"Top revenue channel is {top_rev['channel']} with ${top_rev['revenue']:,.2f} in sales.")

        # best roas channel
        top_roas = channel_df.sort_values(by="roas", ascending=False).iloc[0]
        insights.append(f"Highest ROAS channel is {top_roas['channel']} with a return of {top_roas['roas']:.2f}x.")

        # lowest roas channel
        lowest_roas = channel_df.sort_values(by="roas", ascending=True).iloc[0]
        if lowest_roas["channel"] != top_roas["channel"]:
            insights.append(f"Lowest performing channel by ROAS is {lowest_roas['channel']} at {lowest_roas['roas']:.2f}x.")

    # conversion funnel check
    ctr = kpis.get("ctr", 0)
    cvr = kpis.get("cvr", 0)
    insights.append(f"Average CTR is {ctr:.2f}% and conversion rate (CVR) is {cvr:.2f}%.")

    return insights

# suggest basic budget and campaign adjustments
def generate_recommendations(channel_df, camp_df):
    tips = []

    if channel_df.empty or camp_df.empty:
        return tips

    # scale channels with good return
    good_channels = channel_df[channel_df["roas"] >= 3.5]["channel"].tolist()
    if good_channels:
        tips.append({
            "area": "Budget Allocation",
            "tip": f"Consider increasing budget for {', '.join(good_channels)} since their ROAS is above 3.5x."
        })

    # check low return campaigns
    bad_camps = camp_df[camp_df["roas"] < 2.0]["campaign_name"].tolist()
    if bad_camps:
        tips.append({
            "area": "Campaign Review",
            "tip": f"Look into or pause these low-return campaigns: {', '.join(bad_camps[:3])}."
        })

    # check low click through rate
    low_ctr_channels = channel_df[channel_df["ctr"] < 2.0]["channel"].tolist()
    if low_ctr_channels:
        tips.append({
            "area": "Ad Copy and Creatives",
            "tip": f"Refresh ad copy for {', '.join(low_ctr_channels)} to help raise CTR above 2%."
        })

    return tips

# generate a simple plain text report for downloading
def generate_text_report(kpis, channel_df):
    lines = []
    lines.append("Marketing Performance Dashboard Report")
    lines.append("--------------------------------------")
    lines.append(f"Total Spend:        ${kpis.get('total_spend', 0):,.2f}")
    lines.append(f"Total Revenue:      ${kpis.get('total_revenue', 0):,.2f}")
    lines.append(f"Net Profit:         ${kpis.get('net_profit', 0):,.2f}")
    lines.append(f"Overall ROAS:       {kpis.get('roas', 0):.2f}x")
    lines.append(f"Impressions:        {kpis.get('total_impressions', 0):,}")
    lines.append(f"Clicks:             {kpis.get('total_clicks', 0):,}")
    lines.append(f"Conversions:        {kpis.get('total_conversions', 0):,}")
    lines.append(f"Average CTR:        {kpis.get('ctr', 0):.2f}%")
    lines.append(f"Average CPC:        ${kpis.get('cpc', 0):.2f}")
    lines.append(f"Average CPA:        ${kpis.get('cpa', 0):.2f}")
    lines.append("")
    lines.append("Channel Breakdown:")
    lines.append("------------------")

    for _, row in channel_df.iterrows():
        lines.append(
            f"{row['channel']}: Spend=${row['spend']:,.0f}, Revenue=${row['revenue']:,.0f}, ROAS={row['roas']:.2f}x, CPA=${row['cpa']:.2f}"
        )

    return "\n".join(lines)
