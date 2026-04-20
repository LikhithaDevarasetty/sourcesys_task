import numpy as np
import sys
sys.stdout.flush()
N = 1_000_000
print(f"  Array size: {N:,} elements\n")
 

f64 = np.ones(N, dtype=np.float64)
f32 = np.ones(N, dtype=np.float32)
f16 = np.ones(N, dtype=np.float16)
i32 = np.ones(N, dtype=np.int32)
i16 = np.ones(N, dtype=np.int16)
i8  = np.ones(N, dtype=np.int8)
u8  = np.ones(N, dtype=np.uint8)

def mem(arr, label=""):
    mb = arr.nbytes / 1024
    print(f"  {label:<35} dtype={str(arr.dtype):<10} bytes={arr.nbytes:>8,}  ({mb:.2f} KB)")
 
mem(f64, "float64 (default)")
mem(f32, "float32")
mem(f16, "float16")
mem(i32, "int32")
mem(i16, "int16")
mem(i8,  "int8")
mem(u8,  "uint8")
 

print(f"  float64  range  : {np.finfo(np.float64).min:.2e}  to  {np.finfo(np.float64).max:.2e}")
print(f"  float64  eps    : {np.finfo(np.float64).eps:.2e}")
print(f"  float32  range  : {np.finfo(np.float32).min:.2e}  to  {np.finfo(np.float32).max:.2e}")
print(f"  float32  eps    : {np.finfo(np.float32).eps:.2e}   ← less precise")
print(f"  float16  max    : {np.finfo(np.float16).max:.2e}   ← very limited!")
print(f"  int8     range  : {np.iinfo(np.int8).min}  to  {np.iinfo(np.int8).max}")
print(f"  int16    range  : {np.iinfo(np.int16).min}  to  {np.iinfo(np.int16).max}")
print(f"  int32    range  : {np.iinfo(np.int32).min}  to  {np.iinfo(np.int32).max}")
print(f"  uint8    range  : {np.iinfo(np.uint8).min}  to  {np.iinfo(np.uint8).max}   ← images!")


data = np.array([1.5, 2.7, 3.1, 4.9])
print(f"  Original: {data}  dtype={data.dtype}")
print(f"  can_cast float64→float32: {np.can_cast(data, np.float32)}")
print(f"  can_cast float64→int32  : {np.can_cast(data, np.int32)}")   # loses decimals
safe_f32 = data.astype(np.float32)
print(f"  After float32: {safe_f32}  bytes saved: {data.nbytes - safe_f32.nbytes}")
 

print(f"  float64 → float32 : saves {(f64.nbytes - f32.nbytes)/1024:.0f} KB  (50% reduction)")
print(f"  float64 → float16 : saves {(f64.nbytes - f16.nbytes)/1024:.0f} KB  (75% reduction)")
print(f"  int32   → int16   : saves {(i32.nbytes - i16.nbytes)/1024:.0f} KB  (50% reduction)")
print(f"  int32   → int8    : saves {(i32.nbytes - i8.nbytes)/1024:.0f} KB  (75% reduction)")