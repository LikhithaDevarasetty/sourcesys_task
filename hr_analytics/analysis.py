
import statistics
from collections import defaultdict, Counter
from data_generator import DEPARTMENTS, CITIES

# ── DISPLAY HELPERS ────────────────────────────────────────

def separator(title=""):
    width = 60
    if title:
        print(f"\n{'─'*5} {title} {'─'*(width - len(title) - 7)}")
    else:
        print("─" * width)

def bar(value, max_val, width=28, char="█"):
    filled = int((value / max_val) * width)
    return char * filled + "░" * (width - filled)


# ── ANALYSIS FUNCTIONS ─────────────────────────────────────

def overview(data):
    
    separator("DATASET OVERVIEW")
    salaries = [e["salary"]      for e in data]
    perfs    = [e["performance"] for e in data]
    ages     = [e["age"]         for e in data]
    exps     = [e["experience"]  for e in data]

    print(f"  Total Records     : {len(data)}")
    print(f"  Departments       : {len(DEPARTMENTS)}")
    print(f"  Cities            : {len(CITIES)}")
    print()
    print(f"  Salary  → Min: ${min(salaries):,}  |  Max: ${max(salaries):,}  |  "
          f"Avg: ${statistics.mean(salaries):,.0f}  |  Median: ${statistics.median(salaries):,.0f}")
    print(f"  Perf    → Min: {min(perfs)}        |  Max: {max(perfs)}        |  Avg: {statistics.mean(perfs):.2f}")
    print(f"  Age     → Min: {min(ages)}          |  Max: {max(ages)}          |  Avg: {statistics.mean(ages):.1f}")
    print(f"  Exp     → Min: {min(exps)}           |  Max: {max(exps)}          |  Avg: {statistics.mean(exps):.1f} yrs")


def dept_analysis(data):
    
    separator("DEPARTMENT ANALYSIS")
    groups = defaultdict(list)
    for e in data:
        groups[e["department"]].append(e)

    max_salary = max(statistics.mean(v["salary"] for v in g) for g in groups.values())

    print(f"  {'Department':<14} {'Count':>5}  {'Avg Salary':>11}  {'Avg Perf':>9}  {'Avg Age':>8}  Chart")
    print(f"  {'─'*14} {'─'*5}  {'─'*11}  {'─'*9}  {'─'*8}  {'─'*28}")

    for dept in sorted(groups, key=lambda d: -statistics.mean(e["salary"] for e in groups[d])):
        g       = groups[dept]
        avg_sal = statistics.mean(e["salary"]      for e in g)
        avg_prf = statistics.mean(e["performance"] for e in g)
        avg_age = statistics.mean(e["age"]         for e in g)
        b       = bar(avg_sal, max_salary)
        print(f"  {dept:<14} {len(g):>5}  ${avg_sal:>10,.0f}  {avg_prf:>9.2f}  {avg_age:>8.1f}  {b}")


def salary_distribution(data):
    
    separator("SALARY DISTRIBUTION")
    buckets = {
        "  $40k – $60k ": 0, "  $60k – $80k ": 0,
        "  $80k – $100k": 0, "  $100k – $120k": 0,
        "  $120k+      ": 0
    }
    for e in data:
        s = e["salary"]
        if   s < 60000:  buckets["  $40k – $60k "]  += 1
        elif s < 80000:  buckets["  $60k – $80k "]  += 1
        elif s < 100000: buckets["  $80k – $100k"] += 1
        elif s < 120000: buckets["  $100k – $120k"] += 1
        else:            buckets["  $120k+      "]  += 1

    max_count = max(buckets.values())
    for label, count in buckets.items():
        pct = count / len(data) * 100
        b   = bar(count, max_count)
        print(f"  {label}  {b}  {count:>3} ({pct:.1f}%)")


def performance_distribution(data):
    
    separator("PERFORMANCE RATING DISTRIBUTION")
    ratings = [round(e["performance"] * 2) / 2 for e in data]
    freq    = sorted(Counter(ratings).items())
    max_f   = max(v for _, v in freq)

    for rating, count in freq:
        stars = "★" * int(rating) + "☆" * (5 - int(rating))
        b     = bar(count, max_f, width=24)
        print(f"  {rating:.1f}  {stars}  {b}  {count:>3}")


