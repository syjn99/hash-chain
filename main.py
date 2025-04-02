import argparse

from analyze import run_analysis
from cycle import find_cycle
from collision import find_collision

MY_STUDENT_ID = "20180334"


def main():
    parser = argparse.ArgumentParser(description="MD5 Hash Chain Analyzer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Analyze hash graph (4-a)")
    analyze.add_argument("--k", type=int, default=16, help="Number of bits in hash value")

    cycle = subparsers.add_parser("cycle", help="Find cycle in hash function (4-d)")
    cycle.add_argument("--k", type=int, required=True, help="Number of bits in hash value")
    cycle.add_argument("--iv", type=str, default=MY_STUDENT_ID, help="Initial value")

    collision = subparsers.add_parser("collision", help="Find hash collision (4-e)")
    collision.add_argument("--k", type=int, required=True, help="Number of bits in hash value")
    collision.add_argument("--iv", type=str, default=MY_STUDENT_ID, help="Initial value")

    args = parser.parse_args()

    if args.command == "analyze":
        run_analysis(args.k)
    elif args.command == "cycle":
        find_cycle(args.k, args.iv)
    elif args.command == "collision":
        find_collision(args.k, args.iv)


if __name__ == "__main__":
    main()
