# Read the Data_Dictionary sheet to find out what each column is meant to record.
import pandas as pd

# Path is relative, so run this from the project root.
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Data_Dictionary")

print(df.shape)       # (rows, columns)
print(df.columns)     # what the dictionary records about each column
print(df.to_string()) # to_string() prints every row, with nothing hidden by "..."