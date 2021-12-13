import os
import glob
import pandas as pd
os.chdir("C:\\Users\\omar_\\Documents\\Code\\School\\CS_486\\CS-486\\Projects\\ClipItChat\\scored")


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

#export to csv
os.chdir("C:\\Users\\omar_\\Documents\\Code\\School\\CS_486\\CS-486\\Projects\\ClipItChat")
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')