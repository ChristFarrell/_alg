import math

_memo1 = {1: 1}


def T1_recursive(n):
    if n in _memo1:
        return _memo1[n]
    result = T1_recursive(n - 1) + 8
    _memo1[n] = result
    return result


def T1_formula(n):
    return 8 * n - 7

_memo2 = {1: 1}


def T2_recursive(n):
    if n in _memo2:
        return _memo2[n]
    result = 2 * T2_recursive(n - 1) + 9
    _memo2[n] = result
    return result


def T2_formula(n):
    return 10 * (2 ** (n - 1)) - 9

_memo3 = {1: 1}


def T3_recursive(n):
    if n in _memo3:
        return _memo3[n]
    result = 2 * T3_recursive(n // 2) + 1
    _memo3[n] = result
    return result


def T3_formula(n):
    return 2 * n - 1

_memo4 = {1: 1}


def T4_recursive(n):
    if n in _memo4:
        return _memo4[n]
    result = T4_recursive(n // 2) + 1
    _memo4[n] = result
    return result


def T4_formula(n):
    return 1 + math.log2(n)


# ---------------------------------------------------------------
# Verification / demonstration
# ---------------------------------------------------------------
def print_table(title, recursive_fn, formula_fn, n_values, big_o):
    print("=" * 70)
    print(f"{title}   (Big-O: {big_o})")
    print("=" * 70)
    print(f"{'n':>8} {'recursive T(n)':>18} {'formula T(n)':>18} {'match?':>8}")
    print("-" * 70)
    for n in n_values:
        r = recursive_fn(n)
        f = formula_fn(n)
        ok = abs(r - f) < 1e-9
        print(f"{n:>8} {r:>18} {round(f, 4) if isinstance(f, float) else f:>18} {'OK' if ok else 'MISMATCH':>8}")
    print()


def main():
    # #1: linear growth, safe to test with fairly large n
    print_table(
        "1. T(n) = T(n-1) + 8, T(1) = 1",
        T1_recursive, T1_formula,
        n_values=[1, 2, 4, 8, 16, 32, 64],
        big_o="O(n)",
    )

    # #2: exponential growth -> only test SMALL n, otherwise numbers
    # (and recursion) explode. This alone proves how fast it blows up.
    print_table(
        "2. T(n) = 2*T(n-1) + 9, T(1) = 1",
        T2_recursive, T2_formula,
        n_values=[1, 2, 3, 4, 5, 10, 15, 20],
        big_o="O(2^n)  <-- exponential!",
    )

    # #3: n must be a power of 2 for the n/2 recursion to land on integers
    print_table(
        "3. T(n) = 2*T(n/2) + 1, T(1) = 1",
        T3_recursive, T3_formula,
        n_values=[1, 2, 4, 8, 16, 32, 64, 128, 1024],
        big_o="O(n)",
    )

    # #4: n must be a power of 2 as well
    print_table(
        "4. T(n) = T(n/2) + 1, T(1) = 1",
        T4_recursive, T4_formula,
        n_values=[1, 2, 4, 8, 16, 32, 64, 128, 1024, 1_048_576],
        big_o="O(log n)",
    )

    # Extra: show side-by-side growth to make the difference between
    # O(n), O(2^n), and O(log n) visually obvious for the same small n's.
    print("=" * 70)
    print("Side-by-side growth comparison (same n for all four)")
    print("=" * 70)
    print(f"{'n':>6} {'#1 O(n)':>12} {'#2 O(2^n)':>18} {'#3 O(n)':>12} {'#4 O(log n)':>14}")
    print("-" * 70)
    for n in [1, 2, 4, 8, 16]:
        v1 = T1_recursive(n)
        v2 = T2_recursive(n)
        v3 = T3_recursive(n)
        v4 = round(T4_recursive(n), 3)
        print(f"{n:>6} {v1:>12} {v2:>18} {v3:>12} {v4:>14}")


if __name__ == "__main__":
    main()