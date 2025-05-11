def resolution_sat(cnf):
    clauses = set(frozenset(c) for c in cnf)
    new = set()
    while True:
        pairs = [(ci, cj) for ci in clauses for cj in clauses if ci < cj]
        for ci, cj in pairs:
            for lit in ci:
                if -lit in cj:
                    resolvent = (ci - {lit}) | (cj - {-lit})
                    if not resolvent:
                        return False
                    new.add(frozenset(resolvent))
        if new.issubset(clauses):
            return True
        clauses |= new

def dp_sat(cnf):
    def eliminate(formula):
        if any(len(c) == 0 for c in formula):
            return False
        if not formula:
            return True
        formula = list(formula)
        var = abs(next(iter(next(iter(formula)))))
        pos = [c for c in formula if var in c]
        neg = [c for c in formula if -var in c]
        others = [c for c in formula if var not in c and -var not in c]
        resolvents = []
        for ci in pos:
            for cj in neg:
                resolvents.append((ci - {var}) | (cj - {-var}))
        return eliminate(others + resolvents)
    return eliminate([set(c) for c in cnf])

def dpll_sat(cnf):
    def dpll(clauses, assignment):
        while True:
            units = [c for c in clauses if len(c) == 1]
            if not units:
                break
            lit = next(iter(units[0]))
            assignment.add(lit)
            new_cnf = []
            for c in clauses:
                if lit in c:
                    continue
                if -lit in c:
                    r = c - {-lit}
                    if not r:
                        return False
                    new_cnf.append(r)
                else:
                    new_cnf.append(c)
            clauses = new_cnf
        if not clauses:
            return True
        if any(len(c) == 0 for c in clauses):
            return False
        var = abs(next(iter(next(iter(clauses)))))
        for val in [var, -var]:
            new_assignment = assignment.copy()
            new_assignment.add(val)
            new_cnf = []
            for c in clauses:
                if val in c:
                    continue
                if -val in c:
                    r = c - {-val}
                    if not r:
                        break
                    new_cnf.append(r)
                else:
                    new_cnf.append(c)
            else:
                if dpll(new_cnf, new_assignment):
                    assignment.clear()
                    assignment.update(new_assignment)
                    return True
        return False

    clauses = [set(c) for c in cnf]
    assignment = set()
    sat = dpll(clauses, assignment)
    if sat:
        return True, sorted(assignment)
    else:
        return False, None

def cdcl_sat(cnf):
    base = [set(c) for c in cnf]
    learned = []
    model = set()

    def solve(clauses, assignment):
        while True:
            units = [c for c in clauses if len(c) == 1]
            if not units:
                break
            lit = next(iter(units[0]))
            assignment.add(lit)
            new = []
            for c in clauses:
                if lit in c:
                    continue
                if -lit in c:
                    r = c - {-lit}
                    if not r:
                        return False, c
                    new.append(r)
                else:
                    new.append(c)
            clauses = new
        if not clauses:
            return True, None
        if any(len(c) == 0 for c in clauses):
            return False, next(c for c in clauses if len(c) == 0)
        var = abs(next(iter(next(iter(clauses)))))
        for lit in (var, -var):
            new_assignment = assignment.copy()
            new_assignment.add(lit)
            new_clauses = []
            for c in clauses:
                if lit in c:
                    continue
                if -lit in c:
                    r = c - {-lit}
                    if not r:
                        break
                    new_clauses.append(r)
                else:
                    new_clauses.append(c)
            else:
                sat, conflict = solve(new_clauses, new_assignment)
                if sat:
                    assignment.clear()
                    assignment.update(new_assignment)
                    return True, None
        return False, None

    while True:
        assignment = set()
        sat, conflict = solve(base + learned, assignment)
        if sat:
            return True, sorted(assignment)
        if conflict is None:
            return False, None
        learned.append(conflict)
