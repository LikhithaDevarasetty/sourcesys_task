# Student Marks Analysis — Linear Algebra with NumPy

A hands-on Python script that demonstrates core **linear algebra** and **data analysis** concepts using a simulated student marks dataset. Every concept is applied to a real academic context — 10 students across 5 subjects — making the mathematics easy to follow.

---

## Dataset

| Property   | Details                                              |
|------------|------------------------------------------------------|
| Students   | Aarav, Bhavya, Charan, Divya, Esha, Farhan, Geetha, Harish, Isha, Jayanth |
| Subjects   | Maths, Physics, Chemistry, English, CS               |
| Shape      | 10 × 5 matrix                                        |
| Mark Range | 40.0 – 98.0 (randomly generated, seed = 7)           |

---


## Sections

### Step 1 — Dataset Generation
Generates random marks using Python's `random` module and converts them into a NumPy array (`M` of shape 10 × 5). Uses a fixed seed for reproducibility.

### Step 2 — Matrix Representation
Displays the marks matrix, its transpose, shape, data type, and memory usage.

### Step 3 — Vector Operations
Treats each student's marks as a vector in 5D subject-space and demonstrates:
- Vector addition and subtraction
- Scalar multiplication
- Dot product
- Vector norms (L2)
- Unit vector (normalisation)
- Vector projection

### Step 4 — Matrix Operations
Works on a 3×3 sub-matrix (first 3 students × first 3 subjects) to show:
- Matrix addition
- Scalar multiplication
- Matrix multiplication (`@` operator)
- Hadamard (element-wise) product
- Transpose verification

### Step 5 — Determinant · Trace · Rank · Inverse
Computes key matrix properties:
- **Trace** — sum of diagonal elements
- **Determinant** — checks invertibility
- **Rank** — number of linearly independent rows/columns
- **Inverse** — verified by confirming `A @ A⁻¹ ≈ I`
- **Frobenius norm**

### Step 6 — Solving a Linear System (Ax = b)
Models a teacher finding unknown exam weights given final totals. Solves using `np.linalg.solve` and also demonstrates least-squares fitting with `np.linalg.lstsq` on the full marks matrix.

### Step 7 — Eigenvalues & Eigenvectors
Computes eigenvalues and eigenvectors of the student similarity matrix (`A3 @ A3.T`). Verifies the eigenvalue equation `S·v = λ·v` and the characteristic equation `det(S − λI) = 0`.

### Step 8 — Cosine Similarity
Compares pairs of students by measuring the angle between their score vectors. Outputs dot product, cosine similarity, and angle in degrees for 5 student pairs.

### Step 9 — Singular Value Decomposition (SVD)
Decomposes the full marks matrix as `M = UΣVᵀ`. Reports singular values, their individual and cumulative energy contribution, and demonstrates a rank-2 low-rank approximation with Frobenius error.

### Step 10 — Mean-Centring & Covariance Matrix
- Computes column means and standard deviations per subject
- Builds the mean-centred matrix `MC = M − col_means`
- Computes the 5×5 covariance matrix manually and verifies it against `np.cov`
- Reports per-subject variance and total variance (trace)

### Step 11 — PCA (Principal Component Analysis)
Performs manual PCA using eigenvectors of the covariance matrix:
1. Mean-centre the data
2. Compute covariance matrix
3. Find eigenvectors (principal components)
4. Project data onto the top 2 PCs

Reports explained variance per component and the 2D projected coordinates for each student.

### Step 12 — Weighted Score & Grade Assignment
Assigns subject weights `[0.25, 0.20, 0.20, 0.15, 0.20]` and computes a final weighted score for each student using matrix–vector multiplication. Assigns grades (O / A+ / A / B / C) and ranks all students.

### Step 13 — Subject Correlation Matrix
Computes the 5×5 Pearson correlation matrix using `np.corrcoef`. Lists correlation coefficients for all 10 subject pairs to reveal which subjects tend to score together.

---

## Key NumPy Functions Used

| Function | Purpose |
|---|---|
| `np.linalg.norm` | Vector and matrix norms |
| `np.linalg.det` | Determinant |
| `np.linalg.inv` | Matrix inverse |
| `np.linalg.solve` | Linear system solver |
| `np.linalg.lstsq` | Least-squares solution |
| `np.linalg.eig` | Eigenvalues and eigenvectors |
| `np.linalg.eigh` | Eigenvalues for symmetric matrices |
| `np.linalg.svd` | Singular value decomposition |
| `np.linalg.matrix_rank` | Matrix rank |
| `np.corrcoef` | Pearson correlation matrix |
| `np.cov` | Covariance matrix |
| `np.dot` | Dot product |
| `np.argsort` | Sorting by index |

