import random
import math
import numpy as np


# ──────────────────────────────────────────────────────────────
#  SECTION 1 — Dataset Generation
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 1 — Dataset Generation (random module + numpy)")
print("=" * 65)

random.seed(7)

STUDENTS = ["Aarav", "Bhavya", "Charan", "Divya", "Esha",
            "Farhan", "Geetha", "Harish", "Isha", "Jayanth"]
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "CS"]

raw = [[round(random.uniform(40, 98), 1) for _ in SUBJECTS] for _ in STUDENTS]

# Convert to NumPy array — all subsequent computations use numpy
M = np.array(raw, dtype=float)   # shape: (10, 5)

print(f"\n  {'Student':<12}", end="")
for s in SUBJECTS:
    print(f"  {s:>10}", end="")
print()
print("  " + "-" * 62)
for i, name in enumerate(STUDENTS):
    print(f"  {name:<12}", end="")
    for mark in M[i]:
        print(f"  {mark:>10.1f}", end="")
    print()


# ──────────────────────────────────────────────────────────────
#  SECTION 2 — Matrix Representation
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 2 — Matrix Representation")
print("=" * 65)

print(f"\n  ── Marks Matrix M  [10 students × 5 subjects]")
print(M)

print(f"\n  ── Shape of M")
print(f"    Rows (students) : {M.shape[0]}")
print(f"    Cols (subjects) : {M.shape[1]}")

print(f"\n  ── Transpose  M.T  [5 subjects × 10 students]")
print(M.T)

print(f"\n  ── Data type and memory")
print(f"    dtype  : {M.dtype}")
print(f"    size   : {M.nbytes} bytes")


# ──────────────────────────────────────────────────────────────
#  SECTION 3 — Vector Operations
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 3 — Vector Operations")
print("=" * 65)

v_aarav  = M[0]
v_bhavya = M[1]

print(f"\n  ── Each student = a vector in 5D subject-space")
print(f"    Aarav  : {v_aarav}")
print(f"    Bhavya : {v_bhavya}")

print(f"\n  ── Vector Addition  (combined score profile)")
combined = v_aarav + v_bhavya
print(f"    Aarav + Bhavya : {combined}")

print(f"\n  ── Vector Subtraction  (score difference)")
diff = v_aarav - v_bhavya
print(f"    Aarav - Bhavya : {diff}")

print(f"\n  ── Scalar Multiplication  (scale marks by 0.5)")
scaled = v_aarav * 0.5
print(f"    Aarav × 0.5 : {scaled}")

print(f"\n  ── Dot Product  (similarity of score patterns)")
dp = np.dot(v_aarav, v_bhavya)
print(f"    Aarav · Bhavya  =  {dp:.2f}")

print(f"\n  ── Vector Norms  (overall performance magnitude)")
for i, name in enumerate(STUDENTS):
    print(f"    ||{name:<8}|| = {np.linalg.norm(M[i]):>7.2f}")

print(f"\n  ── Unit Vector  (normalised score direction for Aarav)")
norm_a  = np.linalg.norm(v_aarav)
unit_a  = v_aarav / norm_a
print(f"    Unit(Aarav) : {unit_a}")
print(f"    Verification ||unit|| = {np.linalg.norm(unit_a):.6f}  (should be 1.0)")

print(f"\n  ── Vector Projection  (project Aarav onto Bhavya)")
proj = (np.dot(v_aarav, v_bhavya) / np.dot(v_bhavya, v_bhavya)) * v_bhavya
print(f"    proj(Aarav → Bhavya) : {proj}")


# ──────────────────────────────────────────────────────────────
#  SECTION 4 — Matrix Operations
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 4 — Matrix Operations")
print("=" * 65)

A3 = M[:3, :3].copy()   # 3×3 sub-matrix: first 3 students, first 3 subjects
print(f"\n  ── 3×3 sub-matrix  (Aarav, Bhavya, Charan  ×  Maths, Physics, Chem)")
print(A3)

print(f"\n  ── Matrix Addition  (A3 + A3)")
print(A3 + A3)

print(f"\n  ── Scalar Multiplication  (A3 × 0.1 → scale to 0-10)")
print(A3 * 0.1)

print(f"\n  ── Matrix Multiplication  A3 @ A3.T  → student similarity")
sim = A3 @ A3.T
print(sim)

