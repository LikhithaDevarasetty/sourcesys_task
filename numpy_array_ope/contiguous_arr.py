import numpy as np

# Contiguous Arrays in NumPy

# 1. C-Contiguous (Row-Major) - default in NumPy
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]], dtype=np.int32)

print("Array:\n", arr)
print("C-Contiguous:", arr.flags['C_CONTIGUOUS'])
print("F-Contiguous:", arr.flags['F_CONTIGUOUS'])
print("Strides:", arr.strides)

# 2. Fortran-Contiguous (Column-Major)
arr_f = np.asfortranarray(arr)
print("\nFortran Array:\n", arr_f)
print("C-Contiguous:", arr_f.flags['C_CONTIGUOUS'])
print("F-Contiguous:", arr_f.flags['F_CONTIGUOUS'])
print("Strides:", arr_f.strides)

# 3. Transpose breaks C-contiguity
transposed = arr.T
print("\nTransposed Array:\n", transposed)
print("C-Contiguous:", transposed.flags['C_CONTIGUOUS'])
print("F-Contiguous:", transposed.flags['F_CONTIGUOUS'])
print("Shares memory:", np.shares_memory(arr, transposed))

# 4. Making non-contiguous array contiguous
# ascontiguousarray makes a C-contiguous copy if needed
arr_contiguous = np.ascontiguousarray(transposed)
print("\nAfter ascontiguousarray:")
print("C-Contiguous:", arr_contiguous.flags['C_CONTIGUOUS'])
print("Shares memory:", np.shares_memory(transposed, arr_contiguous))

# 5. Slicing with steps breaks contiguity
arr2 = np.arange(10, dtype=np.int32)
sliced = arr2[::2]
print("\nOriginal:", arr2)
print("Sliced (step=2):", sliced)
print("C-Contiguous:", sliced.flags['C_CONTIGUOUS'])
print("Shares memory:", np.shares_memory(arr2, sliced))

# Making it contiguous
sliced_contiguous = np.ascontiguousarray(sliced)
print("After ascontiguousarray:")
print("C-Contiguous:", sliced_contiguous.flags['C_CONTIGUOUS'])
print("Shares memory:", np.shares_memory(arr2, sliced_contiguous))

# 6. Checking contiguity before operations
arr3 = np.array([[1, 2, 3],
                 [4, 5, 6]], dtype=np.int32)

print("\nOriginal flags:")
print("C-Contiguous:", arr3.flags['C_CONTIGUOUS'])

arr3_t = arr3.T
print("\nTransposed flags:")
print("C-Contiguous:", arr3_t.flags['C_CONTIGUOUS'])

# Use np.ascontiguousarray to ensure contiguity before heavy computation
arr3_fixed = np.ascontiguousarray(arr3_t)
print("\nFixed flags:")
print("C-Contiguous:", arr3_fixed.flags['C_CONTIGUOUS'])