# Batch_Inventory profiling
# - read only, changes nothing
import pandas as pd

# Load the sheet
# - file: Ubuntu_Pharma_Inventory_Dataset.xlsx
# - sheet: Batch_Inventory
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Batch_Inventory")

# Size
# - rows, columns
print(df.shape)

# Column types
# - name, type, filled-in count
df.info()

# First look
# - first 5 rows, all columns
print(df.head().to_string())
# Missing values
# - count per column
print(df.isna().sum())

# Status counts
# - how many batches in each status
print(df["Current_Status"].value_counts())

# Expiry range per status
# - group rows by status
# - show earliest and latest Expiry_Date in each group
print(df.groupby("Current_Status")["Expiry_Date"].agg(["min", "max"]))

# Dates in the wrong order
# - Expiry_Date on or before Manufacture_Date
print("expiry not after manufacture:", (df["Expiry_Date"] <= df["Manufacture_Date"]).sum())
# Bad date order rows
# - Expiry_Date on or before Manufacture_Date
# - show every one of them
bad = df[df["Expiry_Date"] <= df["Manufacture_Date"]]
print(bad.to_string())

# Split the 14
# - strictly before vs same day
print("expiry before manufacture:", (df["Expiry_Date"] < df["Manufacture_Date"]).sum())
print("expiry same day as manufacture:", (df["Expiry_Date"] == df["Manufacture_Date"]).sum())
# Shelf life check
# - load Reagents to get Shelf_Life_Days
# - join onto batches by Reagent_ID
reagents = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Reagents")
merged = df.merge(reagents[["Reagent_ID", "Shelf_Life_Days"]], on="Reagent_ID", how="left")

# Actual life of each batch
# - days from manufacture to expiry
merged["life_days"] = (merged["Expiry_Date"] - merged["Manufacture_Date"]).dt.days

# Compare with the reagent's shelf life
# - batches with no matching reagent
# - rows where life equals shelf life, and rows where it differs
print("no matching reagent:", merged["Shelf_Life_Days"].isna().sum())
print("life equals shelf life:", (merged["life_days"] == merged["Shelf_Life_Days"]).sum())
print("life differs from shelf life:", (merged["life_days"] != merged["Shelf_Life_Days"]).sum())

# The 14 bad rows
# - show their life vs shelf life
bad_rows = merged[merged["Expiry_Date"] <= merged["Manufacture_Date"]]
print(bad_rows[["Batch_ID", "life_days", "Shelf_Life_Days"]].to_string())
# Difference between life and shelf life
# - life_days minus Shelf_Life_Days
# - 0 means they match
# - count how often each difference appears
merged["diff"] = merged["life_days"] - merged["Shelf_Life_Days"]
print(merged["diff"].value_counts().head(15))
