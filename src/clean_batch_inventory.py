# Batch_Inventory cleaning (decisions D4 and D5)
# - reads the raw sheet, saves a cleaned Parquet file
import pandas as pd

# Load the sheet
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Batch_Inventory")

# Work on a copy
# - original df stays untouched
cleaned = df.copy()

# D4: bad expiry dates
# - flag rows where Expiry_Date is before Manufacture_Date
# - blank the date on those rows
bad_expiry = cleaned["Expiry_Date"] < cleaned["Manufacture_Date"]
cleaned["Expiry_Date_Flag"] = bad_expiry
cleaned.loc[bad_expiry, "Expiry_Date"] = pd.NaT

# D5: missing lot numbers
# - fill with "Unknown"
# - Storage_Location is left alone on purpose
cleaned["Lot_Number"] = cleaned["Lot_Number"].fillna("Unknown")

# Save
# - write to data/processed as Parquet
cleaned.to_parquet("data/processed/batch_inventory.parquet", index=False)

# Read it back and report
# - shape, flagged rows, missing values
check = pd.read_parquet("data/processed/batch_inventory.parquet")
print(check.shape)
print("flagged rows:", check["Expiry_Date_Flag"].sum())
print(check.isna().sum())
