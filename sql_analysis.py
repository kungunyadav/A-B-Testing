import sqlite3
import pandas as pd

df = pd.read_csv("ab_test_data.csv")

conn = sqlite3.connect(":memory:")
df.to_sql("ab_test_data", conn, index=False, if_exists="replace")

query = """
SELECT
    "group",
    COUNT(*) AS total_users,
    SUM(converted) AS total_conversions,
    ROUND(100.0 * SUM(converted) / COUNT(*), 2) AS conversion_rate_pct,
    ROUND(AVG(time_on_page_sec), 1) AS avg_time_on_page_sec
FROM ab_test_data
GROUP BY "group";
"""

result = pd.read_sql_query(query, conn)
print(query)
print(result.to_string(index=False))

result.to_csv("sql_summary.csv", index=False)
conn.close()