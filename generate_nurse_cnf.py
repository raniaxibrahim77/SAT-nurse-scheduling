#!/usr/bin/env python3
import json
import itertools
import os
import argparse


def var(n, d, s, D, S):
    return (n - 1) * (D * S) + (d - 1) * S + s


def generate_clauses(N, D, S):
    clauses = []
    for d in range(1, D + 1):
        for s, k in ((1, 2), (2, 2), (3, 1)):
            vs = [var(n, d, s, D, S) for n in range(1, N + 1)]
            for combo in itertools.combinations(vs, N - k + 1):
                clauses.append(list(combo))
            for combo in itertools.combinations(vs, k + 1):
                clauses.append([-v for v in combo])
    for n in range(1, N + 1):
        off_clause = [
            -var(n, d, s, D, S)
            for d in range(1, D + 1)
            for s in range(1, S + 1)
        ]
        clauses.append(off_clause)
    for n in range(1, N + 1):
        for d in range(1, D):
            clauses.append([-var(n, d, 3, D, S), -var(n, d + 1, 1, D, S)])
    clauses.append([var(1, 2, 1, D, S)])
    clauses.append([var(2, 7, 2, D, S)])
    return clauses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nurses", type=int, default=6)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--shifts", type=int, default=3)
    parser.add_argument(
        "-o", "--output", default="data/nurse7x3.json"
    )
    args = parser.parse_args()

    N, D, S = args.nurses, args.days, args.shifts
    clauses = generate_clauses(N, D, S)
    instance = {"num_vars": N * D * S, "clauses": clauses}

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(instance, f, indent=2)


if __name__ == "__main__":
    main()
