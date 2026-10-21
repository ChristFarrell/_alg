import random, time
from collections import Counter

MATCH, MISMATCH, GAP = 2, -1, -2
random.seed(1)
rand_dna = lambda L: "".join(random.choice("ACGT") for _ in range(L))


# =====================================================================
#  1. DYNAMIC PROGRAMMING: Smith-Waterman (prints its processing)
# =====================================================================
def smith_waterman(a, b, match=MATCH, mismatch=MISMATCH, gap=GAP, show_table=False):
    n, m = len(a), len(b)
    print(f"[DP] Table size = {n} x {m} = {n*m:,} cells (ALL of them will be computed)")
    H = [[0] * (m + 1) for _ in range(n + 1)]
    best, bi, bj = 0, 0, 0
    improvements = []

    # ---- Step 1: fill the table ----
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = match if a[i - 1] == b[j - 1] else mismatch
            H[i][j] = max(0,
                          H[i - 1][j - 1] + s,
                          H[i - 1][j] + gap,
                          H[i][j - 1] + gap)
            if H[i][j] > best:
                best, bi, bj = H[i][j], i, j
                improvements.append((i, j, best))
        if n <= 30 or i % 10 == 0 or i == n:
            print(f"[DP] row {i:>3}/{n} done   best score so far = {best} at cell ({bi},{bj})")

    print(f"[DP] New-best events during filling: {len(improvements)} "
          f"(last 5: {improvements[-5:]})")

    if show_table:                                   # only sensible for small inputs
        print("\n[DP] Score table H:")
        print("      " + "".join(f"{c:>4}" for c in " " + b))
        for i in range(n + 1):
            lab = " " if i == 0 else a[i - 1]
            print(f"  {lab} " + "".join(f"{v:>4}" for v in H[i]))

    # ---- Step 2: traceback ----
    print(f"\n[DP] Traceback from best cell ({bi},{bj}), H={best}, until H = 0:")
    i, j = bi, bj
    ra, rb, mid = [], [], []
    while i > 0 and j > 0 and H[i][j] > 0:
        s = match if a[i - 1] == b[j - 1] else mismatch
        if H[i][j] == H[i - 1][j - 1] + s:
            kind = "match   " if s > 0 else "MISMATCH"
            print(f"   ({i:>2},{j:>5}) {kind} {a[i-1]}/{b[j-1]}  H={H[i][j]}")
            ra.append(a[i - 1]); rb.append(b[j - 1]); mid.append("|" if s > 0 else "x")
            i -= 1; j -= 1
        elif H[i][j] == H[i - 1][j] + gap:
            print(f"   ({i:>2},{j:>5}) GAP in d  {a[i-1]}/-  H={H[i][j]}")
            ra.append(a[i - 1]); rb.append("-"); mid.append(" "); i -= 1
        else:
            print(f"   ({i:>2},{j:>5}) GAP in q  -/{b[j-1]}  H={H[i][j]}")
            ra.append("-"); rb.append(b[j - 1]); mid.append(" "); j -= 1

    ra, rb, mid = "".join(reversed(ra)), "".join(reversed(rb)), "".join(reversed(mid))
    print(f"\n[DP] Alignment (query starts at q[{i}], database starts at d[{j}]):")
    print("   q:", ra); print("      ", mid); print("   d:", rb)
    return best, ra, rb, i, j


# =====================================================================
#  2. NON-DP: Seed-and-extend (prints its processing)
# =====================================================================
def build_index(db, k):
    idx = {}
    for i in range(len(db) - k + 1):
        idx.setdefault(db[i:i + k], []).append(i)
    return idx


def _extend(q, d, i, j, step, match, mismatch, xdrop, verbose=False):
    """Extend in one direction. Returns (best extra score, its length, steps taken)."""
    cur = best = best_len = length = 0
    while 0 <= i < len(q) and 0 <= j < len(d):
        c = match if q[i] == d[j] else mismatch
        cur += c
        length += 1
        if cur > best:
            best, best_len = cur, length
            note = "new best"
        elif best - cur > xdrop:
            if verbose:
                print(f"        q[{i}]={q[i]} d[{j}]={d[j]} {c:+d}  cur={cur} best={best}"
                      f"  drop {best-cur} > xdrop {xdrop} -> STOP")
            break
        else:
            note = ""
        if verbose:
            print(f"        q[{i}]={q[i]} d[{j}]={d[j]} {c:+d}  cur={cur} best={best} {note}")
        i += step
        j += step
    return best, best_len, length


