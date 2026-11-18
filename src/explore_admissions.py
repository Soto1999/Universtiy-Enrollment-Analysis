import pandas as pd

df = pd.read_excel('data/admissions.xlsx')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 200)

for index, row in df.iterrows():
    print(f"Row {index}: {row.tolist()}")

print("\n")

#Selecting Relevant Columns
admissions = df.iloc[7:10].copy()

admissions.columns = [
    "category", "applicants", "admitted", "enrolled_full_time", "enrolled_part_time"
]

admissions = admissions.reset_index(drop=True)

admissions["admission_rate"] = (admissions["admitted"] / admissions["applicants"] * 100).round(2)

admissions["enrolled_total"] = admissions["enrolled_full_time"] + admissions["enrolled_part_time"]

admissions["yield_rate"] = (admissions["enrolled_total"] / admissions["admitted"] * 100).round(2)

print(admissions.to_string(index=False))

admissions.to_csv('data/admissions_cleaned.csv', index=False)
print("\nCleaned admissions and saved data")