print(f"\n  ── Element-wise multiplication  (Hadamard product)")
print(A3 * A3)

print(f"\n  ── Transpose verification  (A.T).T == A")
ok = np.allclose(A3.T.T, A3)
print(f"    (A3.T).T == A3  →  {ok}")


# ──────────────────────────────────────────────────────────────
#  SECTION 5 — Determinant · Trace · Rank · Inverse
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 5 — Determinant · Trace · Rank · Inverse")
print("=" * 65)

print(f"\n  ── Trace  (sum of diagonal)")
print(f"    tr(A3)         = {np.trace(A3):.2f}")
print(f"    tr(sim)        = {np.trace(sim):.2f}")

print(f"\n  ── Determinant  (scaling factor of the transformation)")
det_val = np.linalg.det(A3)
print(f"    det(A3) = {det_val:.2f}")
if abs(det_val) > 1e-6:
    print("    → Non-zero  ⟹  matrix is invertible")
else:
    print("    → Zero  ⟹  singular matrix (not invertible)")

print(f"\n  ── Rank  (number of linearly independent rows/columns)")
print(f"    rank(M  10×5) = {np.linalg.matrix_rank(M)}")
print(f"    rank(A3  3×3) = {np.linalg.matrix_rank(A3)}")

print(f"\n  ── Inverse  A3_inv")
A3_inv = np.linalg.inv(A3)
print(A3_inv)

print(f"\n  ── Verification  A3 @ A3_inv  should be Identity")
I_check = A3 @ A3_inv
print(I_check)
print(f"    Max error from Identity = {np.max(np.abs(I_check - np.eye(3))):.2e}  ✓")

print(f"\n  ── Frobenius Norm of A3")
print(f"    ||A3||_F  =  {np.linalg.norm(A3, 'fro'):.4f}")


# ──────────────────────────────────────────────────────────────
#  SECTION 6 — Solving a Linear System  Ax = b
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 6 — Solving a Linear System  Ax = b")
print("=" * 65)

print("""
    Problem:
    A teacher records weighted marks from 3 exams (x1, x2, x3)
    for 3 students.  Given the final totals, find the weights.

    A × x = b
        A = weight-coefficient matrix  (random)
        x = unknown exam weights
        b = known final totals
""")

random.seed(42)
A_sys  = np.array([[round(random.uniform(0.5, 2.0), 2) for _ in range(3)] for _ in range(3)])
x_true = np.array([0.3, 0.4, 0.3])
b_sys  = A_sys @ x_true

print("Coefficient matrix A :")
print(A_sys)
print(f"Right-hand side b    : {b_sys}")

x_sol = np.linalg.solve(A_sys, b_sys)
print(f"Solution x (recovered weights) : {x_sol}")
print(f"True weights (expected)        : {x_true}")
print(f"\n    Max solution error = {np.max(np.abs(x_sol - x_true)):.2e}  ✓")

print(f"\n  ── Least-squares solution  (np.linalg.lstsq) on full marks matrix")
# find a 5D weight vector such that M @ w ≈ some target scores
target   = np.array([75, 80, 70, 85, 78, 65, 90, 72, 68, 82], dtype=float)
w_lstsq, residuals, rank_ls, sv = np.linalg.lstsq(M, target, rcond=None)
print(f"    Least-squares weights : {w_lstsq}")


# ──────────────────────────────────────────────────────────────
#  SECTION 7 — Eigenvalues & Eigenvectors
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 7 — Eigenvalues & Eigenvectors")
print("=" * 65)

print("""
    Applied on the student similarity matrix  S = A3 @ A3.T
    Eigenvalues reveal the dominant 'variance directions'.
""")

eigenvalues, eigenvectors = np.linalg.eig(sim)

# Sort by descending eigenvalue magnitude
order = np.argsort(np.abs(eigenvalues))[::-1]
eigenvalues  = eigenvalues[order]
eigenvectors = eigenvectors[:, order]

for idx in range(len(eigenvalues)):
    print(f"    λ{idx+1} = {eigenvalues[idx]:>10.4f}   "
          f"v{idx+1} = {np.array2string(eigenvectors[:, idx], precision=4, suppress_small=True)}")

