
import random

# ── CONSTANTS ──────────────────────────────────────────────
random.seed(42)

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
CITIES      = ["New York", "San Francisco", "Chicago", "Austin", "Seattle", "Boston"]
SALARY_BASE = {
    "Engineering": 95000, "Marketing": 72000, "Sales": 68000,
    "HR": 60000, "Finance": 85000, "Operations": 65000
}

# ── DATASET GENERATION ─────────────────────────────────────
def generate_dataset(n=200):
  
    employees = []
    for i in range(1, n + 1):
        dept   = random.choice(DEPARTMENTS)
        city   = random.choice(CITIES)
        age    = random.randint(22, 58)
        exp    = random.randint(0, 25)
        salary = int(SALARY_BASE[dept] + random.gauss(0, 12000))
        salary = max(40000, min(salary, 160000))   # clamp to realistic range
        perf   = round(random.uniform(2.5, 5.0), 1)

        employees.append({
            "id":          i,
            "department":  dept,
            "city":        city,
            "age":         age,
            "experience":  exp,
            "salary":      salary,
            "performance": perf,
        })
    return employees