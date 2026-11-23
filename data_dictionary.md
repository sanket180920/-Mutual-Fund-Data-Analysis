
# Mutual Fund Data Analysis - Data Dictionary

## 1. NAV History
| Column | Description |
|---|---|
| amfi_code | Unique mutual fund scheme code |
| date | NAV date |
| nav | Net Asset Value of the scheme |

## 2. Investor Transactions
| Column | Description |
|---|---|
| investor_id | Unique investor ID |
| scheme_name | Mutual fund scheme name |
| transaction_date | Transaction date |
| transaction_type | Type of transaction |
| amount_inr | Transaction amount in INR |
| city | Investor city |
| state | Investor state |
| kyc_status | Investor KYC verification status |

## 3. Fund Master
| Column | Description |
|---|---|
| amfi_code | Unique scheme code |
| fund_house | Mutual fund company |
| scheme_name | Scheme name |
| category | Fund category |
| sub_category | Fund sub-category |
| plan | Direct or Regular plan |
| launch_date | Scheme launch date |
| benchmark | Benchmark index |
| expense_ratio_pct | Expense ratio percentage |
| exit_load_pct | Exit load percentage |
| min_sip_amount | Minimum SIP amount |
| min_lumpsum_amount | Minimum lump sum amount |
| fund_manager | Fund manager name |
| risk_category | Risk classification |
| sebi_category_code | SEBI category code |

## 4. Portfolio Holdings
Contains information about mutual fund portfolio investments, such as scheme, stock, sector, and holding allocation.

## 5. Benchmark Indices
Contains historical benchmark index values and dates.

## 6. AUM by Fund House
| Column | Description |
|---|---|
| date | Reporting date |
| fund_house | Mutual fund company |
| aum_lakh_crore | AUM in lakh crore |
| aum_crore | AUM in crore |
| num_schemes | Number of schemes |

## 7. Monthly SIP Inflows
Contains monthly SIP investment inflow information and year-on-year growth.

## 8. Category Inflows
Contains mutual fund category-wise investment inflows.

## 9. Industry Folio Count
Contains mutual fund industry folio statistics and related monthly information.

## 10. Scheme Performance
Contains mutual fund scheme performance metrics such as returns, AUM, and expense ratio.

---

## Database Information

Database Name: bluestock_mf.db

Database Type: SQLite

Total Tables: 6

1. dim_fund
2. dim_date
3. fact_nav
4. fact_transactions
5. fact_performance
6. fact_aum
