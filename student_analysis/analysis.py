import pandas as pd
import numpy as np


# 1. LOAD DATASET
df = pd.read_csv("STUDENT.csv")


# 2. BASIC INFORMATION
print("\n--- BASIC INFO ---")
print(df.info())

print("\n--- FIRST 5 RECORDS ---")
print(df.head())


# 3. DATA CLEANING
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# Fill missing values
df["AGE"].fillna(df["AGE"].mean(), inplace=True)
df["ATTENDANCE"].fillna(df["ATTENDANCE"].mean(), inplace=True)
df["EXAM SCORE"].fillna(df["EXAM SCORE"].mean(), inplace=True)

print("\nMissing values handled.\n")


# 4. DESCRIPTIVE STATISTICS
print("\n--- DESCRIPTIVE STATISTICS ---")
print(df.describe())


# 5. NUMPY OPERATIONS
print("\n--- NUMPY ANALYSIS ---")

scores = np.array(df["EXAM SCORE"])
attendance = np.array(df["ATTENDANCE"])

print("Max Score:", np.max(scores))
print("Min Score:", np.min(scores))
print("Average Score:", np.mean(scores))
print("Standard Deviation:", np.std(scores))


# 6. GROUP BY ANALYSIS
print("\n--- GROUP ANALYSIS ---")

print("\nAverage Score by Tuition:")
print(df.groupby("TUTION")["EXAM SCORE"].mean())

print("\nAverage Score by Health:")
print(df.groupby("HEALTH")["EXAM SCORE"].mean())

print("\nAverage Score by Stress:")
print(df.groupby("STRESS")["EXAM SCORE"].mean())

print("\nAverage Score by Daily Work:")
print(df.groupby("DAILY WORK")["EXAM SCORE"].mean())


# 7. SORTING & FILTERING
print("\n--- TOP PERFORMERS ---")
top_students = df.sort_values(by="EXAM SCORE", ascending=False)
print(top_students.head())

print("\n--- LOW PERFORMERS ---")
low_students = df.sort_values(by="EXAM SCORE")
print(low_students.head())

print("\n--- STUDENTS WITH HIGH ATTENDANCE (>85%) ---")
print(df[df["ATTENDANCE"] > 85])


# 8. CORRELATION ANALYSIS
print("\n--- CORRELATION MATRIX ---")
correlation = df.corr(numeric_only=True)
print(correlation)


# 9. CUSTOM ANALYSIS
print("\n--- CUSTOM INSIGHTS ---")

high_study = df[df["SELF STUDY"] > 3]["EXAM SCORE"].mean()
low_study = df[df["SELF STUDY"] <= 3]["EXAM SCORE"].mean()

print("Avg Score (High Study):", high_study)
print("Avg Score (Low Study):", low_study)

more_games = df[df["VIDEO GAMES"] > 2]["EXAM SCORE"].mean()
less_games = df[df["VIDEO GAMES"] <= 2]["EXAM SCORE"].mean()

print("Avg Score (More Gaming):", more_games)
print("Avg Score (Less Gaming):", less_games)


# 10. VALUE COUNTS (CATEGORICAL ANALYSIS)
print("\n--- CATEGORY COUNTS ---")

print("\nTuition Count:")
print(df["TUTION"].value_counts())

print("\nHealth Count:")
print(df["HEALTH"].value_counts())

print("\nStress Count:")
print(df["STRESS"].value_counts())


# 11. ADD NEW COLUMN (FEATURE ENGINEERING)
df["PERFORMANCE LEVEL"] = np.where(df["EXAM SCORE"] >= 75, "GOOD", "AVERAGE")

print("\n--- UPDATED DATA WITH PERFORMANCE LEVEL ---")
print(df.head())


# 12. SAVE CLEANED DATA
df.to_csv("cleaned_student_data.csv", index=False)

print("\nCleaned dataset saved as 'cleaned_student_data.csv'")

