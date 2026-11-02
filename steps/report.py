"""Revenue by region and month (revenue_by_region_month.csv)."""

import os
import pandas as pd

DATA = os.environ.get("DATA", os.path.expanduser("~/data/sales_2025.csv"))
OUT = os.environ.get("OUT", os.path.expanduser("~/data/out"))
os.makedirs(OUT, exist_ok=True)

totals = None

for chunk in pd.read_csv(
    DATA,
    usecols=["region", "order_date", "quantity", "unit_price"],
    chunksize=100_000
):
    months = pd.to_datetime(chunk["order_date"]).dt.month
    revenue = chunk["quantity"] * chunk["unit_price"]

    grouped = revenue.groupby([chunk["region"], months]).sum()
    totals = grouped if totals is None else totals.add(grouped, fill_value=0)

table = totals.unstack().round(2)
table.to_csv(os.path.join(OUT, "revenue_by_region_month.csv"))

print("report: done")
