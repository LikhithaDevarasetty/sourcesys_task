import numpy as np

def sep(title):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print('═'*60)

def sub(title):
    print(f"\n  ── {title} ──")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("1. ARRAY CREATION")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

sub("From Python list")
a = np.array([10, 20, 30, 40, 50])
print(f"  np.array([10,20,30,40,50])  → {a}")

sub("zeros / ones / full")
print(f"  np.zeros(5)                 → {np.zeros(5)}")
print(f"  np.ones(5)                  → {np.ones(5)}")
print(f"  np.full(5, 7)               → {np.full(5, 7)}")

sub("arange / linspace / logspace")
print(f"  np.arange(0, 10, 2)         → {np.arange(0, 10, 2)}")
print(f"  np.linspace(0, 1, 6)        → {np.linspace(0, 1, 6)}")
print(f"  np.logspace(0, 2, 5)        → {np.logspace(0, 2, 5).round(2)}")

sub("Random arrays")
np.random.seed(42)
print(f"  np.random.randint(0,10,6)   → {np.random.randint(0,10,6)}")
print(f"  np.random.rand(5)           → {np.random.rand(5).round(3)}")
print(f"  np.random.randn(5)          → {np.random.randn(5).round(3)}")
print(f"  np.random.uniform(1,10,5)   → {np.random.uniform(1,10,5).round(2)}")
print(f"  np.random.normal(50,10,5)   → {np.random.normal(50,10,5).round(2)}")

sub("empty / eye diagonal / identity")
print(f"  np.empty(4)                 → {np.empty(4).round(3)}")
print(f"  np.eye(3).diagonal()        → {np.eye(3).diagonal()}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("2. ARRAY ATTRIBUTES")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([3, 1, 4, 1, 5, 9, 2, 6], dtype=np.float32)
print(f"  Array         : {a}")
print(f"  .ndim         : {a.ndim}   (dimensions)")
print(f"  .shape        : {a.shape}")
print(f"  .size         : {a.size}   (elements)")
print(f"  .dtype        : {a.dtype}")
print(f"  .itemsize     : {a.itemsize} bytes per element")
print(f"  .nbytes       : {a.nbytes} total bytes")
print(f"  .T            : {a.T}  (transpose = same for 1D)")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("3. INDEXING & SLICING")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
print(f"  Array         : {a}")

sub("Basic indexing")
print(f"  a[0]          : {a[0]}")
print(f"  a[-1]         : {a[-1]}")
print(f"  a[3]          : {a[3]}")

sub("Slicing  a[start:stop:step]")
print(f"  a[2:6]        : {a[2:6]}")
print(f"  a[:5]         : {a[:5]}")
print(f"  a[5:]         : {a[5:]}")
print(f"  a[::2]        : {a[::2]}   (every 2nd)")
print(f"  a[::-1]       : {a[::-1]}  (reversed)")
print(f"  a[1:8:3]      : {a[1:8:3]}")

sub("Fancy indexing")
idx = np.array([0, 2, 4, 7])
print(f"  a[[0,2,4,7]]  : {a[idx]}")

sub("Boolean / Conditional indexing")
mask = a > 50
print(f"  mask (a>50)   : {mask}")
print(f"  a[a>50]       : {a[mask]}")
print(f"  a[a%20==0]    : {a[a % 20 == 0]}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("4. MODIFYING ARRAYS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5])

sub("Element assignment")
b = a.copy()
b[2] = 99
print(f"  b[2] = 99     : {b}")

sub("Slice assignment")
b = a.copy()
b[1:4] = 0
print(f"  b[1:4] = 0    : {b}")

sub("Boolean assignment")
b = a.copy()
b[b > 3] = -1
print(f"  b[b>3] = -1   : {b}")

sub("np.where")
result = np.where(a > 3, a * 10, a)
print(f"  np.where(a>3, a*10, a) : {result}")

