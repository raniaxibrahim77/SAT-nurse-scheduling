import json
import sys
import time
import threading
import os
import psutil

from sat_solvers import resolution_sat, dp_sat, dpll_sat, cdcl_sat

SOLVERS = [
    ("Resolution", resolution_sat),
    ("DP",         dp_sat),
    ("DPLL",       dpll_sat),
    ("CDCL",       cdcl_sat),
]

def run_with_timeout_and_memory(fn, args=(), timeout=2.0, sample_interval=0.01):
    result = {}
    proc = psutil.Process(os.getpid())
    peak_rss = 0
    done = threading.Event()

    def monitor():
        nonlocal peak_rss
        while not done.is_set():
            rss = proc.memory_info().rss
            if rss > peak_rss:
                peak_rss = rss
            time.sleep(sample_interval)

    def target():
        try:
            result['val'] = fn(*args)
        except Exception as e:
            result['val'] = e
        finally:
            done.set()

    mon = threading.Thread(target=monitor, daemon=True)
    mon.start()
    worker = threading.Thread(target=target, daemon=True)
    start = time.perf_counter()
    worker.start()
    worker.join(timeout)
    elapsed = time.perf_counter() - start

    if worker.is_alive():
        done.set()
        return None, True, peak_rss, elapsed

    done.set()
    mon.join()
    return result.get('val'), False, peak_rss, elapsed

def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)["clauses"]

def main():
    inst_path = sys.argv[1] if len(sys.argv) > 1 else "data/nurse7x3.json"
    cnf = load_json(inst_path)

    print(f"Benchmark on {inst_path}\n")
    print(f"{'Solver':<10} {'Result':<12} {'Time (s)':>8} {'Mem (MB)':>8}")
    print("-" * 46)

    for name, solver in SOLVERS:
        if name == "DP":
            sat, timed_out, peak, elapsed = run_with_timeout_and_memory(
                solver, (cnf,), timeout=2.0
            )
            if timed_out:
                result = "Timeout"
            elif isinstance(sat, Exception):
                result = type(sat).__name__
            else:
                result = "SAT" if sat else "UNSAT"
        else:
            start = time.perf_counter()
            sat = solver(cnf)
            elapsed = time.perf_counter() - start
            result = "SAT" if sat else "UNSAT"
            peak = psutil.Process(os.getpid()).memory_info().rss

        print(f"{name:<10} {result:<12} {elapsed:8.4f} {peak/1024/1024:8.2f}")

if __name__ == "__main__":
    main()
