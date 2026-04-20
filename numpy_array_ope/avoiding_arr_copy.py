import numpy as np
import sys
sys.stdout.flush()
# 1. Views via Slicing
arr = np.array([1, 2, 3, 4, 5])
sliced_view = arr[1:4]
sliced_copy = arr[1:4].copy()
print("Sliced View shares memory:", np.shares_memory(arr, sliced_view))
print("Sliced Copy shares memory:", np.shares_memory(arr, sliced_copy))

# 2. In-Place Operations
arr2 = np.array([1.0, 2.0, 3.0, 4.0])
arr2 *= 2
arr2 += 10
np.multiply(arr2, 2, out=arr2)
print("\nIn-place result:", arr2)

# 3. Reshape Without Copying
arr3 = np.arange(12)
reshaped  = arr3.reshape(3, 4)
flat_view = reshaped.ravel()
flat_copy = reshaped.flatten()
print("\nReshape shares memory:", np.shares_memory(arr3, reshaped))
print("Ravel   shares memory:", np.shares_memory(arr3, flat_view))
print("Flatten shares memory:", np.shares_memory(arr3, flat_copy))

# 4. Pre-allocate Instead of Growing
arr_good = np.empty(10, dtype=int)
for i in range(10):
    arr_good[i] = i * 2
arr_best = np.arange(10) * 2
print("\nPre-allocated:", arr_good)
print("Vectorized:   ", arr_best)

# 5. Transpose
arr4 = np.arange(6).reshape(2, 3)
transposed = arr4.T
print("\nTranspose shares memory:", np.shares_memory(arr4, transposed))

# 6. Boolean and Fancy Indexing
arr5 = np.array([10, 20, 30, 40, 50])
fancy_index = arr5[[0, 2, 4]]
bool_index  = arr5[arr5 > 25]
print("\nFancy Index shares memory:", np.shares_memory(arr5, fancy_index))
print("Bool  Index shares memory:", np.shares_memory(arr5, bool_index))