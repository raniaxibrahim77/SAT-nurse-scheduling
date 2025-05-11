import sys
import os
import json
import threading

sys.setrecursionlimit(10_000)

from sat_solvers import resolution_sat, dp_sat, dpll_sat, cdcl_sat

def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        inst = json.load(f)
    return inst["clauses"]

def load_dimacs(path):
    clauses = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line[0] in ('c', 'p'):
                continue
            lits = [int(x) for x in line.split()]
            clauses.append(lits[:-1])
    return clauses

def run_with_timeout(fn, args=(), timeout=2.0):
    result = {}
    def target():
        try:
            result['val'] = fn(*args)
        except Exception as e:
            result['val'] = e
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()
    t.join(timeout)
    if t.is_alive():
        return None, True
    return result.get('val'), False

if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "data/example.json"
    ext = os.path.splitext(fn)[1].lower()

    if ext == ".json":
        cnf = load_json(fn)
    elif ext in (".cnf", ".dimacs"):
        cnf = load_dimacs(fn)
    else:
        print(f"Unknown extension '{ext}'. Use .json or .cnf")
        sys.exit(1)

    for name, solver in [
        ("Resolution", resolution_sat),
        ("DP",         dp_sat),
        ("DPLL",       dpll_sat),
        ("CDCL",       cdcl_sat),
    ]:
        if name == "DP":
            sat, timed_out = run_with_timeout(solver, (cnf,), timeout=2.0)
            if timed_out:
                print(f"{name:>10}: Timeout (skipped)")
                continue
            if isinstance(sat, Exception):
                print(f"{name:>10}: {type(sat).__name__}")
                continue
        else:
            try:
                sat = solver(cnf)
            except Exception as e:
                print(f"{name:>10}: {type(e).__name__}")
                continue

        print(f"{name:>10}: {'SAT' if sat else 'UNSAT'}")
