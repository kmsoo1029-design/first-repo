import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# 1) .env 불러오기
load_dotenv()
SERVER = os.getenv("SQL_SERVER", r"localhost\SQLEXPRESS")
PORT   = os.getenv("SQL_PORT", "1433")
DB     = os.getenv("SQL_DB_OLTP", "AdventureWorks2022")
AUTH   = os.getenv("SQL_AUTH", "windows").lower()
USER   = os.getenv("SQL_USERNAME")
PWD    = os.getenv("SQL_PASSWORD")

# 2) 인스턴스명/포트 처리
if "\\" in SERVER:   # 인스턴스명 포함 (예: localhost\SQLEXPRESS)
    SERVER_ADDR = SERVER
else:                # 그냥 서버명이면 포트 붙여줌
    SERVER_ADDR = f"{SERVER},{PORT}"

# 3) 연결 문자열
if AUTH == "windows":
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={SERVER_ADDR};Database={DB};"
        f"Trusted_Connection=yes;Encrypt=yes;TrustServerCertificate=yes;"
    )
else:
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={SERVER_ADDR};Database={DB};"
        f"Uid={USER};Pwd={PWD};Encrypt=yes;TrustServerCertificate=yes;"
    )

# 4) SQL 쿼리
sql = """
WITH SalesCTE AS (
  SELECT
    YEAR(soh.OrderDate) AS [Year],
    MONTH(soh.OrderDate) AS [Month],
    SUM(sod.OrderQty * sod.UnitPrice * (1 - sod.UnitPriceDiscount)) AS SalesAmount
  FROM Sales.SalesOrderHeader AS soh
  JOIN Sales.SalesOrderDetail  AS sod
    ON soh.SalesOrderID = sod.SalesOrderID
  GROUP BY YEAR(soh.OrderDate), MONTH(soh.OrderDate)
)
SELECT [Year], [Month], CAST(SalesAmount AS DECIMAL(18,2)) AS SalesAmount
FROM SalesCTE
ORDER BY [Year], [Month];
"""

# 5) 실행 및 시각화
with pyodbc.connect(conn_str) as conn:
    df = pd.read_sql(sql, conn)

print(df.head())  # 터미널에서 데이터 일부 확인

plt.figure(figsize=(9,4))
df["YM"] = df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2)
plt.plot(df["YM"], df["SalesAmount"], marker="o")
plt.xticks(rotation=60)
plt.title("AdventureWorks 2022: Monthly Sales")
plt.xlabel("Year-Month")
plt.ylabel("Sales Amount")
plt.tight_layout()
plt.savefig("oltp_monthly_sales.png", dpi=150)
plt.show()
