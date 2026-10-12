# Check the cleaned Purchase_Orders against the original
# - read only, changes nothing
import pandas as pd

# Load both versions
# - raw = original Excel sheet
# - clean = saved Parquet file
raw = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Purchase_Orders")
clean = pd.read_parquet("data/processed/purchase_orders.parquet")

# Same size?
# - rows only (clean has extra columns)
print("same rows:", len(raw) == len(clean))
print("new columns:", set(clean.columns) - set(raw.columns))

# Rows changed per column
# - a row counts as changed if the values differ
# - two missing values count as the same
for col in raw.columns:
    differs = ~((raw[col] == clean[col]) | (raw[col].isna() & clean[col].isna()))
    print(col, "rows changed:", differs.sum())
    