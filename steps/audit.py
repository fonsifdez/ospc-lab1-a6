"""Audit trail: one line per order with its revenue."""

# AI assistance: ChatGPT (OpenAI) suggested replacing repeated
# file opens with a single buffered output file.
import os
import pandas as pd

DATA = os.environ.get("DATA", os.path.expanduser("~/data/sales_2025.csv"))
OUT = os.environ.get("OUT", os.path.expanduser("~/data/out"))
os.makedirs(OUT, exist_ok=True)

path = os.path.join(OUT, "audit_2025.csv")
count = 0

with open(path, "w") as f:
    for chunk in pd.read_csv(
        DATA,
        usecols=["order_id", "region", "quantity", "unit_price"],
        chunksize=100_000
    ):
        chunk["revenue"] = chunk["quantity"] * chunk["unit_price"]

        for order in chunk.itertuples(index=False):
            f.write(f"{order.order_id},{order.region},{order.revenue:.2f}\n")

        count += len(chunk)

print(f"audit: {count:,} lines written")
