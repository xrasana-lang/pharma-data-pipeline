# Waste_Transactions profiling
# - read only, changes nothing
import pandas as pd

# Load the sheet
# - file: Ubuntu_Pharma_Inventory_Dataset.xlsx
# - sheet: Waste_Transactions
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Waste_Transactions")

# Size
# - rows, columns
print(df.shape)

# Column types
# - name, type, filled-in count
df.info()

# First look
# - first 5 rows, all columns
print(df.head().to_string())

# Duplicate keys
# - 0 means every Waste_ID appears once
print("duplicate Waste_ID:", df["Waste_ID"].duplicated().sum())

# Waste reasons
# - each reason with its row count
print(df["Waste_Reason"].value_counts())

# Departments
# - each department with its row count
print(df["Department"].value_counts())

# Number ranges
# - min and max show zeros or negatives
print(df[["Quantity_Wasted", "Waste_Cost_ZAR"]].describe())

# Date range
# - earliest and latest waste date
print(df["Date"].min(), df["Date"].max())
