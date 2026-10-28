"""
TSP solvers that SHOW THEIR SEARCH PROCESS step by step.

Algorithms: Nearest Neighbor, 2-opt, Hill Climbing, Simulated Annealing,
            Gradient Descent (Sinkhorn relaxation).

Every algorithm is a generator that yields one "event" per decision
(dict: step, kind, msg, tour, length, best). The runner prints those events,
so you can see WHY the tour changes, not only the final result.

Usage:
    python tsp_algorithms.py                         # all algorithms, 12 cities
    python tsp_algorithms.py --algo 2opt --n 15
    python tsp_algorithms.py --algo sa --every 25 --detail 15
    python tsp_algorithms.py --algo all --plot       # convergence + final tours
    python tsp_algorithms.py --algo hc --animate     # live drawing of the tour
Requires: numpy (matplotlib only for --plot / --animate)
"""
import argparse
import math
import random
import numpy as np


# ---------------------------------------------------------------- helpers
def dist_matrix(pts):
    p = np.asarray(pts, dtype=float)
    return np.sqrt(((p[:, None, :] - p[None, :, :]) ** 2).sum(-1))


def tour_length(t, D):
    return float(sum(D[t[i], t[(i + 1) % len(t)]] for i in range(len(t))))


def path_length(t, D):  # open path (used while a tour is still being built)
    return float(sum(D[t[i], t[i + 1]] for i in range(len(t) - 1)))


def ev(step, kind, msg, tour, length, best=None):
    return dict(step=step, kind=kind, msg=msg, tour=list(tour),
                length=length, best=length if best is None else best)


def fmt(t):
    return "-".join(map(str, t))


# ------------------------------------------------- 1. Greedy: Nearest Neighbor
def nearest_neighbor(D, start=0):
    n = len(D)
    tour, left, step = [start], set(range(n)) - {start}, 0
    yield ev(0, "start", f"Start at city {start}. Rule: always go to the closest unvisited city.",
             tour, 0.0)
    while left:
        cur = tour[-1]
        cands = sorted(left, key=lambda j: D[cur, j])
        shown = ", ".join(f"{j}(d={D[cur, j]:.3f})" for j in cands[:3])
        nxt = cands[0]
        tour.append(nxt)
        left.remove(nxt)
        step += 1
        yield ev(step, "move",
                 f"At city {cur}. Closest unvisited: {shown}{' ...' if len(cands) > 3 else ''} "
                 f"-> go to {nxt}. Path length so far {path_length(tour, D):.3f}",
                 tour, path_length(tour, D))
    L = tour_length(tour, D)
    yield ev(step + 1, "end",
             f"All cities visited. Close the loop {tour[-1]} -> {start} "
             f"(+{D[tour[-1], start]:.3f}). Final length {L:.3f}", tour, L)


# ------------------------------------------------- 2. Improvement: 2-opt
def two_opt(D, tour=None):
    n = len(D)
    t = tour[:] if tour else random.sample(range(n), n)
    L, step, sweep = tour_length(t, D), 0, 0
    yield ev(0, "start", f"Random start tour {fmt(t)}  length {L:.3f}", t, L)
    improved = True
    while improved:
        improved, sweep, rejected = False, sweep + 1, 0
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                a, b, c, d = t[i], t[i + 1], t[j], t[(j + 1) % n]
                delta = (D[a, c] + D[b, d]) - (D[a, b] + D[c, d])
                if delta < -1e-12:
                    t[i + 1:j + 1] = t[i + 1:j + 1][::-1]
                    L += delta
                    step += 1
                    improved = True
                    yield ev(step, "accept",
                             f"Sweep {sweep}: swap edges ({a},{b})+({c},{d}) -> ({a},{c})+({b},{d}), "
                             f"delta={delta:+.3f} (after {rejected} rejected tries). Length {L:.3f}",
                             t, L)
                    rejected = 0
                else:
                    rejected += 1
        yield ev(step, "info", f"End of sweep {sweep}: "
                 f"{'found improvements, scan again' if improved else 'no improving move'}", t, L)
    yield ev(step + 1, "end", f"Local optimum for 2-opt. Final length {L:.3f}", t, L)


