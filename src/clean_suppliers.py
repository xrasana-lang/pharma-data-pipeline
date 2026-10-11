# Suppliers cleaning (decisions D1 and D2)
# - reads the raw sheet, saves a cleaned Parquet file
import pandas as pd

# Load the sheet
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Suppliers")

# Work on a copy
# - original df stays untouched
cleaned = df.copy()

# D1: Merck spellings
# - rename "Merck SA" and "MERCK" to "Merck"
# - D2: Country is not touched
cleaned["Supplier_Name"] = cleaned["Supplier_Name"].replace({"Merck SA": "Merck", "MERCK": "Merck"})

# Save
# - write to data/processed as Parquet
cleaned.to_parquet("data/processed/suppliers.parquet", index=False)

# Read it back and report
# - shape, names after cleaning, rows renamed
check = pd.read_parquet("data/processed/suppliers.parquet")
print(check.shape)
print(check["Supplier_Name"].value_counts())
print("rows renamed:", (df["Supplier_Name"] != check["Supplier_Name"]).sum())
