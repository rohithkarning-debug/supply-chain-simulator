"""Command-line entry point: ``python -m scm_sim --days 10 --seed 42``."""
from __future__ import annotations

import argparse
from typing import List, Optional

from scm_sim.simulator import build_demo, describe_day


def main(argv: Optional[List[str]] = None) -> int:
    """Run the demo scenario, print a day-by-day summary and the final report."""
    parser = argparse.ArgumentParser(
        prog="scm_sim", description="Run the Supply Chain Management Simulator demo."
    )
    parser.add_argument("--days", type=int, default=10, help="days to simulate (default 10)")
    parser.add_argument("--seed", type=int, default=42, help="random seed (default 42)")
    args = parser.parse_args(argv)
    if args.days < 1:
        parser.error("--days must be at least 1")

    sim = build_demo(seed=args.seed)
    print(f"Supply Chain Simulator demo: {args.days} day(s), seed {args.seed}\n")
    for report in sim.run(args.days):
        print(describe_day(sim.logs[report["day"] - 1], report))
    print()
    print(sim.final_summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