def seed_extend(q, d, k=5, match=MATCH, mismatch=MISMATCH, xdrop=5, detail_diag=None):
    # ---- Step 1: index ----
    t = time.time()
    idx = build_index(d, k)
    print(f"[SE] Step 1 - index: {len(d)-k+1:,} k-mers -> {len(idx)} distinct {k}-mers "
          f"({time.time()-t:.4f}s)")

    # ---- Step 2: seeds ----
    n_q = len(q) - k + 1
    best = (0, 0, 0, 0)
    hits, steps = [], 0
    for qi in range(n_q):
        for di in idx.get(q[qi:qi + k], []):
            rs, rl, s1 = _extend(q, d, qi + k, di + k, +1, match, mismatch, xdrop)
            ls, ll, s2 = _extend(q, d, qi - 1, di - 1, -1, match, mismatch, xdrop)
            score = k * match + rs + ls
            steps += s1 + s2
            hits.append((qi, di, di - qi, score))
            if score > best[0]:
                best = (score, qi - ll, di - ll, k + ll + rl)
    print(f"[SE] Step 2 - seeds: looked up {n_q} query {k}-mers -> {len(hits):,} seed hits")

    # ---- Step 3: group hits by diagonal (d - q) ----
    diag = Counter(h[2] for h in hits)
    print("[SE] Step 3 - hits per diagonal (d-q). A real alignment = many seeds on ONE diagonal:")
    for dg, cnt in diag.most_common(5):
        top = max(h[3] for h in hits if h[2] == dg)
        print(f"        diagonal {dg:>6}: {cnt:>3} seeds, best extended score = {top}")
    one = sum(1 for c in diag.values() if c == 1)
    print(f"        ({one} other diagonals have just 1 hit = random noise)")

    # ---- Step 4: show extension step by step for one real seed ----
    if detail_diag is None:
        detail_diag = diag.most_common(1)[0][0]
    qi, di, _, _ = next(h for h in hits if h[2] == detail_diag)
    print(f"\n[SE] Step 4 - extension in detail for seed q[{qi}] <-> d[{di}] (diagonal {detail_diag}):")
    print("      extend right:")
    rs, _, _ = _extend(q, d, qi + k, di + k, +1, match, mismatch, xdrop, verbose=True)
    print("      extend left:")
    ls, _, _ = _extend(q, d, qi - 1, di - 1, -1, match, mismatch, xdrop, verbose=True)
    print(f"      total = seed {k*match} + right {rs} + left {ls} = {k*match+rs+ls}")

    noise = [h for h in hits if h[2] != detail_diag]
    if noise:
        print(f"\n[SE] Noise check: {len(noise):,} hits off the true diagonal, "
              f"best noise score = {max(h[3] for h in noise)}  (they die quickly by X-drop)")
    print(f"[SE] Total extension steps = {steps:,}   (compare with DP cells)")
    return best


# =====================================================================
#  PART A: small example (full table visible)
# =====================================================================
print("=" * 72); print("PART A - small example"); print("=" * 72)
ds = "TTGACCGATCGGATTACAGCTA"
qs = "GATCGGATAACAG"
print("database d =", ds); print("query    q =", qs, "\n")
smith_waterman(qs, ds, show_table=True)
print()
seed_extend(qs, ds, k=4, xdrop=3)

# =====================================================================
#  PART B: your original program (20,000 bases) + processing
# =====================================================================
print("\n" + "=" * 72); print("PART B - original program: 20,000-base database"); print("=" * 72)
d = rand_dna(20000)
q = list(d[12000:12060])
for p in (10, 30, 50):
    q[p] = "A" if q[p] != "A" else "C"
q = "".join(q)
print(f"query = d[12000:12060] with 3 mutations at q[10], q[30], q[50]\n")

print("-" * 30, "DP", "-" * 30)
t = time.time(); sw = smith_waterman(q, d); t_sw = time.time() - t

print("\n" + "-" * 24, "Seed-and-extend", "-" * 24)
t = time.time(); se = seed_extend(q, d); t_se = time.time() - t

print("\n" + "=" * 72); print("FINAL RESULT"); print("=" * 72)
print(f"Smith-Waterman : score={sw[0]}  position in d={sw[4]}  time={t_sw:.3f}s")
print(f"Seed-extend    : score={se[0]}  position in d={se[2]}  time={t_se:.4f}s")
print(f"Speedup        : {t_sw / t_se:.0f}x")