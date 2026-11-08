import sqlite3
import pandas as pd

#read in cleaned admissions data
df = pd.read_csv('data/admissions_cleaned.csv')

#connect to sqlite database
conn = sqlite3.connect('data/admissions.db')

#Store the data frame as a table in the database
df.to_sql('admissions', conn, if_exists='replace', index=False)

#Verify the import
print("Database created")
print(f"Imported {len(df)} rows into the admissions table.")

conn.close()