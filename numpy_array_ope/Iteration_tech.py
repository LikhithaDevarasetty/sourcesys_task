import numpy as np

# 1. Basic Iteration (Iterates Row by Row)
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

print("1. Basic Iteration (Row by Row):")
for row in arr:
    print(row)

# 2. Iterating Over Each Element using nditer
print("\n2. nditer (Element by Element):")
for val in np.nditer(arr):
    print(val, end=" ")

# 3. nditer with Order
print("\n\n3. nditer C-Order (Row by Row):")
for val in np.nditer(arr, order='C'):
    print(val, end=" ")

print("\n\n3. nditer F-Order (Column by Column):")
for val in np.nditer(arr, order='F'):
    print(val, end=" ")

# 4. nditer with Read/Write (op_flags)
print("\n\n4. Modify Array using nditer:")
arr2 = np.array([1, 2, 3, 4, 5])
for val in np.nditer(arr2, op_flags=['readwrite']):
    val[...] = val * 2
print("Modified Array:", arr2)

# 5. ndenumerate (Index + Value)
print("\n5. ndenumerate (Index + Value):")
arr3 = np.array([[10, 20, 30],
                 [40, 50, 60]])
for index, val in np.ndenumerate(arr3):
    print(f"Index: {index}  Value: {val}")

# 6. ndindex (Only Indices)
print("\n6. ndindex (Only Indices):")
for index in np.ndindex(2, 3):
    print(index, end=" ")

# 7. Flat Iterator (1D view of array)
print("\n\n7. Flat Iterator:")
arr4 = np.array([[1, 2, 3],
                 [4, 5, 6]])
for val in arr4.flat:
    print(val, end=" ")

# 8. Vectorized Iteration (Fastest - No Loop)
print("\n\n8. Vectorized (No Loop):")
arr5 = np.array([1, 2, 3, 4, 5])
result = arr5 * 2
print("Result:", result)