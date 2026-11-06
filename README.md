# Marketing Performance Dashboard

I built this project as my college Data Analytics Capstone Project based on the SkillOrbit capstone guidelines. It focuses on Module 3 (Dashboard Development) to track and analyze marketing campaign performance across Google Search, Meta Ads, YouTube, Email, and LinkedIn.

## Tech Stack
- Python
- Pandas and NumPy
- Plotly
- Streamlit
- SQLite

## Project Modules
- Module 1: Marketing Data Collection (data/marketing_data.csv and SQLite database)
- Module 2: Data Cleaning and Analysis (src/data_cleaning.py and src/kpi_calculations.py)
- Module 3: Dashboard Development (app.py and src/visualizations.py)
- Module 4: Business Insights and Recommendations (src/analysis.py)
- Module 5: Report Generation (src/report_generation.py)

## Key Formulas
- CTR = (Clicks / Impressions) * 100
- CPC = Spend / Clicks
- CPA = Spend / Conversions
- CVR = (Conversions / Clicks) * 100
- ROAS = Revenue / Spend
- Net Profit = Revenue - Spend

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Run the Streamlit dashboard:
   streamlit run app.py
