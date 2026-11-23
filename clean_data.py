
import pandas as pd
import numpy as np

# 1. Read NAV history dataset
df = pd.read_csv("data/raw/nav_history.csv")

print("Original Dataset Shape:", df.shape)

# 2. Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# 3. Convert NAV to numeric
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

# 4. Remove invalid dates
df = df.dropna(subset=["date"])

# 5. Sort by amfi_code and date
df = df.sort_values(
    by=["amfi_code", "date"]
).reset_index(drop=True)

# 6. Remove duplicate records
df = df.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="last"
)

# 7. Forward fill missing NAV values
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# 8. Remove missing or invalid NAV values
df = df.dropna(subset=["nav"])
df = df[df["nav"] > 0]

# 9. Save cleaned dataset
df.to_csv(
    "data/processed/nav_history_cleaned.csv",
    index=False
)

# 10. Display results
print("\nCleaned Dataset Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

print("\nFirst 5 Cleaned Rows:")
print(df.head())

print("\nNAV Cleaning Completed Successfully!")

# ==========================================
# 2. CLEAN INVESTOR TRANSACTIONS DATASET
# ==========================================

# Read dataset
transactions = pd.read_csv(
    "data/raw/investor_transactions.csv"
)

print("\nOriginal Transactions Shape:", transactions.shape)

# Clean column names
transactions.columns = (
    transactions.columns
    .str.replace("*", "", regex=False)
    .str.replace("&#x61;", "a", regex=False)
    .str.replace("_", "_", regex=False)
    .str.strip()
)

# Remove unwanted special characters from column names
transactions.columns = transactions.columns.str.replace(
    r"[^a-zA-Z0-9_]", "", regex=True
)

# Remove unwanted characters from text columns
for col in transactions.select_dtypes(include="object").columns:
    transactions[col] = (
        transactions[col]
        .astype(str)
        .str.replace(r"^[*]+", "", regex=True)
        .str.strip()
    )

# Convert transaction date to datetime
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

# Convert amount to numeric
transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"],
    errors="coerce"
)

# Standardize transaction types
transactions["transaction_type"] = (
    transactions["transaction_type"]
    .str.strip()
    .str.title()
)

# Keep only valid transaction types
valid_types = ["SIP", "Lumpsum", "Redemption"]

transactions = transactions[
    transactions["transaction_type"].isin(valid_types)
]

# Standardize KYC status
transactions["kyc_status"] = (
    transactions["kyc_status"]
    .str.strip()
    .str.title()
)

# Validate KYC status
valid_kyc = ["Verified", "Pending", "Rejected"]

transactions = transactions[
    transactions["kyc_status"].isin(valid_kyc)
]

# Remove invalid dates and amounts
transactions = transactions.dropna(
    subset=["transaction_date", "amount_inr"]
)

transactions = transactions[
    transactions["amount_inr"] > 0
]

# Remove duplicate records
transactions = transactions.drop_duplicates()

# Save cleaned dataset
transactions.to_csv(
    "data/processed/investor_transactions_cleaned.csv",
    index=False
)

# Display results
print("\nCleaned Transactions Shape:", transactions.shape)

print("\nTransaction Types:")
print(transactions["transaction_type"].value_counts())

print("\nKYC Status:")
print(transactions["kyc_status"].value_counts())

print("\nMissing Values:")
print(transactions.isnull().sum())

print("\nInvestor Transactions Cleaning Completed!")

# Step 3: Clean Scheme Performance Data

performance = pd.read_csv("data/raw/scheme_performance.csv")

print("\nScheme Performance - Original Data:")
print(performance.head())

print("\nColumns:")
print(performance.columns.tolist())

print("\nData Types:")
print(performance.dtypes)


# Step 3: Clean Scheme Performance Data

performance = pd.read_csv("data/raw/scheme_performance.csv")

# Convert numeric columns
numeric_columns = [
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
    "morningstar_rating"
]

for col in numeric_columns:
    performance[col] = pd.to_numeric(performance[col], errors="coerce")

# Remove duplicate records
performance = performance.drop_duplicates(subset=["amfi_code"])

