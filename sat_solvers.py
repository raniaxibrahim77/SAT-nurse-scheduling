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
    cnf = [set(c) for c in cnf]
    assignment = set()
    while True:
        units = [c for c in cnf if len(c) == 1]
        if not units:
            break
        lit = next(iter(units[0]))
        assignment.add(lit)
        new_cnf = []
        for c in cnf:
            if lit in c:
                continue
            if -lit in c:
                r = c - {-lit}
                if not r:
                    return False
                new_cnf.append(r)
            else:
                new_cnf.append(c)
        cnf = new_cnf
    lits = set().union(*cnf) if cnf else set()
    for lit in [l for l in lits if -l not in lits]:
        assignment.add(lit)
        cnf = [c for c in cnf if lit not in c]
    if not cnf:
        return True
    if any(len(c) == 0 for c in cnf):
        return False
    var = abs(next(iter(next(iter(cnf)))))
    if dpll_sat([list(c) for c in cnf if var not in c] +
                [list(c - {-var}) for c in cnf if -var in c]):
        return True
    return dpll_sat([list(c) for c in cnf if -var not in c] +
                    [list(c - {var}) for c in cnf if var in c])

def cdcl_sat(cnf):
    base = [set(c) for c in cnf]
    learned = []
    def solve(clauses):
        assignment = []
        while True:
            units = [c for c in clauses if len(c) == 1]
            if not units:
                break
            lit = next(iter(units[0]))
            assignment.append(lit)
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
            sat, conflict = solve([c for c in clauses if lit not in c] +
                                  [c - {-lit} for c in clauses if -lit in c])
            if sat:
                return True, None
            if conflict is not None:
                return False, conflict
        return False, None
    while True:
        sat, conflict = solve(base + learned)
        if sat:
            return True
        if conflict is None:
            return False
        learned.append(conflict)