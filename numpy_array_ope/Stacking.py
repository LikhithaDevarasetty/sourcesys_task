import numpy as np
import sys

 
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = np.array([7, 8, 9])
 

print(f"  a={a}  b={b}  c={c}")
s0 = np.stack([a, b, c], axis=0)
print(f"\n  np.stack(axis=0) → shape {s0.shape}:\n{s0}  (rows stacked)")
s1 = np.stack([a, b, c], axis=1)
print(f"\n  np.stack(axis=1) → shape {s1.shape}:\n{s1}  (cols stacked)")
 

vs = np.vstack([a, b, c])
print(f"  np.vstack shape {vs.shape}:\n{vs}")
# Works on 2D too
m1 = np.array([[1,2],[3,4]])
m2 = np.array([[5,6],[7,8]])
print(f"\n  vstack of 2D matrices shape {np.vstack([m1,m2]).shape}:\n{np.vstack([m1,m2])}")
 

hs = np.hstack([a, b, c])
print(f"  np.hstack (1D):   {hs}  shape={hs.shape}")
print(f"  np.hstack (2D) shape {np.hstack([m1,m2]).shape}:\n{np.hstack([m1, m2])}")
 

cs = np.column_stack([a, b, c])
print(f"  np.column_stack shape {cs.shape}:\n{cs}")
print(f"  ↑ Each 1D array becomes a COLUMN  ← key difference from hstack")
# Mixed 1D[2] and 2D[2x2] — rows must match
a2r = np.array([10, 20])
mixed = np.column_stack([a2r, m1])
print("  column_stack(1D[2]+2D[2x2]) shape", mixed.shape, ":\n", mixed)
 
 
 

rs = np.row_stack([a, b, c])
print(f"  np.row_stack shape {rs.shape}:\n{rs}")
 

ds = np.dstack([a, b, c])
print(f"  np.dstack shape {ds.shape}:\n{ds}")
 

print(f"  concatenate axis=0: {np.concatenate([a,b,c], axis=0)}")
print(f"  concatenate 2D r0:  shape={np.concatenate([m1,m2], axis=0).shape}")
print(f"  concatenate 2D c1:  shape={np.concatenate([m1,m2], axis=1).shape}")
 

block = np.block([[m1, m2],
                  [m2, m1]])
print(f"  np.block 4x4:\n{block}")
 
