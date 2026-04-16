
from data_generator import generate_dataset
from analysis import (
    separator,
    overview,
    dept_analysis,
    salary_distribution,
    performance_distribution,
    city_analysis,
    top_earners,
    correlation_insight,
    dept_performance_rank,
    sample_records,
)

# ── CONFIGURATION ──────────────────────────────────────────
NUM_RECORDS  = 200
TOP_N        = 5
SAMPLE_ROWS  = 8

# ── MAIN ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("   HR ANALYTICS MINI PROJECT")
    print(f"   Dataset: Python random module  |  Records: {NUM_RECORDS}")
    print("=" * 60)

    # Step 1 — Generate dataset
    dataset = generate_dataset(NUM_RECORDS)

    # Step 2 — Run all analyses
    overview(dataset)
    dept_analysis(dataset)
    salary_distribution(dataset)
    performance_distribution(dataset)
    city_analysis(dataset)
    top_earners(dataset, n=TOP_N)
    correlation_insight(dataset)
    dept_performance_rank(dataset)
    sample_records(dataset, n=SAMPLE_ROWS)

    # Step 3 — Done
    separator()
    print(f"  ✓ Analysis complete. Total employees processed: {len(dataset)}")
    print("=" * 60)