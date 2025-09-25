import polars as pl
import os


directory = "/Volumes/T7 Shield/Downloads"


files = [f for f in os.listdir(directory) if f.endswith(".csv") and not f.startswith(".")]

files = [os.path.join(directory, file) for file in files]

file = files[0]

df = pl.read_csv(file)

print(df.head())