print(f"\n  ── Verification  S @ v1 ≈ λ1 × v1")
lam1 = eigenvalues[0]
v1   = eigenvectors[:, 0]
Sv1  = sim @ v1
lv1  = lam1 * v1
print(f"    S @ v1  : {Sv1.real}")
print(f"    λ1 × v1 : {lv1.real}")
print(f"    Max error = {np.max(np.abs(Sv1 - lv1)):.2e}  ✓")

print(f"\n  ── Characteristic equation  det(S - λI) ≈ 0  for each eigenvalue")
for idx, lam in enumerate(eigenvalues):
    val = np.linalg.det(sim - lam * np.eye(3))
    print(f"    det(S - λ{idx+1}·I)  =  {val:.4e}")


# ──────────────────────────────────────────────────────────────
#  SECTION 8 — Cosine Similarity
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 8 — Cosine Similarity (Student Profile Comparison)")
print("=" * 65)

print("""
    Cosine similarity measures angular closeness between
    two score vectors regardless of their magnitudes.
    Range: -1 (opposite) to +1 (identical direction).
""")

print(f"  {'Pair':<22}  {'Dot Product':>12}  {'Cos Sim':>10}  {'Angle (°)':>10}")
print("  " + "-" * 60)

pairs = [(0,1), (0,2), (0,3), (1,4), (2,5)]
for i, j in pairs:
    u, v    = M[i], M[j]
    cs      = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    angle   = math.degrees(math.acos(np.clip(cs, -1, 1)))
    dp_ij   = np.dot(u, v)
    print(f"  {STUDENTS[i]+' & '+STUDENTS[j]:<22}  {dp_ij:>12.1f}  {cs:>10.4f}  {angle:>10.2f}°")


# ──────────────────────────────────────────────────────────────
#  SECTION 9 — Singular Value Decomposition (SVD)
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 9 — Singular Value Decomposition (SVD)")
print("=" * 65)

print("""
    Full SVD on the marks matrix M (10×5):
        M = U Σ V^T
    Singular values represent the 'energy' of each dimension.
    Useful for dimensionality reduction (low-rank approximation).
""")

U, S_vals, Vt = np.linalg.svd(M, full_matrices=False)

print(f"    U  shape : {U.shape}")
print(f"    Σ  shape : {S_vals.shape}  (diagonal)")
print(f"    Vᵀ shape : {Vt.shape}")
print()

total_energy = np.sum(S_vals ** 2)
cumulative   = 0.0
for idx, sv in enumerate(S_vals):
    energy     = sv ** 2
    cumulative += energy
    print(f"    σ{idx+1} = {sv:>9.4f}   "
          f"energy = {energy/total_energy*100:>5.1f}%   "
          f"cumulative = {cumulative/total_energy*100:>5.1f}%")

print(f"\n  ── Low-rank approximation using top-2 singular values")
M_approx = U[:, :2] @ np.diag(S_vals[:2]) @ Vt[:2, :]
error    = np.linalg.norm(M - M_approx, 'fro')
print(f"    Frobenius error (rank-2 approx)  =  {error:.4f}")
print(f"    Energy retained                  =  "
      f"{np.sum(S_vals[:2]**2)/total_energy*100:.1f}%")


# ──────────────────────────────────────────────────────────────
#  SECTION 10 — Mean-Centring & Covariance Matrix
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 10 — Mean-Centring & Covariance Matrix")
print("=" * 65)

print(f"\n  ── Column means  (average score per subject)")
col_means = np.mean(M, axis=0)
for s, m in zip(SUBJECTS, col_means):
    print(f"    {s:<12}  mean = {m:.2f}")

print(f"\n  ── Column std-deviations  (spread per subject)")
col_stds = np.std(M, axis=0)
for s, sd in zip(SUBJECTS, col_stds):
    print(f"    {s:<12}  std  = {sd:.2f}")

print(f"\n  ── Mean-centred matrix  MC = M − col_means")
MC = M - col_means
print(MC)

print(f"\n  ── Covariance matrix  C = (1/n) × MC.T @ MC   [5×5]")
n = M.shape[0]
C_cov = (MC.T @ MC) / n
print(C_cov)

print(f"\n  ── Diagonal of C = variance per subject")
for s, v in zip(SUBJECTS, np.diag(C_cov)):
    print(f"    Var({s:<12}) = {v:.2f}   std = {math.sqrt(v):.2f}")

