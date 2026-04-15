import numpy as np

# 1️⃣ Scalar Broadcasting
print("1. Scalar Broadcasting")
a = np.array([1, 2, 3])
print("Array:", a)
print("Array + 10:", a + 10)
print()

# 2️⃣ Same Shape Broadcasting
print("2. Same Shape Arrays")
b = np.array([4, 5, 6])
print("Array1:", a)
print("Array2:", b)
print("Result:", a + b)
print()

# 3️⃣ Row Broadcasting (1D to 2D)
print("3. Row Broadcasting")
c = np.array([[1, 2, 3],
              [4, 5, 6]])
d = np.array([10, 20, 30])
print("Matrix:\n", c)
print("Row vector:", d)
print("Result:\n", c + d)
print()

# 4️⃣ Column Broadcasting
print("4. Column Broadcasting")
e = np.array([[1], [2], [3]])
f = np.array([10, 20, 30])
print("Column vector:\n", e)
print("Row vector:", f)
print("Result:\n", e + f)
print()

# 5️⃣ Higher Dimension Broadcasting
print("5. Higher Dimension Broadcasting")
g = np.array([[[1, 2, 3]]])
h = np.array([10, 20, 30])
print("3D Array:\n", g)
print("1D Array:", h)
print("Result:\n", g + h)
print()

# 6️⃣ Broadcasting with Different Shapes
print("6. Different Shape Broadcasting")
i = np.array([[1], [2]])
j = np.array([10, 20, 30])
print("Shape (2,1):\n", i)
print("Shape (3,):", j)
print("Result:\n", i + j)
print()

# 7️⃣ Invalid Broadcasting Example
print("7. Invalid Broadcasting (Error Case)")
try:
    x = np.array([1, 2])
    y = np.array([1, 2, 3])
    print(x + y)
except ValueError as e:
    print("Error:", e)
