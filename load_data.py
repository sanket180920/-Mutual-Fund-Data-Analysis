
import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite Database
engine = create_engine("sqlite:///bluestock_mf.db")

# Step 1: Clear old records (if script is run again)
with engine.begin() as conn:
    conn.exec_driver_sql("DELETE FROM fact_nav")
    conn.exec_driver_sql("DELETE FROM fact_transactions")
    conn.exec_driver_sql("DELETE FROM fact_performance")
    conn.exec_driver_sql("DELETE FROM fact_aum")
    conn.exec_driver_sql("DELETE FROM dim_date")
    conn.exec_driver_sql("DELETE FROM dim_fund")

print("Old records cleared!")

# Step 2: Load Fund Master
fund = pd.read_csv("data/processed/fund_master_cleaned.csv")

fund_dim = fund[
    [
        "amfi_code",
        "fund_house",
        "scheme_name",
        "category",
        "sub_category",
        "plan",
        "risk_category"
    ]
]

fund_dim.to_sql("dim_fund", engine, if_exists="append", index=False)

print("Fund Master Loaded!")

# Step 3: Load NAV History
nav = pd.read_csv("data/processed/nav_history_cleaned.csv")

nav["date"] = pd.to_datetime(nav["date"])
nav["date_id"] = nav["date"].dt.strftime("%Y%m%d").astype(int)

# Step 4: Load AUM Data
aum = pd.read_csv("data/processed/aum_by_fund_house_cleaned.csv")

aum["date"] = pd.to_datetime(aum["date"])
aum["date_id"] = aum["date"].dt.strftime("%Y%m%d").astype(int)

# Step 5: Create Date Dimension
all_dates = pd.concat([
    nav["date"],
    aum["date"]
]).drop_duplicates().sort_values()

date_dim = pd.DataFrame({
    "full_date": all_dates.dt.strftime("%Y-%m-%d")
})

date_dim["date_id"] = all_dates.dt.strftime("%Y%m%d").astype(int).values
date_dim["year"] = all_dates.dt.year.values
date_dim["month"] = all_dates.dt.month.values
date_dim["quarter"] = all_dates.dt.quarter.values

date_dim = date_dim[
    ["date_id", "full_date", "year", "month", "quarter"]
]

date_dim.to_sql("dim_date", engine, if_exists="append", index=False)

print("Date Dimension Loaded!")

# Step 6: Load NAV Fact Table
nav_fact = nav[
    ["amfi_code", "date_id", "nav"]
]

nav_fact.to_sql("fact_nav", engine, if_exists="append", index=False)

print("NAV Data Loaded!")

# Step 7: Load Investor Transactions
transactions = pd.read_csv(
    "data/processed/investor_transactions_cleaned.csv"
)

transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

print("Investor Transactions Loaded!")

# Step 8: Load Scheme Performance
performance = pd.read_csv(
    "data/processed/scheme_performance_cleaned.csv"
)

performance_fact = performance[
    [
        "amfi_code",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade"
    ]
]

performance_fact.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

print("Scheme Performance Loaded!")

# Step 9: Load AUM Fact Table
aum_fact = aum[
    [
        "date_id",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
]

aum_fact.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)

print("AUM Data Loaded!")

print("\nAll Required Data Loaded Successfully!")