def city_analysis(data):
    
    separator("CITY BREAKDOWN")
    groups = defaultdict(list)
    for e in data:
        groups[e["city"]].append(e)

    max_sal = max(statistics.mean(e["salary"] for e in g) for g in groups.values())

    print(f"  {'City':<16} {'Employees':>10}  {'Avg Salary':>12}  Chart")
    print(f"  {'─'*16} {'─'*10}  {'─'*12}  {'─'*24}")
    for city in sorted(groups, key=lambda c: -statistics.mean(e["salary"] for e in groups[c])):
        g       = groups[city]
        avg_sal = statistics.mean(e["salary"] for e in g)
        b       = bar(avg_sal, max_sal, width=24)
        print(f"  {city:<16} {len(g):>10}  ${avg_sal:>11,.0f}  {b}")


def top_earners(data, n=5):
    
    separator(f"TOP {n} EARNERS")
    top = sorted(data, key=lambda e: -e["salary"])[:n]
    print(f"  {'Rank':<5} {'ID':>4}  {'Department':<14} {'City':<16} {'Age':>4}  {'Exp':>4}  {'Salary':>10}  {'Perf':>5}")
    print(f"  {'─'*5} {'─'*4}  {'─'*14} {'─'*16} {'─'*4}  {'─'*4}  {'─'*10}  {'─'*5}")
    for rank, e in enumerate(top, 1):
        print(f"  {rank:<5} #{e['id']:>3}  {e['department']:<14} {e['city']:<16} "
              f"{e['age']:>4}  {e['experience']:>3}y  ${e['salary']:>9,}  {e['performance']:>5.1f}")


def correlation_insight(data):
    
    separator("INSIGHTS: EXPERIENCE vs SALARY")
    buckets = defaultdict(list)
    for e in data:
        tier = (e["experience"] // 5) * 5   # 0-4, 5-9, 10-14, …
        buckets[tier].append(e["salary"])

    print(f"  {'Exp Range':<12} {'Employees':>10}  {'Avg Salary':>12}  Trend")
    print(f"  {'─'*12} {'─'*10}  {'─'*12}  {'─'*20}")
    prev = None
    for tier in sorted(buckets):
        avg   = statistics.mean(buckets[tier])
        trend = ""
        if prev is not None:
            trend = ("↑ +" if avg > prev else "↓ -") + f"${abs(avg - prev):,.0f}"
        label = f"{tier}-{tier+4} yrs"
        print(f"  {label:<12} {len(buckets[tier]):>10}  ${avg:>11,.0f}  {trend}")
        prev = avg


def dept_performance_rank(data):
    
    separator("DEPARTMENT PERFORMANCE RANKING")
    groups = defaultdict(list)
    for e in data:
        groups[e["department"]].append(e["performance"])

    ranked = sorted(groups.items(), key=lambda x: -statistics.mean(x[1]))
    max_p  = statistics.mean(ranked[0][1])

    print(f"  {'Rank':<5} {'Department':<14} {'Avg Perf':>9}  {'Std Dev':>8}  Chart")
    print(f"  {'─'*5} {'─'*14} {'─'*9}  {'─'*8}  {'─'*24}")
    for i, (dept, perfs) in enumerate(ranked, 1):
        avg = statistics.mean(perfs)
        std = statistics.stdev(perfs) if len(perfs) > 1 else 0
        b   = bar(avg, max_p, width=24)
        print(f"  {i:<5} {dept:<14} {avg:>9.2f}  {std:>8.2f}  {b}")


def sample_records(data, n=8):
    
    separator(f"SAMPLE RECORDS (first {n})")
    print(f"  {'ID':>4}  {'Department':<14} {'City':<16} {'Age':>4}  {'Exp':>4}  {'Salary':>10}  {'Perf':>5}")
    print(f"  {'─'*4}  {'─'*14} {'─'*16} {'─'*4}  {'─'*4}  {'─'*10}  {'─'*5}")
    for e in data[:n]:
        print(f"  #{e['id']:>3}  {e['department']:<14} {e['city']:<16} "
              f"{e['age']:>4}  {e['experience']:>3}y  ${e['salary']:>9,}  {e['performance']:>5.1f}")