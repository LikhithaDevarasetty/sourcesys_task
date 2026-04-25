import pandas as pd
import numpy as np

# ==========================================
# LOAD ORIGINAL DATASET
# ==========================================
df_original = pd.read_csv("STUDENT.csv")   # ⚠️ check file name/path

print("Initial Data:\n", df_original.head())

# =========================================================
# COMMON CLEANING FUNCTION (FULL CLEANING)
# =========================================================
def clean_data(df):
    df = df.copy()

    # Numerical columns
    df["AGE"] = df["AGE"].fillna(df["AGE"].mean()).round().astype(int)
    df["ATTENDANCE"] = df["ATTENDANCE"].fillna(df["ATTENDANCE"].mean()).round().astype(int)
    df["EXAM SCORE"] = df["EXAM SCORE"].fillna(df["EXAM SCORE"].median()).round().astype(int)
    df["VIDEO GAMES"] = df["VIDEO GAMES"].fillna(0)
    df["SELF STUDY"] = df["SELF STUDY"].fillna(0)

    # Categorical columns
    df["TUTION"] = df["TUTION"].fillna("no")
    df["HEALTH"] = df["HEALTH"].fillna("UNKNOWN")
    df["STRESS"] = df["STRESS"].fillna("UNKNOWN")

    return df


# =========================================================
# 1. OPERATIONS
# =========================================================
print("\n========== OPERATIONS ==========")

df = clean_data(df_original)

# Basic Inspection
print("\nShape:", df.shape)
print("\nColumns:", df.columns)
print("\nData Types:\n", df.dtypes)
print("\nSummary:\n", df.describe())

# Missing Values Check
print("\nMissing Values AFTER CLEANING:\n", df.isnull().sum())

# Column Selection
print("\nSelected Columns:\n", df[["NAME", "EXAM SCORE"]].head())

# Sorting
print("\nTop Students (Sorted):\n",
      df.sort_values("EXAM SCORE", ascending=False).head())

# Mathematical Operations
print("\nMean Score:", df["EXAM SCORE"].mean())
print("Max Score:", df["EXAM SCORE"].max())
print("Min Score:", df["EXAM SCORE"].min())

# Grouping & Aggregation
print("\nAvg Score by Tuition:\n",
      df.groupby("TUTION")["EXAM SCORE"].mean())

print("\nAvg Score by Health:\n",
      df.groupby("HEALTH")["EXAM SCORE"].mean())

# Feature Engineering
df["PERFORMANCE"] = df["EXAM SCORE"].apply(
    lambda x: "Excellent" if x > 90 else "Average" if x > 70 else "Poor"
)

df["STATUS"] = np.where(df["EXAM SCORE"] > 75, "Pass", "Fail")

# Duplicate Handling
print("\nDuplicate Rows:", df.duplicated().sum())

#  Rename Column
df = df.rename(columns={"EXAM SCORE": "SCORE"})


# =========================================================
# 2. FILTERS
# =========================================================
print("\n========== FILTERS ==========")

df = clean_data(df_original)
df = df.rename(columns={"EXAM SCORE": "SCORE"})

# Single Condition
print("\nHigh Scorers:\n", df[df["SCORE"] > 90])

print("\nLow Attendance:\n", df[df["ATTENDANCE"] < 75])

print("\nTuition Students:\n", df[df["TUTION"] == "yes"])

# Multiple Conditions
print("\nHigh Score + High Attendance:\n",
      df[(df["SCORE"] > 90) & (df["ATTENDANCE"] > 90)])

print("\nGood Health & Low Stress:\n",
      df[(df["HEALTH"] == "GOOD") & (df["STRESS"] == "LOW")])

# OR Condition
print("\nHigh Video Games OR Low Study:\n",
      df[(df["VIDEO GAMES"] > 2) | (df["SELF STUDY"] < 2)])

# NOT Condition
print("\nNo Tuition:\n", df[~(df["TUTION"] == "yes")])

#  Advanced Filters
print("\nQuery Filter:\n",
      df.query("SCORE > 90 and ATTENDANCE > 90"))

print("\nName contains 'a':\n",
      df[df["NAME"].str.contains("a", case=False)])

print("\nHealth in GOOD:\n",
      df[df["HEALTH"].isin(["GOOD"])])


# =========================================================
# 3. DATA FIGURE-OUT (ANALYSIS)
# =========================================================
print("\n========== DATA ANALYSIS ==========")

df = clean_data(df_original)
df = df.rename(columns={"EXAM SCORE": "SCORE"})

# Analysis
print("\nTuition vs Score:\n",
      df.groupby("TUTION")["SCORE"].mean())

print("\nHealth vs Score:\n",
      df.groupby("HEALTH")["SCORE"].mean())

print("\nStress vs Score:\n",
      df.groupby("STRESS")["SCORE"].mean())

print("\nCorrelation Matrix:\n",
      df.corr(numeric_only=True))

print("\nPivot Table:\n",
      pd.pivot_table(df, values="SCORE",
                     index="TUTION", columns="HEALTH", aggfunc="mean"))

print("\nHealth Count:\n", df["HEALTH"].value_counts())
print("\nStress Count:\n", df["STRESS"].value_counts())

print("\nFinal Dataset:\n", df.head())



df = clean_data(df_original)

df["PERFORMANCE"] = df["EXAM SCORE"].apply(
    lambda x: "Excellent" if x > 90 else "Average" if x > 70 else "Poor"
)
df["STATUS"] = np.where(df["EXAM SCORE"] > 75, "Pass", "Fail")

df = df.rename(columns={"EXAM SCORE": "SCORE"})

df.to_csv("final_output.csv", index=False)