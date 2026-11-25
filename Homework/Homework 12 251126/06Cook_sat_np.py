"""
07 - Cook, SAT, P vs NP and Reductions (Chapter 6)
==================================================
  P   : problems a deterministic machine SOLVES in polynomial time.
  NP  : problems whose answer can be CHECKED in polynomial time
        (equivalently, solved by a nondeterministic machine in poly time).
  Cook (1971): SAT is NP-complete - every NP problem reduces to SAT.
  So a fast SAT solver would give a fast solver for ALL of NP (P = NP).

Run:  python 07_cook_sat_np.py
"""

import time
from itertools import product


# --- 1. SAT: easy to CHECK, hard to SOLVE ------------------------------------
# A formula in CNF: list of clauses; a clause is a list of literals;
# literal +k means variable k, -k means NOT variable k.
def check(cnf, assignment):
    """Verify a certificate: polynomial time (one pass over the formula)."""
    return all(any(assignment[abs(l)] == (l > 0) for l in clause) for clause in cnf)


def brute_force_sat(cnf, n):
    """Try all 2^n assignments: exponential time."""
    for values in product([False, True], repeat=n):
        assignment = {i + 1: v for i, v in enumerate(values)}
        if check(cnf, assignment):
            return assignment
    return None


# --- 2. Reduction: n-queens  ->  SAT  ->  answer back ------------------------
# Same pattern as the notes:  ob = b(a2b(ia));  oa = b2a(ob)
def queens_to_sat(n):                                      # a2b
    var = lambda r, c: r * n + c + 1
    cnf = []
    for r in range(n):                                     # at least one queen per row
        cnf.append([var(r, c) for c in range(n)])
    cells = [(r, c) for r in range(n) for c in range(n)]
    for (r1, c1) in cells:                                 # no two queens attack
        for (r2, c2) in cells:
            if (r1, c1) < (r2, c2) and (r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2)):
                cnf.append([-var(r1, c1), -var(r2, c2)])
    return cnf, n * n


def dpll(cnf, assignment=None):
    """Small DPLL SAT solver (unit propagation + branching)."""
    assignment = dict(assignment or {})
    cnf = [list(c) for c in cnf]
    while True:                                            # unit propagation
        unit = next((c[0] for c in cnf if len(c) == 1), None)
        if unit is None:
            break
        assignment[abs(unit)] = unit > 0
        new = []
        for c in cnf:
            if unit in c:
                continue
            c = [l for l in c if l != -unit]
            if not c:
                return None                                # empty clause: conflict
            new.append(c)
        cnf = new
    if not cnf:
        return assignment
    lit = cnf[0][0]
    for choice in (lit, -lit):                             # branch
        reduced = [c for c in cnf if choice not in c]
        reduced = [[l for l in c if l != -choice] for c in reduced]
        if any(len(c) == 0 for c in reduced):
            continue
        result = dpll(reduced, {**assignment, abs(choice): choice > 0})
        if result is not None:
            return result
    return None


def sat_to_queens(assignment, n):                          # b2a
    rows = []
    for r in range(n):
        rows.append("".join("Q " if assignment.get(r * n + c + 1) else ". " for c in range(n)))
    return "\n".join("  " + row for row in rows)


# --- 3. Another NP problem: subset sum (certificate vs search) ---------------
def subset_sum_verify(numbers, target, chosen_idx):
    return sum(numbers[i] for i in chosen_idx) == target     # fast check

def subset_sum_search(numbers, target):
    n = len(numbers)
    for mask in range(1 << n):                               # 2^n subsets
        idx = [i for i in range(n) if mask >> i & 1]
        if subset_sum_verify(numbers, target, idx):
            return idx
    return None


# --- 4. Cook-Levin for real: turn a nondeterministic TM run into SAT --------
# delta: (state, symbol) -> list of (new_state, write, move)  -- several options = nondeterminism
BLANK = "_"

def ntm_accepts(delta, start, accept, tape, K, L):
    """Reference answer: explore ALL nondeterministic branches for K steps."""
    tape0 = tuple(list(tape) + [BLANK] * (L - len(tape)))
    frontier = {(start, 0, tape0)}
    for _ in range(K + 1):
        if any(q == accept for q, _, _ in frontier):
            return True
        nxt = set()
        for q, h, t in frontier:
            for q2, w, d in delta.get((q, t[h]), []):
                h2 = h + d
                if 0 <= h2 < L:
                    nxt.add((q2, h2, t[:h] + (w,) + t[h + 1:]))
        frontier = nxt
    return False