# Remove missing important values
performance = performance.dropna(
    subset=["amfi_code", "scheme_name", "expense_ratio_pct"]
)

# Validate expense ratio
performance = performance[
    (performance["expense_ratio_pct"] >= 0) &
    (performance["expense_ratio_pct"] <= 5)
]

# Check invalid AUM
performance = performance[performance["aum_crore"] >= 0]

# Save cleaned dataset
performance.to_csv(
    "data/processed/scheme_performance_cleaned.csv",
    index=False
)

print("\nScheme Performance Original Shape:", pd.read_csv("data/raw/scheme_performance.csv").shape)
print("Scheme Performance Cleaned Shape:", performance.shape)

print("\nMissing Values:")
print(performance.isnull().sum())

print("\nExpense Ratio Summary:")
print(performance["expense_ratio_pct"].describe())

print("\nScheme Performance Cleaning Completed!")


# Step 4: Check Fund Master Data

fund_master = pd.read_csv("data/raw/fund_master.csv")

print("\nFund Master - Original Data:")
print(fund_master.head())

print("\nColumns:")
print(fund_master.columns.tolist())

print("\nData Types:")
print(fund_master.dtypes)

print("\nMissing Values:")
print(fund_master.isnull().sum())


# Step 4: Clean Fund Master Data

fund_master = pd.read_csv("data/raw/fund_master.csv")

# Convert launch_date to datetime
fund_master["launch_date"] = pd.to_datetime(
    fund_master["launch_date"], errors="coerce"
)

# Remove duplicate AMFI codes
fund_master = fund_master.drop_duplicates(
    subset=["amfi_code"], keep="last"
)

# Remove rows with missing important values
fund_master = fund_master.dropna(
    subset=["amfi_code", "scheme_name", "launch_date"]
)

# Validate expense ratio and exit load
fund_master = fund_master[
    (fund_master["expense_ratio_pct"] >= 0) &
    (fund_master["expense_ratio_pct"] <= 5)
]

fund_master = fund_master[
    (fund_master["exit_load_pct"] >= 0) &
    (fund_master["exit_load_pct"] <= 5)
]

# Save cleaned data
fund_master.to_csv(
    "data/processed/fund_master_cleaned.csv",
    index=False
)

print("\nFund Master Original Shape:",
      pd.read_csv("data/raw/fund_master.csv").shape)

print("Fund Master Cleaned Shape:", fund_master.shape)

print("\nMissing Values:")
print(fund_master.isnull().sum())

print("\nFund Master Cleaning Completed!")


# Step 5: Check Portfolio Holdings Data

holdings = pd.read_csv("data/raw/portfolio_holdings.csv")

print("\nPortfolio Holdings - Original Data:")
print(holdings.head())

print("\nColumns:")
print(holdings.columns.tolist())

print("\nData Types:")
print(holdings.dtypes)

print("\nMissing Values:")
print(holdings.isnull().sum())


# Step 5: Clean Portfolio Holdings Data

holdings = pd.read_csv("data/raw/portfolio_holdings.csv")

# Convert portfolio_date to datetime
holdings["portfolio_date"] = pd.to_datetime(
    holdings["portfolio_date"], errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "weight_pct",
    "market_value_cr",
    "current_price_inr"
]

for col in numeric_columns:
    holdings[col] = pd.to_numeric(holdings[col], errors="coerce")

# Remove duplicates
holdings = holdings.drop_duplicates(
    subset=["amfi_code", "stock_symbol", "portfolio_date"]
)

# Remove missing important values
holdings = holdings.dropna(
    subset=["amfi_code", "stock_symbol", "portfolio_date"]
)

# Validate numeric values
holdings = holdings[
    (holdings["weight_pct"] >= 0) &
    (holdings["market_value_cr"] >= 0) &
    (holdings["current_price_inr"] > 0)
]

# Save cleaned data
holdings.to_csv(
    "data/processed/portfolio_holdings_cleaned.csv",
    index=False
)

print("\nPortfolio Holdings Original Shape:",
      pd.read_csv("data/raw/portfolio_holdings.csv").shape)

print("Portfolio Holdings Cleaned Shape:", holdings.shape)