print(f"\n  ── Trace(C) = Total variance")
print(f"    tr(C) = {np.trace(C_cov):.2f}")

print(f"\n  ── Verify with numpy's built-in cov (rowvar=False)")
C_np = np.cov(M, rowvar=False, bias=True)
print(f"    Max difference from manual formula = {np.max(np.abs(C_cov - C_np)):.2e} ")


# ──────────────────────────────────────────────────────────────
#  SECTION 11 — PCA (manual, using eigenvectors of covariance)
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 11 — PCA (Principal Component Analysis)")
print("=" * 65)

print("""
    PCA finds directions of maximum variance.
    Steps:
      1. Mean-centre the data
      2. Compute covariance matrix C
      3. Find eigenvectors of C  → principal components
      4. Project data onto top-k components
""")

eig_vals_pca, eig_vecs_pca = np.linalg.eigh(C_cov)   # eigh for symmetric matrix
# Sort descending
order_pca    = np.argsort(eig_vals_pca)[::-1]
eig_vals_pca = eig_vals_pca[order_pca]
eig_vecs_pca = eig_vecs_pca[:, order_pca]

print(f"\n  ── Explained variance per principal component")
total_var = np.sum(eig_vals_pca)
for idx, ev in enumerate(eig_vals_pca):
    print(f"    PC{idx+1}  eigenvalue = {ev:>8.4f}   "
          f"explained = {ev/total_var*100:>5.1f}%")

print(f"\n  ── Project data onto first 2 principal components")
PC2   = eig_vecs_pca[:, :2]
M_pca = MC @ PC2
print(f"    Projected shape : {M_pca.shape}  (10 students × 2 PCs)")
print()
print(f"  {'Student':<12}  {'PC1':>10}  {'PC2':>10}")
print("  " + "-" * 36)
for name, coords in zip(STUDENTS, M_pca):
    print(f"  {name:<12}  {coords[0]:>10.4f}  {coords[1]:>10.4f}")


# ──────────────────────────────────────────────────────────────
#  SECTION 12 — Weighted Score & Grade Assignment
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 12 — Weighted Score & Grade Assignment")
print("=" * 65)


weights = np.array([0.25, 0.20, 0.20, 0.15, 0.20])

w_scores = M @ weights

def grade(score):
    if   score >= 85: return "O  (Outstanding)"
    elif score >= 75: return "A+ (Excellent)"
    elif score >= 65: return "A  (Very Good)"
    elif score >= 55: return "B  (Good)"
    else:             return "C  (Needs Improvement)"

print(f"\n  {'Student':<12}  {'Weighted Score':>14}  {'Grade'}")
print("  " + "-" * 55)
for name, ws in zip(STUDENTS, w_scores):
    print(f"  {name:<12}  {ws:>14.2f}  {grade(ws)}")

print(f"\n  ── Class statistics using numpy")
print(f"    Mean  score : {np.mean(w_scores):.2f}")
print(f"    Std   score : {np.std(w_scores):.2f}")
print(f"    Max   score : {np.max(w_scores):.2f}  → {STUDENTS[np.argmax(w_scores)]}")
print(f"    Min   score : {np.min(w_scores):.2f}  → {STUDENTS[np.argmin(w_scores)]}")

print(f"\n  ── Ranking students by weighted score (numpy argsort)")
ranked = np.argsort(w_scores)[::-1]
print()
for rank_pos, idx in enumerate(ranked, 1):
    print(f"    #{rank_pos:<3} {STUDENTS[idx]:<10}  {w_scores[idx]:.2f}")


# ──────────────────────────────────────────────────────────────
#  SECTION 13 — Subject Correlation Matrix
# ──────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  STEP 13 — Subject Correlation Matrix")
print("=" * 65)

print("""
    Correlation = normalised covariance.
    Reveals which subjects tend to score together.
""")

corr = np.corrcoef(M, rowvar=False)
print(corr)

print()
print(f"  {'Subject Pair':<25}  {'Correlation':>12}")
print("  " + "-" * 40)
for i in range(5):
    for j in range(i+1, 5):
        print(f"  {SUBJECTS[i]+' & '+SUBJECTS[j]:<25}  {corr[i,j]:>12.4f}")