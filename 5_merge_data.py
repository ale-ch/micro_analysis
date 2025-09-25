import os
import pandas as pd

directory = "/Volumes/T7 Shield/Downloads/panel_data"

files = [f for f in os.listdir(directory) if f.endswith(".csv") and not f.startswith(".") and f.startswith("clean")]

files = [os.path.join(directory, file) for file in files]

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

print(df.shape)
print(df.columns)

output_file = os.path.join(directory, "ITA_PANEL.csv")

df.to_csv(output_file, index=False)