# ------------------------------------------------- 3. Hill climbing (swap neighbours)
def hill_climbing(D, tour=None):
    n = len(D)
    t = tour[:] if tour else random.sample(range(n), n)
    cur, step = tour_length(t, D), 0
    yield ev(0, "start", f"Random start tour {fmt(t)}  length {cur:.3f}", t, cur)
    while True:
        step += 1
        best, best_len, better, total = None, cur, 0, 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                t[i], t[j] = t[j], t[i]
                L = tour_length(t, D)
                t[i], t[j] = t[j], t[i]
                total += 1
                if L < cur - 1e-12:
                    better += 1
                    if L < best_len:
                        best, best_len = (i, j), L
        if best is None:
            yield ev(step, "end", f"Checked all {total} neighbours: none is better "
                     f"-> stuck on a peak (local optimum). Final length {cur:.3f}", t, cur)
            return
        i, j = best
        ci, cj = t[i], t[j]
        t[i], t[j] = t[j], t[i]
        yield ev(step, "accept",
                 f"Iter {step}: {total} neighbours checked, {better} better. Best = swap cities "
                 f"{ci}<->{cj} (positions {i},{j}): {cur:.3f} -> {best_len:.3f}", t, best_len)
        cur = best_len


# ------------------------------------------------- 4. Simulated annealing
def simulated_annealing(D, T0=None, alpha=0.995, T_min=1e-3, iters_per_T=100):
    n = len(D)
    t = random.sample(range(n), n)
    cur = tour_length(t, D)
    best, best_len = t[:], cur
    T = T0 or cur * 0.1
    step = stage = 0
    yield ev(0, "start", f"Random start length {cur:.3f}. Start temperature T={T:.4f}, "
             f"cooling x{alpha} per stage, {iters_per_T} proposals per stage.", t, cur)
    while T > T_min:
        stage += 1
        cnt = dict(improve=0, worse_ok=0, reject=0)
        for _ in range(iters_per_T):
            step += 1
            i, j = sorted(random.sample(range(n), 2))
            cand = t[:i] + t[i:j + 1][::-1] + t[j + 1:]        # 2-opt move
            L = tour_length(cand, D)
            delta = L - cur
            if delta < 0:
                d, cnt["improve"] = f"better ({delta:+.3f}) -> ACCEPT", cnt["improve"] + 1
                t, cur = cand, L
            else:
                p = math.exp(-delta / T)
                r = random.random()
                if r < p:
                    d = f"worse ({delta:+.3f}), p=exp(-d/T)={p:.3f} > rand {r:.3f} -> ACCEPT anyway"
                    cnt["worse_ok"] += 1
                    t, cur = cand, L
                else:
                    d = f"worse ({delta:+.3f}), p={p:.3f} < rand {r:.3f} -> reject"
                    cnt["reject"] += 1
            if cur < best_len:
                best, best_len = t[:], cur
            yield ev(step, "iter", f"T={T:.4f} reverse segment [{i}..{j}]: {d}. "
                     f"Current {cur:.3f}, best {best_len:.3f}", t, cur, best_len)
        yield ev(stage, "stage",
                 f"Stage {stage}: T={T:.4f}  improved {cnt['improve']}, accepted-worse "
                 f"{cnt['worse_ok']}, rejected {cnt['reject']}  | current {cur:.3f}  best {best_len:.3f}",
                 t, cur, best_len)
        T *= alpha
    yield ev(step + 1, "end", f"Frozen (T<{T_min}). Best tour found: length {best_len:.3f}",
             best, best_len)


# ------------------------------------------------- 5. Gradient descent (relaxed permutation)
def sinkhorn(logits, iters=30):
    """Log-domain Sinkhorn: logits -> doubly-stochastic matrix."""
    L = logits.copy()
    for _ in range(iters):
        L -= np.logaddexp.reduce(L, axis=1, keepdims=True)
        L -= np.logaddexp.reduce(L, axis=0, keepdims=True)
    return np.exp(L)


def round_to_tour(P):
    """Projection: take highest-probability (city, position) pairs first."""
    n = len(P)
    order = np.dstack(np.unravel_index(np.argsort(-P, axis=None), P.shape))[0]
    pos, uc, up = [None] * n, set(), set()
    for c, p in order:
        if c not in uc and p not in up:
            pos[p] = int(c)
            uc.add(c)
            up.add(p)
    return pos


