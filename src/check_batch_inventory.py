# Check the cleaned Batch_Inventory against the original
# - read only, changes nothing
import pandas as pd

# Load both versions
# - raw = original Excel sheet
# - clean = saved Parquet file
raw = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Batch_Inventory")
clean = pd.read_parquet("data/processed/batch_inventory.parquet")

# Same size?
# - rows only (clean has one extra column)
print("same rows:", len(raw) == len(clean))
print("new columns:", set(clean.columns) - set(raw.columns))

# Rows changed per column
# - a row counts as changed if the values differ
# - two missing values count as the same
for col in raw.columns:
    differs = ~((raw[col] == clean[col]) | (raw[col].isna() & clean[col].isna()))
    print(col, "rows changed:", differs.sum())
    