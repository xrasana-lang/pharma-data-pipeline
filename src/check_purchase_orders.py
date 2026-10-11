# Check the cleaned Purchase_Orders against the original
# - read only, changes nothing
import pandas as pd

# Load both versions
# - raw = original Excel sheet
# - clean = saved Parquet file
raw = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Purchase_Orders")
clean = pd.read_parquet("data/processed/purchase_orders.parquet")

# Same size?
# - True means same rows and columns
print("same shape:", raw.shape == clean.shape)

# Same values, column by column?
# - raw[col] == clean[col] compares row by row
# - .all() is True only if every row matches
for col in raw.columns:
    same = (raw[col] == clean[col]).all()
    print(col, "unchanged:", same)