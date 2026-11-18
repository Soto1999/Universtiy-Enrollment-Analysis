import pandas as pd

file_path = 'data/enrollment_2024.xlsx'

excel_file = pd.ExcelFile(file_path)

print("Available sheets:")
print(excel_file.sheet_names)

df = pd.read_excel(file_path, header=7)
df = df.rename(columns={"Unnamed: 0": "category"})
df = df.dropna(subset=["Total"])
df["category"] = df["category"].str.strip()
df = df.reset_index(drop=True)

# Add a new column for attendance status
df["attendance_status"] = None
status = "All"

#In this section because the data is cumulative, we will need to find the start of each category and assign the
#correct attendance staus to each row. We will assign the "All students" row since it is a summary of all students and cannot
#be assigned a specific attendance status.
for index, row in df.iterrows():

    if row["category"] == "Full-time students":
        status = "Full-time"
    elif row["category"] == "Part-time students":
        status = "Part-time"
    
    df.loc[index, "attendance_status"] = status

df["student_level"] = None
level = "All"
#In this section because the data is cumulative, we will need to find the start of each category and assign the
#the correct studend level. We will assign the summerized line to "All" since it cannot be assigned a specific type.
for index, row in df.iterrows():
    if row["category"] in ["All students", "Full-time students", "Part-time students"]:
        level = "All"
    elif row["category"] == "Undergraduate":
        level = "Undergraduate"
    elif row["category"] == "Graduate":
        level = "Graduate"
    df.loc[index, "student_level"] = level

df["degree_status"] = None
degree_status = "All"

#In this section we are assiging degree status, we will need to loop the through the rows until we the start of a category
#such as "Degree/certificate seeking" then keep asigning that status until we hit a generalized line such as "All students"
for index, row in df.iterrows():
    if row['category'] in ["All students", "Full-time students", "Part-time students", "Undergraduate", "Graduate"]:
        degree_status = None
    elif row['category'] in ["Degree/certificate seeking", "Nondegree/certificate seeking"]:
        degree_status = row['category']
    df.loc[index, "degree_status"] = degree_status

df["entry_type"] = None
#in this section we are checking each line to see the entry type, if a valid type we will assign it to the entry_type column for 
#each row
for index, row in df.iterrows():
    if row["category"] in ["First-time", "Transfer-ins" , "Continuing"]:
        df.loc[index, "entry_type"] = row["category"]

df["row_type"] = "leaf"
#Here we seperate sub totals and totals. We check to see if the row in a known subtotal or total and asign that correct value
#everything else defaults to leaf 
for index, row in df.iterrows():
    if row["category"] == "All students":
        df.loc[index, "row_type"] = "Total"
    elif row["category"] in ["Full-time students", "Part-time students", "Undergraduate", "Degree/certificate seeking"]:
        df.loc[index, "row_type"] = "Subtotal"

print(df[["category", "Total"]].to_string(index=False))

print("\n All enrollment data:")
print(df.to_string(index=False))

#DATA validation
#Here we create a new data frame that filters for rows that are leaf in the All attendence_status sections
#to prevent double counting
leafs = df[
    (df["attendance_status"] == "All") & (df["row_type"] == "leaf")
]
leaf_total = leafs["Total"].sum()

#Using the leafed data frame we than sum up men and women enrollment totals
male_total = leafs["Men"].sum()
female_total = leafs["Women"].sum()

#To sum part and full time student, we need to refer back to the original datafarme
#to have access back to full and part time sections
for status in ["Full-time", "Part-time"]: 
    students = df[
        (df["attendance_status"] == status) & (df["row_type"] == "leaf")
    ]
    print(status, students["Total"].sum())

#Validate the the enrollment totals matcht the published totals to check for classification
#erros and we are ready to push this data to SQL
print("Male enrollment: ", male_total)
print("Female enrollment: ", female_total)
print("Combined enrollment: " , male_total + female_total)
print("Calculated enrollment:", leaf_total)

#Here is a final check to make sure totals match
published_total = df.loc[df["category"] == "All students", "Total"].iloc[0]

assert leaf_total == published_total
print(df.shape)
