
import pandas as pd
import os
import glob

# CSV files folder path
data_folder = "data/raw"

# Find all CSV files
csv_files = glob.glob(os.path.join(data_folder, "*.csv"))

print("Total CSV Files Found:", len(csv_files))

# Load and inspect each CSV file
for file in csv_files:
    print("\n" + "=" * 60)
    print("File Name:", os.path.basename(file))

    df = pd.read_csv(file)

    print("\nShape (Rows, Columns):")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())


# Step 4: Fund Master Analysis

import glob
import pandas as pd

fund_file = glob.glob("Data/raw/*fund_master.csv")[0]

fund_df = pd.read_csv(fund_file)

print("\n===== FUND MASTER ANALYSIS =====")

print("\nUnique Fund Houses:")
print(fund_df["fund_house"].unique())

print("\nUnique Categories:")
print(fund_df["category"].unique())

print("\nUnique Sub Categories:")
print(fund_df["sub_category"].unique())

print("\nUnique Risk Categories:")
print(fund_df["risk_category"].unique())

print("\nTotal Unique AMFI Codes:")
print(fund_df["amfi_code"].nunique())



# Step 5: AMFI Codes Validation

import pandas as pd
import glob

fund_file = glob.glob("Data/raw/*fund_master.csv")[0]
nav_file = glob.glob("Data/raw/*nav_history.csv")[0]

fund_df = pd.read_csv(fund_file)
nav_df = pd.read_csv(nav_file)

# Get unique AMFI codes
fund_codes = set(fund_df["amfi_code"].unique())
nav_codes = set(nav_df["amfi_code"].unique())

# Find missing codes
missing_codes = fund_codes - nav_codes

print("\n===== AMFI CODE VALIDATION =====")

print("Total Fund Master Codes:", len(fund_codes))
print("Total NAV History Codes:", len(nav_codes))

print("Missing AMFI Codes:", len(missing_codes))

if len(missing_codes) == 0:
    print("SUCCESS: All AMFI Codes are available in NAV History.")
else:
    print("Missing Codes:", missing_codes)
