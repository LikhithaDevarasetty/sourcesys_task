import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("STUDENT.csv")

print("Original Data:\n", df.head())

#  1. Check Missing Values
print("\nMissing Values:\n", df.isnull().sum())


#  2. Handle Missing Values
# Numerical columns
df["AGE"] = df["AGE"].fillna(df["AGE"].mean()).round().astype(int)
df["ATTENDANCE"] = df["ATTENDANCE"].fillna(df["ATTENDANCE"].mean()).round().astype(int)
df["EXAM SCORE"] = df["EXAM SCORE"].fillna(df["EXAM SCORE"].median()).astype(int)

# Replace missing with default values
df["VIDEO GAMES"] = df["VIDEO GAMES"].fillna(0).round().astype(int)
df["SELF STUDY"] = df["SELF STUDY"].fillna(0).astype(int)

# Categorical columns
df["TUTION"] = df["TUTION"].fillna("no")
df["HEALTH"] = df["HEALTH"].fillna("UNKNOWN")
df["STRESS"] = df["STRESS"].fillna("UNKNOWN")


#  3. Remove Duplicates
print("\nDuplicate Rows:", df.duplicated().sum())
df = df.drop_duplicates()


#  4. Standardize Data
# Convert text to uppercase for consistency
df["HEALTH"] = df["HEALTH"].str.lower()
df["STRESS"] = df["STRESS"].str.lower()
df["TUTION"] = df["TUTION"].str.lower()


#  5. Fix Data Types
df["AGE"] = df["AGE"].astype(int)
df["ATTENDANCE"] = df["ATTENDANCE"].astype(int)



#  6. Outlier Check 
print("\nScore Range:", df["EXAM SCORE"].min(), "-", df["EXAM SCORE"].max())


#  7. Final Clean Dataset

print("\nCleaned Data:\n", df.head())

print("\nFinal Missing Values:\n", df.isnull().sum())

df.to_csv("cleaned_student_data.csv", index=False)