def cook_levin(delta, start, accept, tape, K, L):
    """Build a CNF that is satisfiable  <=>  the NTM accepts within K steps
    using tape cells 0..L-1.  Size is polynomial in K and L."""
    states = sorted({start, accept} | {q for q, _ in delta} | {o[0] for v in delta.values() for o in v})
    symbols = sorted({BLANK} | set(tape) | {a for _, a in delta} | {o[1] for v in delta.values() for o in v})
    ids, cnf = {}, []
    def var(*key):
        if key not in ids:
            ids[key] = len(ids) + 1
        return ids[key]
    T = lambda i, j, k: var("T", i, j, k)      # cell i holds symbol j at step k
    H = lambda i, k:    var("H", i, k)         # head at cell i at step k
    Q = lambda q, k:    var("Q", q, k)         # machine in state q at step k

    def exactly_one(lits):
        cnf.append(list(lits))
        for x in range(len(lits)):
            for y in range(x + 1, len(lits)):
                cnf.append([-lits[x], -lits[y]])

    padded = list(tape) + [BLANK] * (L - len(tape))
    for i in range(L):                                    # initial configuration
        cnf.append([T(i, padded[i], 0)])
    cnf.append([H(0, 0)]); cnf.append([Q(start, 0)])

    for k in range(K + 1):                                # one symbol/cell, one head, one state
        for i in range(L):
            exactly_one([T(i, j, k) for j in symbols])
        exactly_one([H(i, k) for i in range(L)])
        exactly_one([Q(q, k) for q in states])

    delta = {**delta, **{(accept, a): [(accept, a, 0)] for a in symbols}}   # accept = absorbing
    for k in range(K):
        for i in range(L):                                # cells away from the head never change
            for j in symbols:
                cnf.append([-T(i, j, k), H(i, k), T(i, j, k + 1)])
        for i in range(L):                                # legal transitions
            for q in states:
                for a in symbols:
                    options = [o for o in delta.get((q, a), []) if 0 <= i + o[2] < L]
                    guard = [-H(i, k), -Q(q, k), -T(i, a, k)]
                    choices = []
                    for n, (q2, w, d) in enumerate(options):
                        c = var("C", i, q, a, k, n)       # "option n is the one taken"
                        choices.append(c)
                        cnf += [[-c, Q(q2, k + 1)], [-c, T(i, w, k + 1)], [-c, H(i + d, k + 1)]]
                    cnf.append(guard + choices)           # a move must exist (else: dead end)
    cnf.append([Q(accept, K)])                            # must be accepting at the end
    return cnf, ids


def decode_run(assignment, ids, K, L):
    rows = []
    for k in range(K + 1):
        state = next(key[1] for key, v in ids.items() if key[0] == "Q" and key[2] == k and assignment.get(v))
        head = next(key[1] for key, v in ids.items() if key[0] == "H" and key[2] == k and assignment.get(v))
        cells = "".join(next(key[2] for key, v in ids.items() if key[0] == "T" and key[1] == i and key[3] == k and assignment.get(v))
                        for i in range(L))
        rows.append(f"    step {k}: state={state:3} head={head}  tape={cells}")
    return rows


# Nondeterministic machine: accepts strings over {0,1} that contain "11".
# At q0 it may keep scanning OR guess "the 11 starts here".
NTM = {
    ("q0", "0"): [("q0", "0", 1)],
    ("q0", "1"): [("q0", "1", 1), ("q1", "1", 1)],
    ("q1", "1"): [("qa", "1", 0)],
}


