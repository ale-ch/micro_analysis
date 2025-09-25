import polars as pl
import re

def transpose_csv(input_file, output_file, transpose_columns):
    """
    Transpose specified columns from wide to long format.
    Extracts year from column names using regex pattern.
    """
    
    # Read CSV
    df = pl.read_csv(input_file)
    print(f"Original shape: {df.shape}")
    
    # Get ID columns (everything except transpose columns)
    id_columns = [col for col in df.columns if col not in transpose_columns]
    
    # Melt to long format
    df_long = df.melt(
        id_vars=id_columns,
        value_vars=transpose_columns,
        variable_name="column_name",
        value_name="value"
    )
    
    # Extract year from column name using regex
    df_long = df_long.with_columns(
        pl.col("column_name").map_elements(
            lambda x: int(re.search(r'\d{4}', x).group()) if re.search(r'\d{4}', x) else None,
            return_dtype=pl.Int64
        ).alias("year")
    )#.drop("column_name")
    
    print(f"Transposed shape: {df_long.shape}")
    print("\nPreview:")
    print(df_long.head(10))
    
    # Export
    df_long.write_csv(output_file)
    print(f"\nExported to {output_file}")

# Example usage
if __name__ == "__main__":
    # Create sample data
    #sample_data = """name,address,r2000,r2001,r2002,other_col
#a,adda,283,8549,1283,keep1
#b,addb,47385,47,84,keep2"""
    
    #with open("input.csv", 'w') as f:
    #   f.write(sample_data)

    input_file = '/Volumes/T7 Shield/Downloads/ITA_PANEL_5001_10000.csv'
    
    # Specify which columns to transpose
    # columns_to_transpose = ["r2000", "r2001", "r2002"]

    df = pl.read_csv(input_file)

    colnames = df.columns

    columns_to_transpose = [col for col in colnames if "Totale valore della produzione migl USD" in col or 'Numero dipendenti' in col or 'Fatturato' in col]
    
    print(columns_to_transpose)
    
    transpose_csv(input_file, "output.csv", columns_to_transpose)
    
    # Show result
    result = pl.read_csv("output.csv")
    print("\nFinal result:")
    print(result)