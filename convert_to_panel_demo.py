import polars as pl
import os

def transpose_csv(input_file, output_file):
    """
    Transpose CSV from wide format to long format.
    
    Wide format: name, address, r2000, r2001, r2002
    Long format: name, address, r, year
    """
    
    print("Reading CSV file...")
    try:
        # Read the CSV file
        df = pl.read_csv(input_file)
        print(f"Original data shape: {df.shape}")
        print("Original data preview:")
        print(df.head())
        
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False
    
    print("\nTransposing data...")
    
    # Identify year columns (columns that start with 'r' followed by digits)
    year_columns = [col for col in df.columns if col.startswith('r') and col[1:].isdigit()]
    non_year_columns = [col for col in df.columns if col not in year_columns]
    
    print(f"Year columns found: {year_columns}")
    print(f"ID columns: {non_year_columns}")
    
    # Melt the dataframe to convert from wide to long format
    df_long = df.melt(
        id_vars=non_year_columns,
        value_vars=year_columns,
        variable_name="year_col",
        value_name="r"
    )
    
    # Extract year from the column name (remove 'r' prefix)
    df_long = df_long.with_columns(
        pl.col("year_col").str.slice(1).cast(pl.Int64).alias("year")
    ).drop("year_col")
    
    # Reorder columns to match desired output
    df_long = df_long.select([
        *non_year_columns,  # name, address, etc.
        "r",
        "year"
    ])
    
    print(f"\nTransposed data shape: {df_long.shape}")
    print("Transposed data preview:")
    print(df_long.head(10))
    
    # Quality checks
    print("\n" + "="*50)
    print("QUALITY CHECKS")
    print("="*50)
    
    # Check 1: No missing values in key columns
    missing_check = df_long.null_count()
    print("Missing values per column:")
    print(missing_check)
    
    # Check 2: Data type validation
    print(f"\nData types:")
    print(df_long.dtypes)
    
    # Check 3: Year range validation
    year_stats = df_long.select("year").describe()
    print(f"\nYear statistics:")
    print(year_stats)
    
    # Check 4: Row count validation
    expected_rows = len(df) * len(year_columns)
    actual_rows = len(df_long)
    print(f"\nRow count validation:")
    print(f"Expected rows: {expected_rows}")
    print(f"Actual rows: {actual_rows}")
    row_count_ok = expected_rows == actual_rows
    print(f"Row count matches: {row_count_ok}")
    
    # Check 5: No duplicate combinations of ID columns + year
    id_cols_with_year = non_year_columns + ["year"]
    duplicates = df_long.group_by(id_cols_with_year).len().filter(pl.col("len") > 1)
    duplicate_check = len(duplicates) == 0
    print(f"\nDuplicate check:")
    print(f"No duplicate (ID + year) combinations: {duplicate_check}")
    
    # Check 6: Value range validation for 'r' column
    r_stats = df_long.select("r").describe()
    print(f"\n'r' column statistics:")
    print(r_stats)
    
    # Overall quality assessment
    all_checks_passed = (
        missing_check.select(pl.sum_horizontal(pl.all())).item() == 0 and  # No missing values
        row_count_ok and
        duplicate_check
    )
    
    print(f"\n" + "="*50)
    print(f"OVERALL QUALITY ASSESSMENT: {'PASSED' if all_checks_passed else 'FAILED'}")
    print("="*50)
    
    if all_checks_passed:
        print(f"\nExporting to {output_file}...")
        try:
            df_long.write_csv(output_file)
            print(f"Successfully exported transposed data to {output_file}")
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False
    else:
        print("Quality checks failed. Not exporting the file.")
        print("Please review the data and fix any issues before proceeding.")
        return False

# Example usage
if __name__ == "__main__":
    # Create sample input file for demonstration
    sample_data = """name,address,r2000,r2001,r2002
a,adda,283,8549,1283
b,addb,47385,47,84"""
    
    input_file = "input_data.csv"
    output_file = "transposed_data.csv"
    
    # Write sample data to file
    with open(input_file, 'w') as f:
        f.write(sample_data)
    
    # Run the transpose function
    success = transpose_csv(input_file, output_file)
    
    if success:
        print(f"\nFinal output preview:")
        result_df = pl.read_csv(output_file)
        print(result_df)
    
    # Clean up sample files (optional)
    # os.remove(input_file)
    # if success:
    #     os.remove(output_file)