def gradient_descent(D, steps=600, lr=0.5, tau=0.3, seed=0):
    """P[i,k] ~ "city i is visited at position k" (doubly-stochastic).
    Loss = expected tour length = sum_ik P_ik * sum_j D_ij * (P_j,k+1).
    dLoss/dP is applied to the logits (straight-through approximation)."""
    rng = np.random.default_rng(seed)
    n = len(D)
    theta = rng.normal(0, 0.1, (n, n))
    scale = D.mean()
    best_t, best_len = None, float("inf")
    yield ev(0, "start", f"Random logits -> P is ~uniform (every city equally likely at every "
             f"position). lr={lr}, tau={tau}", list(range(n)), tour_length(list(range(n)), D))
    for s in range(1, steps + 1):
        P = sinkhorn(theta / tau)
        grad = D @ (np.roll(P, -1, 1) + np.roll(P, 1, 1))
        theta -= lr * grad / scale
        t = round_to_tour(P)
        L = tour_length(t, D)
        if L < best_len:
            best_t, best_len = t, L
        exp_loss = float(np.sum(P * (D @ np.roll(P, -1, 1))))
        yield ev(s, "stage",
                 f"Step {s}: expected length {exp_loss:.3f}, |grad|={np.linalg.norm(grad):.3f}, "
                 f"confidence(mean max P)={P.max(1).mean():.2f}, rounded tour {L:.3f}, best {best_len:.3f}",
                 t, L, best_len)
    yield ev(steps + 1, "end", f"Projected back to a valid permutation. Best rounded tour "
             f"length {best_len:.3f}", best_t, best_len)


ALGOS = {
    "nn": ("Nearest Neighbor (Greedy)", nearest_neighbor),
    "2opt": ("2-opt (Improvement)", two_opt),
    "hc": ("Hill Climbing", hill_climbing),
    "sa": ("Simulated Annealing", simulated_annealing),
    "gd": ("Gradient Descent", gradient_descent),
}


# ---------------------------------------------------------------- runner
def draw(ax, pts, tour, title, closed=True):
    ax.clear()
    ax.scatter(*zip(*pts), c="k", zorder=3)
    for i, p in enumerate(pts):
        ax.annotate(str(i), p, textcoords="offset points", xytext=(4, 4), fontsize=8)
    t = tour + [tour[0]] if closed and len(tour) == len(pts) else tour
    ax.plot([pts[i][0] for i in t], [pts[i][1] for i in t], "-", color="teal")
    ax.set_title(title, fontsize=9)


def run(key, pts, D, args, ax=None):
    name, fn = ALGOS[key]
    print(f"\n{'=' * 78}\n{name}\n{'=' * 78}")
    hist, last = [], None
    for e in fn(D):
        last = e
        hist.append(e["best"])
        show = (e["kind"] in ("start", "move", "accept", "end", "info")
                or (e["kind"] == "iter" and e["step"] <= args.detail)
                or (e["kind"] == "stage" and (e["step"] % args.every == 0 or e["step"] <= 1)))
        if show:
            print(f"[{e['step']:>6}] {e['msg']}")
            if ax is not None:
                import matplotlib.pyplot as plt
                draw(ax, pts, e["tour"], f"{name} - step {e['step']}  len={e['length']:.3f}")
                plt.pause(args.delay)
    assert sorted(last["tour"]) == list(range(len(pts))), "invalid tour"
    return last["tour"], tour_length(last["tour"], D), hist


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=12, help="number of cities")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--algo", choices=list(ALGOS) + ["all"], default="all")
    ap.add_argument("--every", type=int, default=50, help="print every N-th stage (SA/GD)")
    ap.add_argument("--detail", type=int, default=10, help="SA: print first N individual proposals")
    ap.add_argument("--plot", action="store_true", help="final tours + convergence curves")
    ap.add_argument("--animate", action="store_true", help="live drawing of each printed step")
    ap.add_argument("--delay", type=float, default=0.15)
    a = ap.parse_args()

    random.seed(a.seed)
    np.random.seed(a.seed)
    pts = [(random.random(), random.random()) for _ in range(a.n)]
    D = dist_matrix(pts)
    print("Cities:", ", ".join(f"{i}=({x:.2f},{y:.2f})" for i, (x, y) in enumerate(pts)))

    ax = None
    if a.animate:
        import matplotlib.pyplot as plt
        plt.ion()
        _, ax = plt.subplots(figsize=(5, 5))

    results = {}
    for key in (ALGOS if a.algo == "all" else [a.algo]):
        results[key] = run(key, pts, D, a, ax)

    print(f"\n{'=' * 78}\nSUMMARY (shorter is better)\n{'=' * 78}")
    for key, (t, L, h) in sorted(results.items(), key=lambda kv: kv[1][1]):
        print(f"{ALGOS[key][0]:<28} length = {L:.4f}   tour = {fmt(t)}")

    if a.plot:
        import matplotlib.pyplot as plt
        k = len(results)
        fig, axs = plt.subplots(2, k, figsize=(4 * k, 7), squeeze=False)
        for c, (key, (t, L, h)) in enumerate(results.items()):
            draw(axs[0][c], pts, t, f"{ALGOS[key][0]}\nlength {L:.3f}")
            axs[1][c].plot(h)
            axs[1][c].set_xlabel("event #")
            axs[1][c].set_ylabel("best length so far")
        plt.tight_layout()
        plt.show()