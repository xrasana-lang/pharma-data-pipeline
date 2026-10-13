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