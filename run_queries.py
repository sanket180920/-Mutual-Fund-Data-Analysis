
import pandas as pd
from sqlalchemy import create_engine

# Connect to SQLite Database
engine = create_engine("sqlite:///bluestock_mf.db")

# Read SQL Queries
with open("sql/queries.sql", "r") as file:
    sql_script = file.read()

# Split queries
queries = [
    query.strip()
    for query in sql_script.split(";")
    if query.strip()
]

# Execute each query
for i, query in enumerate(queries, start=1):

    print(f"\n========== QUERY {i} RESULT ==========")

    try:
        result = pd.read_sql_query(query, engine)
        print(result.to_string(index=False))

    except Exception as e:
        print("Error:", e)

print("\nAll SQL Queries Execution Completed!")