print("\nMissing Values:")
print(holdings.isnull().sum())

print("\nPortfolio Holdings Cleaning Completed!")


# Step 6: Check Benchmark Indices Data

benchmark = pd.read_csv("data/raw/benchmark_indices.csv")

print("\nBenchmark Indices - Original Data:")
print(benchmark.head())

print("\nColumns:")
print(benchmark.columns.tolist())

print("\nData Types:")
print(benchmark.dtypes)

print("\nMissing Values:")
print(benchmark.isnull().sum())


# Step 6: Clean Benchmark Indices Data

benchmark = pd.read_csv("data/raw/benchmark_indices.csv")

# Convert date to datetime
benchmark["date"] = pd.to_datetime(
    benchmark["date"], errors="coerce"
)

# Convert close_value to numeric
benchmark["close_value"] = pd.to_numeric(
    benchmark["close_value"], errors="coerce"
)

# Remove duplicates
benchmark = benchmark.drop_duplicates(
    subset=["date", "index_name"]
)

# Remove missing values
benchmark = benchmark.dropna(
    subset=["date", "index_name", "close_value"]
)

# Validate close value
benchmark = benchmark[benchmark["close_value"] > 0]

# Sort data
benchmark = benchmark.sort_values(
    by=["index_name", "date"]
).reset_index(drop=True)

# Save cleaned data
benchmark.to_csv(
    "data/processed/benchmark_indices_cleaned.csv",
    index=False
)

print("\nBenchmark Original Shape:",
      pd.read_csv("data/raw/benchmark_indices.csv").shape)

print("Benchmark Cleaned Shape:", benchmark.shape)

print("\nMissing Values:")
print(benchmark.isnull().sum())

print("\nBenchmark Indices Cleaning Completed!")


# Step 7: Check AUM by Fund House Data

aum = pd.read_csv("data/raw/aum_by_fund_house.csv")

print("\nAUM by Fund House - Original Data:")
print(aum.head())

print("\nColumns:")
print(aum.columns.tolist())

print("\nData Types:")
print(aum.dtypes)

print("\nMissing Values:")
print(aum.isnull().sum())


# Step 7: Clean AUM by Fund House Data

aum = pd.read_csv("data/raw/aum_by_fund_house.csv")

# Convert date to datetime
aum["date"] = pd.to_datetime(
    aum["date"], errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]

for col in numeric_columns:
    aum[col] = pd.to_numeric(aum[col], errors="coerce")

# Remove duplicates
aum = aum.drop_duplicates(
    subset=["date", "fund_house"]
)

# Remove missing values
aum = aum.dropna(
    subset=["date", "fund_house", "aum_crore", "num_schemes"]
)

# Validate values
aum = aum[
    (aum["aum_lakh_crore"] >= 0) &
    (aum["aum_crore"] >= 0) &
    (aum["num_schemes"] >= 0)
]

# Sort data
aum = aum.sort_values(
    by=["fund_house", "date"]
).reset_index(drop=True)

# Save cleaned data
aum.to_csv(
    "data/processed/aum_by_fund_house_cleaned.csv",
    index=False
)

print("\nAUM Original Shape:",
      pd.read_csv("data/raw/aum_by_fund_house.csv").shape)

print("AUM Cleaned Shape:", aum.shape)

print("\nMissing Values:")
print(aum.isnull().sum())

print("\nAUM Cleaning Completed!")


# Step 8: Check Monthly SIP Inflows Data

sip = pd.read_csv("data/raw/monthly_sip_inflows.csv")

print("\nMonthly SIP Inflows - Original Data:")
print(sip.head())

print("\nColumns:")
print(sip.columns.tolist())

print("\nData Types:")
print(sip.dtypes)

print("\nMissing Values:")
print(sip.isnull().sum())


# Step 8: Clean Monthly SIP Inflows Data

sip = pd.read_csv("data/raw/monthly_sip_inflows.csv")

# Convert month to datetime
sip["month"] = pd.to_datetime(
    sip["month"], format="%Y-%m", errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]

for col in numeric_columns:
    sip[col] = pd.to_numeric(sip[col], errors="coerce")