sub("np.put / np.place")
b = np.array([10, 20, 30, 40, 50])
np.put(b, [1, 3], [200, 400])
print(f"  np.put(b,[1,3],[200,400]) : {b}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("5. ARITHMETIC OPERATIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

sub("Element-wise operations")
print(f"  a          : {a}")
print(f"  b          : {b}")
print(f"  a + b      : {a + b}")
print(f"  b - a      : {b - a}")
print(f"  a * b      : {a * b}")
print(f"  b / a      : {b / a}")
print(f"  b // a     : {b // a}   (floor div)")
print(f"  a ** 2     : {a ** 2}")
print(f"  b % 3      : {b % 3}")

sub("Scalar broadcasting")
print(f"  a + 100    : {a + 100}")
print(f"  a * 3      : {a * 3}")
print(f"  a / 2      : {a / 2}")
print(f"  a ** 0.5   : {a ** 0.5}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("6. MATHEMATICAL / UNIVERSAL FUNCTIONS (ufuncs)")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 4, 9, 16, 25], dtype=float)
b = np.array([0.0, 30.0, 45.0, 60.0, 90.0])  # degrees

sub("Power & roots")
print(f"  a              : {a}")
print(f"  np.sqrt(a)     : {np.sqrt(a)}")
print(f"  np.cbrt(a)     : {np.cbrt(a).round(3)}")
print(f"  np.square(a)   : {np.square(a)}")
print(f"  np.power(a,3)  : {np.power(a,3)}")

sub("Exponential & Logarithm")
x = np.array([1.0, 2.0, 3.0, 4.0])
print(f"  np.exp(x)      : {np.exp(x).round(3)}")
print(f"  np.exp2(x)     : {np.exp2(x)}")
print(f"  np.log(x)      : {np.log(x).round(3)}")
print(f"  np.log2(x)     : {np.log2(x)}")
print(f"  np.log10(x)    : {np.log10(x).round(3)}")
print(f"  np.log1p(x)    : {np.log1p(x).round(3)}")

sub("Trigonometry")
rad = np.deg2rad(b)
print(f"  deg            : {b}")
print(f"  np.sin         : {np.sin(rad).round(3)}")
print(f"  np.cos         : {np.cos(rad).round(3)}")
print(f"  np.tan         : {np.tan(rad).round(3)}")
print(f"  np.arcsin(0..1): {np.arcsin(np.linspace(0,1,4)).round(3)}")

sub("Rounding")
r = np.array([1.2, 2.5, 3.7, -1.5, -2.8])
print(f"  array          : {r}")
print(f"  np.round(a,1)  : {np.round(r, 1)}")
print(f"  np.floor       : {np.floor(r)}")
print(f"  np.ceil        : {np.ceil(r)}")
print(f"  np.trunc       : {np.trunc(r)}")
print(f"  np.fix         : {np.fix(r)}")

sub("Absolute value / sign")
s = np.array([-3, -2, 0, 2, 3])
print(f"  np.abs(s)      : {np.abs(s)}")
print(f"  np.sign(s)     : {np.sign(s)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("7. STATISTICAL OPERATIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([4, 7, 2, 9, 1, 5, 8, 3, 6, 10])
print(f"  Array          : {a}")
print()
print(f"  np.sum         : {np.sum(a)}")
print(f"  np.prod        : {np.prod(a)}")
print(f"  np.mean        : {np.mean(a)}")
print(f"  np.median      : {np.median(a)}")
print(f"  np.std         : {np.std(a):.4f}")
print(f"  np.var         : {np.var(a):.4f}")
print(f"  np.min         : {np.min(a)}")
print(f"  np.max         : {np.max(a)}")
print(f"  np.ptp (range) : {np.ptp(a)}")
print(f"  np.argmin      : {np.argmin(a)}  (index of min)")
print(f"  np.argmax      : {np.argmax(a)}  (index of max)")
print(f"  np.cumsum      : {np.cumsum(a)}")
print(f"  np.cumprod     : {np.cumprod(a)}")
print(f"  np.diff        : {np.diff(a)}")
print(f"  np.percentile(25,50,75): {np.percentile(a, [25,50,75])}")
print(f"  np.quantile(.25,.75)   : {np.quantile(a, [0.25, 0.75])}")
print(f"  np.nanmean (w/nan)     : {np.nanmean(np.array([1,2,np.nan,4]))}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("8. SORTING & SEARCHING")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([5, 3, 8, 1, 9, 2, 7, 4, 6])
print(f"  Array          : {a}")

sub("Sorting")
print(f"  np.sort        : {np.sort(a)}")
print(f"  np.sort desc   : {np.sort(a)[::-1]}")
print(f"  np.argsort     : {np.argsort(a)}  (indices)")

sub("Searching")
print(f"  np.argmin      : {np.argmin(a)}")
print(f"  np.argmax      : {np.argmax(a)}")
print(f"  np.where(a>5)  : {np.where(a > 5)}")
print(f"  np.nonzero     : {np.nonzero(a > 5)}")
sorted_a = np.sort(a)
print(f"  np.searchsorted: {np.searchsorted(sorted_a, 5)}  (insert pos for 5)")

sub("Unique values")
b = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
print(f"  Array          : {b}")
vals, counts = np.unique(b, return_counts=True)
print(f"  np.unique      : {vals}")
print(f"  counts         : {counts}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("9. RESHAPING & MANIPULATION")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.arange(1, 13)
print(f"  arange(1,13)   : {a}")

sub("Reshape")
print(f"  reshape(3,4):\n{a.reshape(3, 4)}")
print(f"  reshape(2,6):\n{a.reshape(2, 6)}")

sub("Flatten / ravel")
mat = a.reshape(3, 4)
print(f"  flatten()      : {mat.flatten()}")
print(f"  ravel()        : {mat.ravel()}")

sub("Resize / repeat / tile")
small = np.array([1, 2, 3])
print(f"  np.repeat(x,3) : {np.repeat(small, 3)}")
print(f"  np.tile(x,3)   : {np.tile(small, 3)}")

sub("Append / insert / delete")
a = np.array([1, 2, 3, 4, 5])
print(f"  np.append(a,6)        : {np.append(a, 6)}")
print(f"  np.insert(a,2,99)     : {np.insert(a, 2, 99)}")
print(f"  np.delete(a,2)        : {np.delete(a, 2)}")

sub("Flip / roll / rotate")
print(f"  np.flip(a)     : {np.flip(a)}")
print(f"  np.roll(a,2)   : {np.roll(a, 2)}")

sub("Padding / trimming")
print(f"  np.pad(a,2)    : {np.pad(a, 2)}")
print(f"  np.trim_zeros  : {np.trim_zeros(np.array([0,0,1,2,3,0]))}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("10. CONCATENATION & SPLITTING")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([7, 8, 9])

sub("Concatenation")
print(f"  np.concatenate([a,b,c])  : {np.concatenate([a, b, c])}")
print(f"  np.hstack([a,b,c])       : {np.hstack([a, b, c])}")
print(f"  np.r_[a, b, c]           : {np.r_[a, b, c]}")

sub("Splitting")
full = np.arange(1, 13)
print(f"  np.split(arr,3)          : {np.split(full, 3)}")
print(f"  np.array_split(arr,5)    : {np.array_split(full, 5)}")
print(f"  np.hsplit(arr,4)         : {np.hsplit(full, 4)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("11. SET OPERATIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5, 6])
b = np.array([4, 5, 6, 7, 8, 9])
print(f"  a                     : {a}")
print(f"  b                     : {b}")
print(f"  np.union1d            : {np.union1d(a, b)}")
print(f"  np.intersect1d        : {np.intersect1d(a, b)}")
print(f"  np.setdiff1d(a,b)     : {np.setdiff1d(a, b)}")
print(f"  np.setdiff1d(b,a)     : {np.setdiff1d(b, a)}")
print(f"  np.setxor1d           : {np.setxor1d(a, b)}")
print(f"  np.isin(a,b)          : {np.isin(a, b)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("12. COMPARISON & LOGICAL OPERATIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 5, 3, 8, 2])
b = np.array([2, 4, 3, 7, 5])
print(f"  a              : {a}")
print(f"  b              : {b}")

sub("Comparisons")
print(f"  a == b         : {a == b}")
print(f"  a != b         : {a != b}")
print(f"  a >  b         : {a >  b}")
print(f"  a >= b         : {a >= b}")
print(f"  a <  b         : {a <  b}")
print(f"  np.equal       : {np.equal(a, b)}")
print(f"  np.greater     : {np.greater(a, b)}")

sub("Logical operations")
x = np.array([True, False, True, False])
y = np.array([True, True, False, False])
print(f"  np.logical_and : {np.logical_and(x, y)}")
print(f"  np.logical_or  : {np.logical_or(x, y)}")
print(f"  np.logical_xor : {np.logical_xor(x, y)}")
print(f"  np.logical_not : {np.logical_not(x)}")

sub("Any / All")
a = np.array([0, 1, 2, 3, 4])
print(f"  np.any(a>3)    : {np.any(a > 3)}")
print(f"  np.all(a>0)    : {np.all(a > 0)}")
print(f"  np.any(a<0)    : {np.any(a < 0)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("13. BITWISE OPERATIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([0b1010, 0b1100, 0b1111], dtype=np.int32)
b = np.array([0b1001, 0b1010, 0b0101], dtype=np.int32)
print(f"  a (bin)        : {[bin(x) for x in a]}")
print(f"  b (bin)        : {[bin(x) for x in b]}")
print(f"  np.bitwise_and : {[bin(x) for x in np.bitwise_and(a,b)]}")
print(f"  np.bitwise_or  : {[bin(x) for x in np.bitwise_or(a,b)]}")
print(f"  np.bitwise_xor : {[bin(x) for x in np.bitwise_xor(a,b)]}")
print(f"  np.invert(a)   : {np.invert(a)}")
print(f"  np.left_shift  : {np.left_shift(a, 1)}")
print(f"  np.right_shift : {np.right_shift(a, 1)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("14. LINEAR ALGEBRA (1D context)")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5], dtype=float)
b = np.array([5, 4, 3, 2, 1], dtype=float)
print(f"  a              : {a}")
print(f"  b              : {b}")
print(f"  np.dot(a,b)    : {np.dot(a, b)}")
print(f"  a @ b          : {a @ b}   (dot product)")
print(f"  np.inner(a,b)  : {np.inner(a, b)}")
print(f"  np.cross(a,b)  : only first 3 → {np.cross(a[:3], b[:3])}")
print(f"  np.outer(a,b):\n{np.outer(a[:4], b[:4])}")
print(f"  np.linalg.norm : {np.linalg.norm(a):.4f}  (L2 norm)")
print(f"  np.linalg.norm(L1): {np.linalg.norm(a, ord=1)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("15. TYPE CASTING")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1.7, 2.3, 3.9, 4.1])
print(f"  float64 array  : {a}")
print(f"  .astype(int)   : {a.astype(int)}")
print(f"  .astype(str)   : {a.astype(str)}")
print(f"  .astype(bool)  : {a.astype(bool)}")
print(f"  .astype(complex): {a.astype(complex)}")
print(f"  .astype(np.float32): {a.astype(np.float32)}")

b = np.array([0, 1, 0, 1, 1])
print(f"\n  int array      : {b}")
print(f"  .astype(bool)  : {b.astype(bool)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("16. COPY vs VIEW")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5])
sub("View (shallow) — shares memory")
view = a[1:4]
view[0] = 99
print(f"  original after modifying view : {a}  ← CHANGED")

sub("Copy (deep) — independent")
a = np.array([1, 2, 3, 4, 5])
copy = a.copy()
copy[0] = 99
print(f"  original after modifying copy : {a}  ← unchanged")
print(f"  np.may_share_memory(a,view)   : {np.may_share_memory(a, a[1:4])}")
print(f"  np.may_share_memory(a,copy)   : {np.may_share_memory(a, copy)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("17. NaN & INF HANDLING")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1.0, np.nan, 3.0, np.inf, -np.inf, 5.0])
print(f"  Array          : {a}")
print(f"  np.isnan       : {np.isnan(a)}")
print(f"  np.isinf       : {np.isinf(a)}")
print(f"  np.isfinite    : {np.isfinite(a)}")
print(f"  np.nan_to_num  : {np.nan_to_num(a)}")
print(f"  np.nansum      : {np.nansum(a)}")
print(f"  np.nanmean     : {np.nanmean(a):.2f}")
print(f"  np.nanmin      : {np.nanmin(a)}")
print(f"  np.nanmax      : {np.nanmax(a)}")
print(f"  np.nanstd      : {np.nanstd(a):.4f}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("18. STRING OPERATIONS (np.char)")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array(["hello", "world", "numpy", "arrays"])
print(f"  Array                    : {a}")
print(f"  np.char.upper            : {np.char.upper(a)}")
print(f"  np.char.capitalize       : {np.char.capitalize(a)}")
print(f"  np.char.add (concat)     : {np.char.add(a, '!')}")
print(f"  np.char.str_len          : {np.char.str_len(a)}")
print(f"  np.char.find('o')        : {np.char.find(a, 'o')}")
print(f"  np.char.startswith('n')  : {np.char.startswith(a, 'n')}")
print(f"  np.char.replace          : {np.char.replace(a, 'a', '@')}")
print(f"  np.char.split            : {np.char.split(np.array(['a b', 'c d']))}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("19. BROADCASTING RULES")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([1, 2, 3, 4, 5])
print(f"  1D + scalar     : {a + 10}")
print(f"  1D * scalar     : {a * 3}")
print(f"  1D ** scalar    : {a ** 2}")
print(f"  np.add.outer(a,[1,2]):\n{np.add.outer(a, np.array([1, 2]))}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("20. SAVE & LOAD")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([10, 20, 30, 40, 50])

sub("Binary .npy format")
np.save("temp_arr.npy", a)
loaded = np.load("temp_arr.npy")
print(f"  Saved & loaded  : {loaded}")

sub("Text .txt format")
np.savetxt("temp_arr.txt", a, fmt="%d")
loaded_txt = np.loadtxt("temp_arr.txt", dtype=int)
print(f"  savetxt/loadtxt : {loaded_txt}")

sub("Multiple arrays .npz")
b = np.array([100, 200, 300])
np.savez("arrays.npz", first=a, second=b)
data = np.load("arrays.npz")
print(f"  savez first     : {data['first']}")
print(f"  savez second    : {data['second']}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sep("21. USEFUL UTILITY FUNCTIONS")
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print(f"  Array           : {a}")
print(f"  np.count_nonzero: {np.count_nonzero(a)}")
print(f"  np.clip(2,7)    : {np.clip(a, 2, 7)}")
print(f"  np.histogram    : vals={np.histogram(a, bins=3)[0]}  edges={np.histogram(a, bins=3)[1]}")
print(f"  np.digitize     : {np.digitize(a, bins=[2,5,8])}")
print(f"  np.convolve     : {np.convolve(np.array([1,2,3]), np.array([0,1,0]))}")
print(f"  np.correlate    : {np.correlate(a[:5], np.array([1,0,-1]))}")
print(f"  np.gradient     : {np.gradient(a)}")
print(f"  np.ediff1d      : {np.ediff1d(a)}")
print(f"  np.interp       : {np.interp([1.5, 3.5], [1,2,3,4], [10,20,30,40])}")
print(f"  np.around(pi,3) : {np.around(np.pi, 3)}")
