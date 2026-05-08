import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# Load dataset
df = pd.read_csv("data.csv")

print("First 5 Rows:\n")
print(df.head())

# Remove unwanted columns
df = df.drop(["date", "street", "country"], axis=1)

# Encode categorical columns
encoder = LabelEncoder()

df["city"] = encoder.fit_transform(df["city"])
df["statezip"] = encoder.fit_transform(df["statezip"])

# Input and output
X = df.drop("price", axis=1)
y = df["price"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LinearRegression()

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = np.sqrt(mse)

r2 = r2_score(y_test, y_pred)

print("\nModel Performance\n")

print("Mean Absolute Error :", mae)

print("Mean Squared Error  :", mse)

print("Root Mean Squared Error :", rmse)

print("R2 Score :", r2)

# Actual vs Predicted table
result = pd.DataFrame({
    "Actual Price": y_test.values,
    "Predicted Price": y_pred
})

print("\nActual vs Predicted Prices:\n")

print(result.head(10))

# Actual vs Predicted Graph
plt.figure(figsize=(6,5))

plt.scatter(y_test, y_pred, alpha=0.4, color="steelblue")

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--"
)

plt.xlabel("Actual Price")

plt.ylabel("Predicted Price")

plt.title("Actual vs Predicted")

plt.savefig("actual_vs_predicted.png")

plt.show()

# Residual Plot
plt.figure(figsize=(6,5))

plt.scatter(
    y_pred,
    y_test - y_pred,
    alpha=0.4,
    color="steelblue"
)

plt.axhline(0, color="red", linestyle="--")

plt.xlabel("Predicted Price")

plt.ylabel("Residuals")

plt.title("Residual Plot")

plt.savefig("residuals.png")

plt.show()

# Feature Coefficients Graph
plt.figure(figsize=(8,6))

coef = pd.Series(
    model.coef_,
    index=X.columns
).sort_values()

coef.plot(
    kind="barh",
    color=[
        "red" if c > 0 else "steelblue"
        for c in coef
    ]
)

plt.axvline(0, color="black", linewidth=0.8)

plt.title("Feature Coefficients")

plt.savefig("feature_coefficients.png")

plt.show()

# Sample Prediction
sample = X.iloc[0:1]

prediction = model.predict(sample)

print("\nPredicted House Price:\n")

print(prediction[0])