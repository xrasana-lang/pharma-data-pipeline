# Purchase_Orders: test the Order_Date parsing (decision D3)
# - read only, nothing is saved yet
import pandas as pd

# Load the sheet
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Purchase_Orders")

# Try each format on every row
# - a row that doesn't match becomes NaT (missing date)
# - errors="coerce" means "don't crash, mark it missing"
iso = pd.to_datetime(df["Order_Date"], format="%Y-%m-%d", errors="coerce")
slash = pd.to_datetime(df["Order_Date"], format="%d/%m/%Y", errors="coerce")
named = pd.to_datetime(df["Order_Date"], format="%d-%b-%Y", errors="coerce")

# How many rows did each format fail on?
print("iso missing:", iso.isna().sum())
print("slash missing:", slash.isna().sum())
print("named missing:", named.isna().sum())

# Combine
# - fillna(x) fills the gaps in one result with values from x
parsed = iso.fillna(slash).fillna(named)
print("still missing after combining:", parsed.isna().sum())

# Check the parsed dates (decision D3)
# - gap = Expected_Delivery_Date minus parsed Order_Date
# - negative gap = delivery before the order (suspicious)
gap = (df["Expected_Delivery_Date"] - parsed).dt.days
print(gap.describe())
print("negative gaps:", (gap < 0).sum())

# Save the cleaned table
# - copy df so the original stays untouched
# - replace Order_Date with the parsed dates
# - write to data/processed as Parquet
cleaned = df.copy()
cleaned["Order_Date"] = parsed
cleaned.to_parquet("data/processed/purchase_orders.parquet", index=False)

# Read it back to prove it worked
# - check shape and column types
check = pd.read_parquet("data/processed/purchase_orders.parquet")
print(check.shape)
print(check.dtypes)