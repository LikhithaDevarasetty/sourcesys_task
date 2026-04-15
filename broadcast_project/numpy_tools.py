import numpy as np

def numpy_tools():
    arr = np.random.randint(1,100,(4,4))

    print("Array:\n", arr)

    print("\nShape:", arr.shape)
    print("Dimensions:", arr.ndim)
    print("Size:", arr.size)
    print("Data Type:", arr.dtype)

    print("\nMean:", arr.mean())
    print("Median:", np.median(arr))
    print("Standard Deviation:", arr.std())

    print("\nTranspose:\n", arr.T)

    print("\nFlatten:\n", arr.flatten())
    
numpy_tools()