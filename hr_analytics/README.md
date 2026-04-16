# 📊 HR Analytics Mini Project

Generates a synthetic employee dataset using Python's `random` module and prints analytics reports — **no external dependencies**.

## Files
| File | Purpose |
|---|---|
| `data_generator.py` | Constants + dataset generation |
| `analysis.py` | All 9 reporting functions |
| `main.py` | Entry point |

## Run
```bash
python main.py
```
> Requires Python 3.8+. No `pip install` needed.

## Config
Edit these in `main.py`:
```python
NUM_RECORDS = 200   # employees to generate
TOP_N       = 5     # top earners to show
SAMPLE_ROWS = 8     # sample rows to print
```

## Libraries Used
`random` · `statistics` · `collections`