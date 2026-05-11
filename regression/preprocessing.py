import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def load_and_split(csv_path: str = "heart.csv", test_size: float = 0.2, random_state: int = 42):
    
    df = pd.read_csv(csv_path)

    print("Shape         :", df.shape)
    print("Missing values:\n", df.isnull().sum())
    print("\nTarget distribution:\n", df["target"].value_counts())
    print("\nDescriptive stats:\n", df.describe())

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"\nTrain size : {X_train.shape}")
    print(f"Test  size : {X_test.shape}")

    return X_train, X_test, y_train, y_test


def get_standard_scaled(X_train, X_test):
    """Return StandardScaler-transformed arrays (fit on train, apply to test)."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def get_minmax_scaled(X_train, X_test):
    """Return MinMaxScaler-transformed arrays (fit on train, apply to test)."""
    mm = MinMaxScaler()
    X_train_mm = mm.fit_transform(X_train)
    X_test_mm  = mm.transform(X_test)
    return X_train_mm, X_test_mm, mm

if __name__ == "__main__":
    import pandas as pd
 
    df = pd.read_csv("heart.csv")
 
    print("DATASET OVERVIEW")
    print(f"\nShape       : {df.shape}")
    print(f"Columns     : {list(df.columns)}")
 
    print("\n── First 5 rows ──────────────────────────────")
    print(df.head())
 
    print("\n── Data Types & Non-Null Counts ──────────────")
    print(df.info())
 
    print("\n── Missing Values ────────────────────────────")
    print(df.isnull().sum())
 
    print("\n── Descriptive Statistics ────────────────────")
    print(df.describe())
 
    print("\n── Target Distribution ───────────────────────")
    print(df["target"].value_counts())
    print(f"  (0 = No Disease, 1 = Disease)")
 
    print("TRAIN / TEST SPLIT (80/20, stratified)")
    X_train, X_test, y_train, y_test = load_and_split("heart.csv")
 
    print("\n── StandardScaler (for KNN) ──────────────────")
    X_train_scaled, X_test_scaled, scaler = get_standard_scaled(X_train, X_test)
    import numpy as np
    print(f"  X_train_scaled mean ≈ {X_train_scaled.mean():.4f}  std ≈ {X_train_scaled.std():.4f}")
    print(f"  X_test_scaled  mean ≈ {X_test_scaled.mean():.4f}  std ≈ {X_test_scaled.std():.4f}")
 
    print("\n── MinMaxScaler (for Multinomial NB) ─────────")
    X_train_mm, X_test_mm, mm = get_minmax_scaled(X_train, X_test)
    print(f"  X_train_mm min={X_train_mm.min():.4f}  max={X_train_mm.max():.4f}")
    print(f"  X_test_mm  min={X_test_mm.min():.4f}  max={X_test_mm.max():.4f}")
 