
import requests
import pandas as pd
from pathlib import Path

schemes = {
    "HDFC_Top_100_Direct": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841"
}

output_dir = Path("Data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for scheme_name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        payload = response.json()
        df = pd.DataFrame(payload.get("data", []))

        df["scheme_code"] = code
        df["scheme_name"] = scheme_name

        file_path = output_dir / f"{scheme_name}_live_nav.csv"
        df.to_csv(file_path, index=False)

        print(f"SUCCESS: {scheme_name} - {len(df)} records saved")

    except Exception as error:
        print(f"ERROR: {scheme_name} - {error}")


# Step 7: Data Quality Summary

print("\n===== DATA QUALITY SUMMARY =====")

print("Total Fund Master Schemes:", len(fund_df))
print("Unique AMFI Codes:", fund_df["amfi_code"].nunique())
print("NAV History Records:", len(nav_df))
print("Missing AMFI Codes:", len(missing_codes))

print("\nMissing Values in Fund Master:")
print(fund_df.isnull().sum().sum())

print("\nMissing Values in NAV History:")
print(nav_df.isnull().sum().sum())

print("\nData Quality Observation:")
print("Monthly SIP Inflows has 12 missing values in yoy_growth_pct.")
print("These values should be investigated before analysis.")
