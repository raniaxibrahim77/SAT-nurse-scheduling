# NSP-SAT Solver Suite

This project implements a simple SAT-based approach to solving the **Nurse Scheduling Problem (NSP)** using four classical SAT solving algorithms:  
1. Resolution  
2. Davis–Putnam (DP)  
3. DPLL (Davis–Putnam–Logemann–Loveland)  
4. CDCL (Conflict-Driven Clause Learning)

The goal is to generate feasible nurse schedules that satisfy various constraints—like shift coverage and rest requirements by encoding the scheduling problem as a Boolean satisfiability (SAT) problem.

---

## What Each Script Does

- **sat_solvers.py**  
  Contains the full logic of four SAT solving algorithms (Resolution, DP, DPLL, CDCL). Each function takes a CNF formula and returns `True` (SAT) or `False` (UNSAT).

- **generate_nurse_cnf.py**  
  Builds a nurse scheduling instance by defining constraints like:
  - Minimum nurses per shift
  - Maximum shifts per week
  - Forbidden shift patterns (e.g., night → morning)  
  Outputs a JSON CNF formula.

- **dump_dimacs.py**  
  Converts a JSON CNF formula into **DIMACS format**, a standard text format used by most SAT solvers.

- **run_all.py**  
  Loads a CNF file and runs all four solvers (Resolution, DP, DPLL, CDCL), printing whether the problem is SAT or UNSAT.

- **benchmark.py**  
  Extends `run_all.py` by also measuring:
  - Execution time  
  - Peak memory usage  
  - Timeout for slow solvers

---

## Requirements

Install dependencies (only one is used):

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:
```
psutil
```

---

## How to Run

Make sure you have **Python 3.9+** installed.

```bash

git clone https://github.com/raniaxibrahim77/SAT-nurse-scheduling.git
cd SAT-nurse-scheduling

1. **Create a virtual environment**  
   ```bash
   python -m venv venv          # Windows  
   python3 -m venv venv         # macOS / Linux / iOS
   ```

2. **Activate the virtual environment**  
   ```bash
   .\venv\Scripts\activate      # Windows  
   source venv/bin/activate     # macOS / Linux / iOS
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate a nurse scheduling instance**  
   ```bash
   py generate_nurse_cnf.py > data/nurse7x3.json      # Windows  
   python3 generate_nurse_cnf.py > data/nurse7x3.json # macOS / Linux / iOS
   ```

5. **Run all solvers**  
   ```bash
   py run_all.py data/nurse7x3.json      # Windows  
   python3 run_all.py data/nurse7x3.json # macOS / Linux / iOS
   ```

6. **Benchmark time and memory usage**  
   ```bash
   py benchmark.py data/nurse7x3.json      # Windows  
   python3 benchmark.py data/nurse7x3.json # macOS / Linux / iOS
   ```

> 📝 Optional: Export the instance to DIMACS format  
```bash
py dump_dimacs.py data/nurse7x3.json data/nurse7x3.cnf      # Windows  
python3 dump_dimacs.py data/nurse7x3.json data/nurse7x3.cnf # macOS / Linux / iOS
```

