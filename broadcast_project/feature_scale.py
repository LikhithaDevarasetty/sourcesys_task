import numpy as np

# Sample data
data = np.array([10, 20, 30, 40, 50])
print("Original Data:", data)

# 1. Min-Max Scaling (0 to 1)
min_val = np.min(data)
max_val = np.max(data)

min_max_scaled = (data - min_val) / (max_val - min_val)
print("\nMin-Max Scaling:", min_max_scaled)

# 2. Standardization (Z-score)
mean = np.mean(data)
std = np.std(data)

standard_scaled = (data - mean) / std
print("\nStandardization (Z-score):", standard_scaled)

# 3. Max Scaling
max_scaled = data / max_val
print("\nMax Scaling:", max_scaled)

# 4. Mean Normalization
mean_norm = (data - mean) / (max_val - min_val)
print("\nMean Normalization:", mean_norm)

# 5. Unit Vector Scaling (L2 Normalization)
l2_norm = np.sqrt(np.sum(data**2))
unit_scaled = data / l2_norm
print("\nUnit Vector Scaling:", unit_scaled)