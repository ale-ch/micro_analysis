import os
import pickle
import polars as pl
import pandas as pd
import dask.dataframe as dd


def convert_xlsx_to_csv(input_file: str, output_file: str, write=False) -> pl.DataFrame:
    df = pl.read_excel(input_file, sheet_id=2)

    if write:
        df = df.rename({col: col.replace('\n', ' ').replace('\r', '') for col in df.columns})
        df[:,1:].write_csv(output_file)

    return df

directory = "/Volumes/T7 Shield/Downloads"

files = [f for f in os.listdir(directory) if f.endswith(".xlsx") and not f.startswith(".")]

for file in files:

    input_path = os.path.join(directory, file)

    size = os.path.getsize(input_path)

    print(input_path)
    print(size)

    output_file = os.path.splitext(input_path)[0] + ".csv"
    # output_file_pkl = os.path.splitext(input_path)[0] + ".pkl"
    output_file_parquet = os.path.splitext(input_path)[0] + ".parquet"

    print(output_file)
    pl_df = convert_xlsx_to_csv(input_path, output_file, write=True)

    # pd_df = pl_df.to_pandas()
# 
    # # Convert Pandas DF to Dask DF
    # dd_df = dd.from_pandas(pd_df, npartitions=10)  # adjust partitions as needed
# 
    # # Save to Parquet
    # dd_df.to_parquet(output_file_parquet, engine="pyarrow", write_index=False)

