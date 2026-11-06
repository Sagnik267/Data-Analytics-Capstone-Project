import sqlite3
import pandas as pd

# load raw data from csv
def load_data(csv_path="data/marketing_data.csv"):
    df = pd.read_csv(csv_path)
    return df

# clean the dataframe columns and values
def clean_data(df):
    # lowercase column names
    df.columns = df.columns.str.lower().str.strip()

    # convert date column to datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    # fill missing values in numeric columns with 0
    num_cols = ["spend", "impressions", "clicks", "conversions", "revenue"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # remove duplicate rows
    df = df.drop_duplicates()

    return df

# save cleaned data into sqlite database
def save_to_db(df, db_path="database/marketing.db"):
    conn = sqlite3.connect(db_path)
    df.to_sql("marketing_data", conn, if_exists="replace", index=False)
    conn.close()

# load data back from sqlite database
def load_from_db(db_path="database/marketing.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM marketing_data", conn)
    conn.close()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    return df
