"""Numerical differentiation & integration: deterministic and Monte Carlo, 1D and n-D."""
import itertools
import numpy as np


# ---------- 1. Single-variable: deterministic ----------
def derivative(f, x, h=1e-5):
    """Central difference, error O(h^2)."""
    return (f(x + h) - f(x - h)) / (2 * h)


def integrate_simpson(f, a, b, n=1000):
    """Composite Simpson's rule (n is forced to be even)."""
    n += n % 2
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3 * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


def integrate_trapezoid(f, a, b, n=1000):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (b - a) / n * (y.sum() - 0.5 * (y[0] + y[-1]))


# ---------- 2. Single-variable: Monte Carlo ----------
def mc_integrate_1d(f, a, b, n=100_000, seed=None):
    """Returns (estimate, standard_error)."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(a, b, n)
    y = f(x) * (b - a)
    return y.mean(), y.std(ddof=1) / np.sqrt(n)


# ---------- 3. n-D: deterministic ----------
def gradient(f, x, h=1e-5):
    """Gradient of f: R^n -> R at point x via central differences."""
    x = np.asarray(x, dtype=float)
    g = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def integrate_nd_grid(f, lower, upper, m=20):
    """Midpoint rule on a tensor grid with m points per axis (m^n evaluations)."""
    lower, upper = np.asarray(lower, float), np.asarray(upper, float)
    h = (upper - lower) / m
    axes = [lower[i] + h[i] * (np.arange(m) + 0.5) for i in range(len(lower))]
    total = sum(f(np.array(p)) for p in itertools.product(*axes))
    return total * np.prod(h)


# ---------- 4. n-D: Monte Carlo ----------
def mc_integrate_nd(f, lower, upper, n=200_000, seed=None):
    """f takes an (N, d) array and returns an (N,) array. Returns (estimate, std_error)."""
    rng = np.random.default_rng(seed)
    lower, upper = np.asarray(lower, float), np.asarray(upper, float)
    pts = rng.uniform(lower, upper, size=(n, lower.size))
    vol = np.prod(upper - lower)
    y = f(pts) * vol
    return y.mean(), y.std(ddof=1) / np.sqrt(n)

# ---------- 5. Riemann sum ----------
def integral(f, low, high, m=20, max_evals=5e7):
    """Midpoint Riemann sum on an m^n grid over the box [low, high].

    Needs m**n evaluations, so it refuses when that is too large.
    """
    low = np.asarray(low, float)
    high = np.asarray(high, float)
    n = low.size
    if float(m) ** n > max_evals:
        raise ValueError(f"grid needs {m}^{n} evaluations: infeasible")
    h = (high - low) / m
    axes = [low[i] + h[i] * (np.arange(m) + 0.5) for i in range(n)]

    if n == 1:
        total = f(axes[0].reshape(-1, 1)).sum()
    else:
        # loop over the first axis, vectorize over the other n-1 axes (saves memory)
        rest = np.stack([g.ravel() for g in np.meshgrid(*axes[1:], indexing="ij")], axis=1)
        total = 0.0
        for x0 in axes[0]:
            pts = np.hstack([np.full((rest.shape[0], 1), x0), rest])
            total += f(pts).sum()
    return total * np.prod(h)


# ---------- 6. Monte Carlo ----------
def integral_mc(f, low, high, n_samples=1_000_000, chunk=100_000, seed=0):
    """Monte Carlo integral over the box [low, high]. Returns (estimate, std_error)."""
    rng = np.random.default_rng(seed)
    low = np.asarray(low, float)
    high = np.asarray(high, float)
    vol = np.prod(high - low)
    s = s2 = 0.0
    done = 0
    while done < n_samples:
        k = min(chunk, n_samples - done)
        y = f(rng.uniform(low, high, size=(k, low.size))) * vol
        s += y.sum()
        s2 += (y ** 2).sum()
        done += k
    mean = s / n_samples
    var = (s2 - n_samples * mean ** 2) / (n_samples - 1)
    return mean, np.sqrt(var / n_samples)

if __name__ == "__main__":
    # 1D: f = sin(x), f'(1) = cos(1), integral over [0, pi] = 2
    print("== 1D ==")
    print("[1] derivative :", derivative(np.sin, 1.0), "| exact", np.cos(1.0))
    print("[1] Simpson    :", integrate_simpson(np.sin, 0, np.pi), "| exact 2")
    print("[1] Trapezoid  :", integrate_trapezoid(np.sin, 0, np.pi))
    print("[2] Monte Carlo:", mc_integrate_1d(np.sin, 0, np.pi, seed=0))

    # n-D: f = sum(x_i^2) on [0,1]^n, grad = 2x, integral = n/3
    n = 3
    f_point = lambda x: np.sum(x ** 2)               # single point
    f_batch = lambda X: np.sum(X ** 2, axis=1)       # many points
    lo, hi = np.zeros(n), np.ones(n)
    p = np.array([0.5, 1.0, 2.0])
    print(f"\n== {n}-D ==")
    print("[3] gradient   :", gradient(f_point, p), "| exact", 2 * p)
    print("[3] grid integ :", integrate_nd_grid(f_point, lo, hi, m=20), "| exact", n / 3)
    print("[4] Monte Carlo:", mc_integrate_nd(f_batch, lo, hi, seed=0))

    # High dimension: grid is infeasible (20^10 points), MC is easy
    n = 10
    print(f"\n== {n}-D Monte Carlo ==")
    print("[4]", mc_integrate_nd(f_batch, np.zeros(n), np.ones(n), seed=0), "| exact", n / 3)

    f = lambda X: np.sum(X ** 2, axis=1)           # x1^2 + ... + xn^2
    grid_m = {1: 1000, 2: 1000, 5: 20, 100: 2}     # points per axis for Riemann
    print("\n=== 5. Riemann sum (f = sum x_i^2, [0,1]^n, exact = n/3) ===")
    for n in (1, 2, 5, 100):
        low, high = np.zeros(n), np.ones(n)
        try:
            est = integral(f, low, high, m=grid_m[n])
            print(f"n={n:>3}  Riemann = {est:.6f}  exact = {n/3:.6f}")
        except ValueError as e:
            print(f"n={n:>3}  Riemann failed: {e}")

    print("\n=== 6. Monte Carlo (N = 1,000,000) ===")
    for n in (1, 2, 5, 100):
        low, high = np.zeros(n), np.ones(n)
        est, se = integral_mc(f, low, high)
        print(f"n={n:>3}  MC = {est:.6f} +/- {se:.6f}  exact = {n/3:.6f}")