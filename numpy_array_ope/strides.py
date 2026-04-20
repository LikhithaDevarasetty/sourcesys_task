import numpy as np

# Strides in NumPy Arrays
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]], dtype=np.int32)

print("Array:\n", arr)
print("Shape:", arr.shape)
print("Strides:", arr.strides)

# 1. Slicing uses strides to create views (no copy)
row = arr[1]
print("\nRow 1:", row)
print("Row strides:", row.strides)
print("Shares memory:", np.shares_memory(arr, row))

# 2. Every other element using strides
every_other = arr[::2, ::2]
print("\nEvery other element:\n", every_other)
print("Strides:", every_other.strides)
print("Shares memory:", np.shares_memory(arr, every_other))

# 3. Transpose changes strides without copying
transposed = arr.T
print("\nTransposed:\n", transposed)
print("Original strides: ", arr.strides)
print("Transposed strides:", transposed.strides)
print("Shares memory:", np.shares_memory(arr, transposed))

# 4. as_strided for custom stride manipulation
from numpy.lib.stride_tricks import as_strided

arr1d = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
# Create 2D sliding window view using custom strides
windowed = as_strided(arr1d, shape=(4, 3), strides=(4, 4))
print("\n1D Array:", arr1d)
print("Sliding window view:\n", windowed)
print("Shares memory:", np.shares_memory(arr1d, windowed))

# 5. Reshape keeps same strides (view, no copy)
arr2 = np.arange(12, dtype=np.int32)
reshaped = arr2.reshape(3, 4)
print("\nOriginal strides:", arr2.strides)
print("Reshaped strides:", reshaped.strides)
print("Shares memory:", np.shares_memory(arr2, reshaped))