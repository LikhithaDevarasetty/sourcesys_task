import pandas as pd

# Load cleaned dataset
df = pd.read_csv("STUDENT.csv")

print("\n========== GROUPING & ANALYSIS ==========")

# 1. Group by Tuition
print("\nAverage Score by Tuition:\n",
      df.groupby("TUTION")["EXAM SCORE"].mean())

# 2. Group by Health
print("\nAverage Score by Health:\n",
      df.groupby("HEALTH")["EXAM SCORE"].mean())

# 3. Group by Stress
print("\nAverage Score by Stress:\n",
      df.groupby("STRESS")["EXAM SCORE"].mean())

# 4. Multiple Grouping
print("\nTuition & Health Analysis:\n",
      df.groupby(["TUTION", "HEALTH"])["EXAM SCORE"].mean())

# 5. Aggregation (multiple stats)
print("\nDetailed Stats (Tuition):\n",
      df.groupby("TUTION")["EXAM SCORE"].agg(["mean", "max", "min", "count"]))

# 6. Pivot Table
print("\nPivot Table:\n",
      pd.pivot_table(df,
                     values="EXAM SCORE",
                     index="TUTION",
                     columns="HEALTH",
                     aggfunc="mean"))

# 7. Count Analysis
print("\nHealth Count:\n", df["HEALTH"].value_counts())
print("\nStress Count:\n", df["STRESS"].value_counts())

# 8. Correlation
print("\nCorrelation Matrix:\n",
      df.corr(numeric_only=True))