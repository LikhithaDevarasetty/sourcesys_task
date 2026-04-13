import numpy as np  
arr = np.array([1, 2, 3, 4]) 
print("Array:", arr) 
print("Sum:", np.sum(arr)) 
print("Mean:", np.mean(arr)) 
# Zeros and Ones 
zeros = np.zeros((2, 2)) 
ones = np.ones((2, 2)) 
print("Zeros:\n", zeros) 
print("Ones:\n", ones) 
# Reshape 
reshaped = arr.reshape(2, 2) 
print("Reshaped:\n", reshaped)