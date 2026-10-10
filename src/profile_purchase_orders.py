# This script looks at the Purchase_Orders sheet. It does not change anything.
import pandas as pd

# Open the Excel file and load the Purchase_Orders sheet into a table called df.
# The path starts from the project folder, so run the script from there.
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Purchase_Orders")

# Show how many rows and columns the table has.
print(df.shape)

# Show each column's name, its type (number or text), and how many values are filled in.
df.info()

# Show the first 5 rows so we can see what the data looks like.
print(df.head().to_string())

# Date shapes
# - digit -> 9, letter -> A
# - leaves only the shape of each date
# - count how often each shape appears
shape = df["Order_Date"].str.replace(r"\d", "9", regex=True).str.replace(r"[A-Za-z]", "A", regex=True)
print(shape.value_counts())

# Slash dates
# - keep only rows with "/"
# - split into first and second number
# - count how often each is above 12
slash = df[df["Order_Date"].str.contains("/")]
parts = slash["Order_Date"].str.split("/", expand=True).astype(int)
print("first number above 12:", (parts[0] > 12).sum())
print("second number above 12:", (parts[1] > 12).sum())