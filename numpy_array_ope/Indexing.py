import numpy as np
import sys 
# ── 1A. Basic Scalar Indexing ──────────────────────────────────

a = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"  Array         : {a}")
print(f"  a[0]          : {a[0]}    (first)")
print(f"  a[-1]         : {a[-1]}   (last)")
print(f"  a[-3]         : {a[-3]}   (3rd from end)")
 
# ── 1B. Slicing ────────────────────────────────────────────────

print(f"  a[2:7]        : {a[2:7]}")
print(f"  a[:4]         : {a[:4]}")
print(f"  a[6:]         : {a[6:]}")
print(f"  a[::3]        : {a[::3]}        (every 3rd)")
print(f"  a[::-1]       : {a[::-1]}  (reversed)")
print(f"  a[1:8:2]      : {a[1:8:2]}      (start=1, stop=8, step=2)")
 
# ── 1C. Fancy / Integer Array Indexing ────────────────────────

idx = np.array([0, 3, 6, 9])
print(f"  Indices       : {idx}")
print(f"  a[idx]        : {a[idx]}")
# Non-contiguous, out-of-order
idx2 = np.array([9, 2, 5, 0])
print(f"  a[[9,2,5,0]]  : {a[idx2]}  (out-of-order → always a COPY)")
# Repeated indices
idx3 = np.array([1, 1, 3, 3])
print(f"  a[[1,1,3,3]]  : {a[idx3]}  (repeated indices allowed)")
 
# ── 1D. Boolean / Mask Indexing ───────────────────────────────

a2 = np.array([5, 12, 3, 18, 7, 25, 1, 9])
print(f"  Array         : {a2}")
mask = a2 > 8
print(f"  mask (>8)     : {mask}")
print(f"  a2[mask]      : {a2[mask]}")
# Compound conditions
print(f"  a2[(a2>5)&(a2<20)]  : {a2[(a2 > 5) & (a2 < 20)]}")
print(f"  a2[(a2<4)|(a2>20)]  : {a2[(a2 < 4) | (a2 > 20)]}")
# np.where returns indices
indices = np.where(a2 > 8)
print(f"  np.where(a2>8): indices={indices[0]}  values={a2[indices]}")
 
# ── 1E. 2D Array Indexing ─────────────────────────────────────

mat = np.arange(1, 26).reshape(5, 5)
print(f"  Matrix (5x5):\n{mat}")
print(f"\n  mat[1, 3]          : {mat[1, 3]}        (row=1, col=3)")
print(f"  mat[0]             : {mat[0]}  (entire row 0)")
print(f"  mat[:, 2]          : {mat[:, 2]}  (entire col 2)")
print(f"  mat[1:3, 1:4]:\n{mat[1:3, 1:4]}  (sub-matrix)")
print(f"  mat[::2, ::2]:\n{mat[::2, ::2]}  (every other row & col)")
 
# ── 1F. Fancy Indexing on 2D ──────────────────────────────────

rows = np.array([0, 2, 4])
cols = np.array([1, 3, 0])
print(f"  mat[rows, cols]   : {mat[rows, cols]}  (pairs: (0,1),(2,3),(4,0))")
# Select specific rows
print(f"  mat[[0,2,4]]:\n{mat[[0, 2, 4]]}  (rows 0,2,4)")
# Select specific columns from specific rows
print(f"  mat[np.ix_([0,2],[1,3])]:\n{mat[np.ix_([0, 2], [1, 3])]}  (np.ix_ cross-product)")
 
# ── 1G. Ellipsis & newaxis ────────────────────────────────────

arr3d = np.arange(24).reshape(2, 3, 4)
print(f"  3D shape: {arr3d.shape}")
print(f"  arr3d[0, ...]     shape: {arr3d[0, ...].shape}   (first slice, keep rest)")
print(f"  arr3d[..., 1]     shape: {arr3d[..., 1].shape}   (last dim = 1)")
a1d = np.array([1, 2, 3])
print(f"  a1d shape         : {a1d.shape}")
print(f"  a1d[np.newaxis,:] : {a1d[np.newaxis, :]}  shape={a1d[np.newaxis, :].shape} (row vector)")
print(f"  a1d[:, np.newaxis]:\n{a1d[:, np.newaxis]}  shape={a1d[:, np.newaxis].shape} (col vector)")
 
# ── 1H. np.take / np.choose / np.compress ────────────────────

a = np.array([10, 20, 30, 40, 50])
print(f"  np.take(a,[0,2,4])   : {np.take(a, [0, 2, 4])}")
choices = np.array([[0,1,2,3],[10,11,12,13],[20,21,22,23]])
sel = np.array([0, 2, 1, 0])
print(f"  np.choose(sel,chcs)  : {np.choose(sel, choices)}")
cond = np.array([True, False, True, False, True])
print(f"  np.compress(cond,a)  : {np.compress(cond, a)}")
 
# ── 1I. Index tricks: np.diag, triu, tril ────────────────────

mat = np.arange(1, 10).reshape(3, 3)
print(f"  Matrix:\n{mat}")
print(f"  np.diag(mat)         : {np.diag(mat)}")
print(f"  np.diag(mat, k=1)    : {np.diag(mat, k=1)}  (super-diagonal)")
print(f"  np.triu(mat):\n{np.triu(mat)}")
print(f"  np.tril(mat):\n{np.tril(mat)}")
di = np.diag_indices(3)
mat2 = mat.copy()
mat2[di] = 0
print(f"  diag zeroed:\n{mat2}")
 