# Mutual Fund Data Analysis

## Project Overview
This project focuses on collecting, processing, and analyzing mutual fund data using Python and data analytics tools.

## Objectives
- Collect mutual fund datasets.
- Perform data ingestion using Pandas.
- Fetch live NAV data using the MFAPI.
- Validate AMFI scheme codes.
- Perform data quality checks.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Requests
- Jupyter Notebook
- Git and GitHub

## Project Structure
```text
Mutual-Fund-Data-Analysis/
├── Data/
│   ├── raw/
│   └── processed/
├── Notebooks/
├── SQL/
├── Dashboard/
├── Reports/
├── data_ingestion.py
├── live_nav_fetch.py
├── requirements.txt
└── README.md
```

## Day 1 – Data Ingestion
- Loaded 10 mutual fund CSV datasets.
- Explored dataset shapes, data types, and missing values.
- Analyzed fund houses, categories, sub-categories, and risk categories.
- Validated AMFI scheme codes against NAV history.
- Fetched live NAV data for 6 mutual fund schemes.
- Prepared a data quality summary.

## Author
Sanket Jadhav

## GitHub Repository
https://github.com/sanket180920/-Mutual-Fund-Data-Analysis


# Mutual Fund Data Analysis

## Project Overview
This project focuses on analyzing Indian mutual fund data using Python, SQL, and data analysis techniques.

The objective is to clean, transform, store, and analyze mutual fund datasets to generate meaningful insights about fund performance, NAV trends, investor transactions, and Assets Under Management (AUM).

## Technologies Used
- Python
- Pandas
- NumPy
- SQL
- SQLite
- SQLAlchemy
- Jupyter Notebook
- Git and GitHub

## Project Structure
```text
Mutual-Fund-Data-Analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
├── SQL/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
├── reports/
├── clean_data.py
├── load_data.py
├── verify_data.py
├── run_queries.py
├── data_dictionary.md
├── bluestock_mf.db
├── requirements.txt
└── README.md
```

## Datasets
The project uses 10 datasets:
1. NAV History
2. Investor Transactions
3. Fund Master
4. Portfolio Holdings
5. Benchmark Indices
6. AUM by Fund House
7. Monthly SIP Inflows
8. Category Inflows
9. Industry Folio Count
10. Scheme Performance

## Data Cleaning
- Handled missing values.
- Checked duplicate records.
- Performed data type conversions.
- Created cleaned CSV files.
- Stored processed datasets in `data/processed/`.

## Database
- Database: SQLite
- Database file: `bluestock_mf.db`
- Total tables: 6

## SQL Analysis
10 SQL queries were prepared to analyze:
- Top mutual funds by AUM
- Fund house-wise AUM
- Best performing funds
- Category-wise returns
- Monthly average NAV
- Investor transactions
- City-wise investor analysis
- Risk-wise fund performance
- Expense ratio comparison
- Fund house-wise scheme count

## Project Deliverables
- 10 cleaned datasets
- SQLite database
- Database schema
- 10 SQL analysis queries
- Data dictionary

## Author
Sanket Jadhav
