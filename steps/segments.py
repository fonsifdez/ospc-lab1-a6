"""Number of orders per region, quarter and order size."""

# AI assistance: ChatGPT (OpenAI) suggested vectorized
# pandas operations instead of per-row Python processing.

import os
import pandas as pd

DATA = os.environ.get("DATA", os.path.expanduser("~/data/sales_2025.csv"))
OUT = os.environ.get("OUT", os.path.expanduser("~/data/out"))
os.makedirs(OUT, exist_ok=True)

orders = pd.read_csv(
    DATA,
    usecols=["order_date", "region", "quantity", "unit_price"]
)

quarter = pd.to_datetime(orders["order_date"]).dt.quarter
value = orders["quantity"] * orders["unit_price"]

size = pd.cut(
    value,
    bins=[float("-inf"), 100, 500, float("inf")],
    labels=["small", "medium", "large"],
    right=False
)

orders["segment"] = "Q" + quarter.astype(str) + " " + size.astype(str)

table = pd.crosstab(orders["region"], orders["segment"])
table.to_csv(os.path.join(OUT, "segments.csv"))

print("segments: done")