if __name__ == "__main__":
    print(__doc__)

    # Formula from the notes: (x or y) and (x or not z); x=1,y=2,z=3
    cnf = [[1, 2], [1, -3]]
    print("1. Checking vs solving: (x or y) and (x or not z)")
    for assign in [(0, 1, 1), (0, 1, 0)]:
        a = {i + 1: bool(v) for i, v in enumerate(assign)}
        print(f"  assignment {assign} -> {check(cnf, a)}   (instant to verify)")
    print("  brute-force solution:", brute_force_sat(cnf, 3))

    print("\n  Brute force time vs number of variables (hard formula, no solution):")
    times = {}
    for n in [10, 14, 18, 20]:
        hard = [[i] for i in range(1, n + 1)] + [[-n]]       # unsatisfiable: forces all 2^n tries
        # put the contradiction last so every assignment is rejected late
        t = time.perf_counter()
        brute_force_sat(hard, n)
        elapsed = time.perf_counter() - t
        times[n] = elapsed
        print(f"    n={n:2}  {elapsed:7.3f}s")
    rate = 2 ** 20 / times[20]                               # assignments checked per second
    years = 2 ** 1024 // int(rate) // (3600 * 24 * 365)   # integer math: the number is huge
    print(f"  measured speed: about {rate:,.0f} assignments/second")
    print(f"  growth per +1 variable (n=18 -> 20): x{(times[20] / times[18]) ** 0.5:.2f}")
    print(f"  1024 variables = 2^1024 (a {len(str(2 ** 1024))}-digit number) tries")
    print(f"  at this speed: about 10^{len(str(years)) - 1} years (the universe is ~1.4 x 10^10 years old)")

    print("\n2. Reduction: solve 6-queens by turning it into SAT")
    cnf, nvars = queens_to_sat(6)
    print(f"  6-queens became a SAT formula with {nvars} variables and {len(cnf)} clauses")
    solution = dpll(cnf)
    print(sat_to_queens(solution, 6))
    cells = [(r, c) for r in range(6) for c in range(6) if solution.get(r * 6 + c + 1)]
    ok = (len({r for r, _ in cells}) == 6 and len({c for _, c in cells}) == 6 and
          all(abs(r1 - r2) != abs(c1 - c2) for (r1, c1) in cells for (r2, c2) in cells if (r1, c1) < (r2, c2)))
    print("  independently verified (6 queens, no shared row/col/diagonal):", ok)
    assert ok
    print("  The solver knows nothing about chess - the reduction did the translation.")

    print("\n3. Subset sum: a certificate is checked instantly")
    nums, target = [3, 34, 4, 12, 5, 2], 9
    idx = subset_sum_search(nums, target)
    print(f"  numbers={nums} target={target} -> pick {[nums[i] for i in idx]}")
    print("  verify:", subset_sum_verify(nums, target, idx))

    print("\n4. Cook-Levin on a real nondeterministic machine (accepts strings containing '11')")
    K, L = 5, 5
    for word in ["0110", "1011", "1010", "0101"]:
        cnf, ids = cook_levin(NTM, "q0", "qa", word, K, L)
        model = dpll(cnf)
        sat = model is not None
        truth = ntm_accepts(NTM, "q0", "qa", word, K, L)
        print(f"  input {word}: formula has {len(ids)} vars, {len(cnf)} clauses -> "
              f"SAT={sat}   machine accepts={truth}   agree: {sat == truth}")
        assert sat == truth
        if sat and word == "0110":
            print("  accepting computation recovered from the satisfying assignment:")
            print("\n".join(decode_run(model, ids, K, L)))

    print("\n  Formula size as the computation grows (K steps, L cells), measured:")
    sizes = []
    for size in [4, 8, 16, 32]:
        cnf, ids = cook_levin(NTM, "q0", "qa", "0110", size, size)
        sizes.append(len(cnf))
        print(f"    K=L={size:2}: {len(ids):6} variables, {len(cnf):7} clauses")
    ratios = ", ".join(f"x{b / a:.1f}" for a, b in zip(sizes, sizes[1:]))
    print(f"  clause growth per doubling of K and L: {ratios}")
    print("  The factor drifts toward 8 (= 2^3): the size is cubic, dominated by the K*L^2")
    print("  pairwise 'at most one head position' clauses.  A polynomial has a fixed factor like")
    print("  this per doubling; an exponential formula would square its size instead.")

    print("""
What the code shows vs. what it cannot show
-------------------------------------------
Shown by running: the formula grows polynomially with K and L, and it is
satisfiable exactly when the machine accepts, so a SAT solver "runs" the
nondeterministic machine.  Cook's theorem is the claim that this works for
EVERY NP machine and input; that general proof is mathematics, not a program.
Whether SAT can be solved in polynomial time (P = NP) is still open.""")