# Remove duplicate months
sip = sip.drop_duplicates(subset=["month"])

# Remove rows with missing important values
sip = sip.dropna(
    subset=["month", "sip_inflow_crore"]
)

# Validate values
sip = sip[
    (sip["sip_inflow_crore"] >= 0) &
    (sip["active_sip_accounts_crore"] >= 0) &
    (sip["new_sip_accounts_lakh"] >= 0) &
    (sip["sip_aum_lakh_crore"] >= 0)
]

# Sort by month
sip = sip.sort_values("month").reset_index(drop=True)

# Save cleaned data
sip.to_csv(
    "data/processed/monthly_sip_inflows_cleaned.csv",
    index=False
)

print("\nSIP Original Shape:",
      pd.read_csv("data/raw/monthly_sip_inflows.csv").shape)

print("SIP Cleaned Shape:", sip.shape)

print("\nMissing Values:")
print(sip.isnull().sum())

print("\nMonthly SIP Inflows Cleaning Completed!")

# Step 9: Check Category Inflows Data

category = pd.read_csv("data/raw/category_inflows.csv")

print("\nCategory Inflows - Original Data:")
print(category.head())

print("\nColumns:")
print(category.columns.tolist())

print("\nData Types:")
print(category.dtypes)

print("\nMissing Values:")
print(category.isnull().sum())

print("\nOriginal Shape:", category.shape)


# Step 9: Clean Category Inflows Data

category = pd.read_csv("data/raw/category_inflows.csv")

# Convert month to datetime
category["month"] = pd.to_datetime(
    category["month"], format="%Y-%m", errors="coerce"
)

# Convert numeric column
category["net_inflow_crore"] = pd.to_numeric(
    category["net_inflow_crore"], errors="coerce"
)

# Remove duplicates
category = category.drop_duplicates(
    subset=["month", "category"]
)

# Remove rows with missing important values
category = category.dropna(
    subset=["month", "category", "net_inflow_crore"]
)

# Sort data
category = category.sort_values(
    by=["month", "category"]
).reset_index(drop=True)

# Save cleaned data
category.to_csv(
    "data/processed/category_inflows_cleaned.csv",
    index=False
)

print("\nCategory Inflows Original Shape:",
      pd.read_csv("data/raw/category_inflows.csv").shape)

print("Category Inflows Cleaned Shape:", category.shape)

print("\nMissing Values:")
print(category.isnull().sum())

print("\nCategory Inflows Cleaning Completed!")

# Step 10: Check Industry Folio Count Data

industry = pd.read_csv("data/raw/industry_folio_count.csv")

print("\nIndustry Folio Count - Original Data:")
print(industry.head())

print("\nColumns:")
print(industry.columns.tolist())

print("\nData Types:")
print(industry.dtypes)

print("\nMissing Values:")
print(industry.isnull().sum())

print("\nOriginal Shape:", industry.shape)


# Step 10: Clean Industry Folio Count Data

industry = pd.read_csv("data/raw/industry_folio_count.csv")

# Convert month to datetime
industry["month"] = pd.to_datetime(
    industry["month"], format="%Y-%m", errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]

for col in numeric_columns:
    industry[col] = pd.to_numeric(
        industry[col], errors="coerce"
    )

# Remove duplicate months
industry = industry.drop_duplicates(subset=["month"])

# Remove rows with missing values
industry = industry.dropna()

# Validate non-negative values
industry = industry[
    (industry[numeric_columns] >= 0).all(axis=1)
]

# Sort by month
industry = industry.sort_values(
    "month"
).reset_index(drop=True)

# Save cleaned data
industry.to_csv(
    "data/processed/industry_folio_count_cleaned.csv",
    index=False
)

print("\nIndustry Folio Count Original Shape:",
      pd.read_csv("data/raw/industry_folio_count.csv").shape)

print("Industry Folio Count Cleaned Shape:", industry.shape)

print("\nMissing Values:")
print(industry.isnull().sum())

print("\nIndustry Folio Count Cleaning Completed!")


import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

tables = cursor.fetchall()

print("Database Tables:")

for table in tables:
    print(table[0])

conn.close()
