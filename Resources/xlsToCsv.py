import pandas as pd
import csv

# Load the Excel file (replace 'your_file.xlsx' with your actual file)
excel_file = '../Resources/tiles.xlsx'
df = pd.read_excel(excel_file)

# Save to CSV with ; as the delimiter
csv_file = '../Resources/tiles.csv'
df.to_csv(csv_file, sep=';', index=False, quoting=csv.QUOTE_NONE)

print(f"Successfully converted {excel_file} to {csv_file} with ';' as the delimiter.")


