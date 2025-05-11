#!/usr/bin/env python3
import json
import argparse


def dump_dimacs(json_path, dimacs_path=None):
    with open(json_path) as f:
        inst = json.load(f)
    num_vars = inst.get(
        "num_vars",
        max(abs(l) for clause in inst["clauses"] for l in clause)
    )
    clauses = inst["clauses"]
    lines = [f"p cnf {num_vars} {len(clauses)}"]
    for clause in clauses:
        lines.append(" ".join(map(str, clause)) + " 0")
    output = "\n".join(lines)

    if dimacs_path:
        with open(dimacs_path, "w") as out:
            out.write(output)
        print(f"Written DIMACS to {dimacs_path}")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(description="Convert JSON CNF to DIMACS format")
    parser.add_argument("input", help="Path to JSON file")
    parser.add_argument("output", nargs="?", help="Output DIMACS file")
    args = parser.parse_args()

    dump_dimacs(args.input, args.output)


if __name__ == "__main__":
    main()
