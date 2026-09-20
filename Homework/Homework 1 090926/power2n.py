import sys
import time
import signal

sys.setrecursionlimit(10000)


# Method 1: Direct computation
def power2n_1(n):
    return 2 ** n


# Method 2a: Recursion (calls itself twice) -> O(2^n) calls
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)


# Method 2b: Recursion (multiply by 2) -> O(n) calls
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)


# Method 3: Recursion + lookup table (memoization)
_table = {0: 1}


def power2n_3(n):
    if n in _table:
        return _table[n]
    result = 2 * power2n_3(n - 1)
    _table[n] = result
    return result


class TimeoutError_(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError_("Timed out")


def time_call(name, func, n, timeout_sec=None):
    """Run a function and return (name, elapsed_time, success, result_or_error).

    If timeout_sec is given, the call is aborted (via SIGALRM) after that
    many seconds and reported as a timeout instead of hanging forever.
    """
    print(f"Testing {name} (n={n}) ...")
    if timeout_sec is not None:
        print(f"  (will give up after {timeout_sec} seconds if it hasn't finished)")

    old_handler = None
    if timeout_sec is not None:
        old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout_sec)

    start = time.perf_counter()
    try:
        result = func(n)
        elapsed = time.perf_counter() - start
        digits = len(str(result))
        print(f"  -> Done! Elapsed {elapsed:.6f} sec, result has {digits} digits")
        return (name, elapsed, True, digits)
    except TimeoutError_:
        elapsed = time.perf_counter() - start
        print(f"  -> Timed out after {elapsed:.2f} sec (did not finish within {timeout_sec} sec)")
        return (name, elapsed, False, f"Timeout (>{timeout_sec} sec)")
    except RecursionError:
        elapsed = time.perf_counter() - start
        print(f"  -> Failed (RecursionError): recursion depth exceeded. Elapsed {elapsed:.6f} sec")
        return (name, elapsed, False, "RecursionError")
    except Exception as e:
        elapsed = time.perf_counter() - start
        print(f"  -> Failed: {e}")
        return (name, elapsed, False, str(e))
    finally:
        if timeout_sec is not None:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


def main():
    N = 100
    results = []

    print("=" * 60)
    print(f"Comparing four power2n(n) methods, n = {N}")
    print("=" * 60)

    # Method 1: direct computation
    results.append(time_call("Method 1 (2**n)", power2n_1, N))

    # Method 2a: we actually attempt n=100, but cap it at a timeout since
    # it would otherwise never finish (it needs ~2^100 recursive calls).
    print()
    results.append(time_call("Method 2a (power2n(n-1)+power2n(n-1))", power2n_2a, N, timeout_sec=10))

    # Method 2b: linear recursion, n=100 is no problem
    print()
    results.append(time_call("Method 2b (2*power2n(n-1))", power2n_2b, N))

    # Method 3: recursion + lookup table
    print()
    results.append(time_call("Method 3 (recursion + memoization)", power2n_3, N))

    # Summary table
    print("\n" + "=" * 60)
    print("Summary of Results")
    print("=" * 60)
    print(f"{'Method':40s} {'Status':14s} {'Time / Note'}")
    print("-" * 60)
    for name, elapsed, ok, note in results:
        status = "Success" if ok else "Failed/Timeout"
        if elapsed is not None:
            time_str = f"{elapsed:.6f} sec"
        else:
            time_str = str(note)
        print(f"{name:40s} {status:14s} {time_str}")


if __name__ == "__main__":
    main()