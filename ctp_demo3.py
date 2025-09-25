import polars as pl
import pandas as pd
import re
import os

def transpose_csv(input_file, output_file, transpose_columns):
    """
    Transpose specified columns from wide to long format.
    Groups columns by prefix (r, H, etc.) and year pattern.
    """
    
    # Read CSV and clean column names
    df = pl.read_csv(input_file)
    # df = df.rename({col: col.replace('\n', '').replace('\r', '') for col in df.columns})
    print(f"Original shape: {df.shape}")
    
    # Get ID columns (everything except transpose columns)
    id_columns = [col for col in df.columns if col not in transpose_columns]
    
    # Extract prefix and year from transpose columns
    column_info = {}
    for col in transpose_columns:
        year_match = re.search(r'\d{4}', col)
        if year_match:
            year = int(year_match.group())
            prefix = col.replace(year_match.group(), '')  # Remove year to get prefix
            if year not in column_info:
                column_info[year] = {}
            column_info[year][prefix] = col
    
    # Build result rows
    result_rows = []
    for row in df.iter_rows(named=True):
        for year in sorted(column_info.keys()):
            new_row = {col: row[col] for col in id_columns}  # Copy ID columns
            new_row['year'] = year
            
            # Add values for each prefix
            for prefix, col_name in column_info[year].items():
                new_row[prefix] = row[col_name]
            
            result_rows.append(new_row)

    print(result_rows[:2])
    
    # Create result dataframe
    df_long = pd.DataFrame(result_rows)
    
    print(f"Transposed shape: {df_long.shape}")
    print("\nPreview:")
    print(df_long.head(10))
    
    # Export
    df_long.to_csv(output_file, index=False)
    print(f"\nExported to {output_file}")

# Example usage
if __name__ == "__main__":
    # Create sample data
    # input_file = '/Volumes/T7 Shield/Downloads/ITA_PANEL_5001_10000.csv'


    directory = "/Volumes/T7 Shield/Downloads"


    files = [f for f in os.listdir(directory) if f.endswith(".csv") and not f.startswith(".")]

    files = [os.path.join(directory, file) for file in files]
    
    # Specify which columns to transpose
    # columns_to_transpose = ["r2000", "r2001", "r2002"]

    for input_file in files:
        output_file = os.path.join(directory, f"TS_{os.path.basename(input_file)}")
        df = pl.read_csv(input_file)

        colnames = df.columns

        columns_to_transpose = [col for col in colnames if "Totale valore della produzione migl USD" in col or 'Numero dipendenti' in col or 'Fatturato' in col]
        
        # print(columns_to_transpose)
        
        transpose_csv(input_file, output_file, columns_to_transpose)
        
        # Show result
        # result = pl.read_csv("output.csv")
        # print("\nFinal result:")
        # print(result)