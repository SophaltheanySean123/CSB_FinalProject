# ...existing code...
import tabula
import pandas as pd

# extract all tables from all pages
tables = tabula.read_pdf("sample.pdf", pages="all", multiple_tables=True)

# tables is a list of DataFrames — iterate, print and save each
for i, df in enumerate(tables, start=1):
    print(f"--- Table {i} (shape={df.shape}) ---")
    print(df)
    df.to_csv(f"table_{i}.csv", index=False)

# optional: concatenate if all tables share the same columns
if tables:
    try:
        combined = pd.concat(tables, ignore_index=True)
        combined.to_csv("tables_combined.csv", index=False)
    except ValueError:
        # different schemas — skip concatenation
        pass
# ...existing code...