import glob
import pandas as pd

extension = 'csv'
scored_dir = 'scored'

list_of_csv_files = glob.glob(scored_dir + '/*.csv')
list_of_csv_files.sort()

df = pd.concat(map(pd.read_csv, list_of_csv_files), ignore_index=True)
df.drop(["Unnamed: 0", 'created_at'],inplace=True, axis=1)
df.to_csv("combined/combined_csv.csv")