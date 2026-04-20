## Task: NumPy 1D Array – Complete Operations

* **Description**
This project demonstrates **all major concepts and operations of NumPy using 1D arrays**. It provides a comprehensive understanding of how NumPy works with array creation, manipulation, mathematical operations, and data analysis.

* **Concepts Covered**

    - Array creation (array, zeros, ones, arange, linspace, random)
    - Array attributes (shape, size, dtype, ndim)
    - Indexing and slicing (basic, fancy, boolean)
    - Array modification and assignment
    - Arithmetic operations and broadcasting
    - Mathematical functions (sqrt, log, trigonometry, etc.)
    - Statistical operations (mean, median, std, sum, etc.)
    - Sorting and searching
    - Reshaping and array manipulation
    - Concatenation and splitting
    - Set operations
    - Logical and comparison operations
    - Bitwise operations
    - Linear algebra operations (dot, norm, etc.)
    - Type casting
    - Copy vs View
    - Handling NaN and infinite values
    - String operations using NumPy
    - Saving and loading arrays
    - Utility functions


## NUMPY — Advanced Topics Deep Dive

This project covers advanced NumPy concepts for efficient computation, memory optimization, and high-performance array operations.

---

## Topics Covered

### 1. Indexing (9 Types)
- **Scalar:** `a[0], a[-1]` → View  
- **Slicing:** `a[2:7:2], a[::-1]` → View  
- **Fancy Indexing:** `a[[0,3,6]]` → Copy  
- **Boolean Mask:** `a[a>5]` → Copy  
- **2D Indexing:** `mat[1,3], mat[:,2]` → View  
- **Cross Indexing:** `mat[np.ix_([0,2],[1,3])]` → Copy  
- **Ellipsis:** `arr3d[0,...]` → View  
- **New Axis:** `a[:, np.newaxis]` → View  
- **Selection Ops:** `take / choose / compress` → Copy  

---

### 2. Stacking (Key Functions)
- `np.stack()` → adds new axis  
- `vstack`, `hstack`, `dstack` → vertical/horizontal/depth  
- `column_stack()` → 1D → columns  
- `concatenate()` → flexible axis join  
- `block()` → block matrix assembly  

---

### 3. Memory Optimization
- `float32` → 50% less memory than `float64`  
- `float16` → 75% savings (ML use)  
- `uint8` (images), `int8` (labels)  
- Use `np.can_cast()` before downcasting  

---

### 4. Avoiding Copies
- Slices → **View (✓)** | Fancy indexing → **Copy (✗)**  
- Use in-place ops: `+=`, `*=`  
- `np.add(a, b, out=...)` → no temp arrays  
- `broadcast_to()` → zero-copy expansion  

---

### 5. Strides
- Defines memory step size (bytes)  
- Slicing changes strides, not data  
- `as_strided()` → advanced zero-copy views  
- Transpose swaps strides (no copy)  

---

### 6. Contiguous Arrays
- **C-contiguous** (row-major, default)  
- **F-contiguous** via `asfortranarray()`  
- Transpose/slices break contiguity  
- Fix using `ascontiguousarray()`  

---

### 7. Iteration Techniques
- `nditer` → efficient iteration  
- `ndenumerate` → (index, value)  
- `apply_along_axis()` → row/col ops  
- `vectorize()` → convenience wrapper  
- `flat` → flat iterator  
- Vectorization → ~60x faster than loops  

---