"""Command-line entry point: ``scm-sim --days 10 --seed 42`` (or ``python -m scm_sim``)."""
from __future__ import annotations

import argparse
import csv
from typing import List, Optional

from scm_sim.analytics import format_run_summary, summarize_run
from scm_sim.simulator import build_demo, describe_day, metrics_rows


def main(argv: Optional[List[str]] = None) -> int:
    """Run the demo scenario, print a day-by-day summary and the final report."""
    parser = argparse.ArgumentParser(
        prog="scm-sim", description="Run the Supply Chain Management Simulator demo."
    )
    parser.add_argument("--days", type=int, default=10, help="days to simulate (default 10)")
    parser.add_argument("--seed", type=int, default=42, help="random seed (default 42)")
    parser.add_argument(
        "--summary", action="store_true", help="print a summary over all days"
    )
    parser.add_argument("--csv", metavar="PATH", help="write daily metrics to a CSV file")
    args = parser.parse_args(argv)
    if args.days < 1:
        parser.error("--days must be at least 1")

    sim = build_demo(seed=args.seed)
    print(f"Supply Chain Simulator demo: {args.days} day(s), seed {args.seed}\n")
    for report in sim.run(args.days):
        print(describe_day(sim.logs[report["day"] - 1], report))
    print()
    print(sim.final_summary())
    if args.summary:
        print()
        print(format_run_summary(summarize_run(sim.history)))
    if args.csv:
        fieldnames = [
            "day",
            "delayed",
            "stockouts",
            "low_stock",
            "excess",
            "pending",
            "fulfilled",
            "backordered",
            "cancelled",
            "fill_rate",
        ]
        with open(args.csv, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(metrics_rows(sim.history))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
