# Reagents cleaning (decision D7)
# - reads the raw sheet, saves a cleaned Parquet file
import pandas as pd

# Load the sheet
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Reagents")

# Work on a copy
# - original df stays untouched
cleaned = df.copy()

# D7: missing hazard class
# - fill with "Unknown"
# - D8: existing labels are not touched
cleaned["Hazard_Class"] = cleaned["Hazard_Class"].fillna("Unknown")

# Save
# - write to data/processed as Parquet
cleaned.to_parquet("data/processed/reagents.parquet", index=False)

# Read it back and report
# - shape, hazard class counts, total missing values
check = pd.read_parquet("data/processed/reagents.parquet")
print(check.shape)
print(check["Hazard_Class"].value_counts())
print("missing values:", check.isna().sum().sum())
