## [Homework 1](https://github.com/ChristFarrell/_alg/tree/main/Homework/Homework%201%20090926)

This homework was getting helped by AI for help understanding.<br>

On this homework, we asked to do some comparison of four methods for calculating 2ⁿ and test the execution efficiency of each method when we put n value = 100.

| Mode | Logic | Time Complexity |
|---|---|---|
| Mode 1 | `return 2**n` | O(1) (Python's built-in large-integer exponentiation; while technically involving O(n) bitwise operations, it is treated as a constant-time operation from the user's perspective) |
| Mode 2a | `power2n(n-1) + power2n(n-1)` | O(2ⁿ): Each recursive level generates two sub-calls; the call tree grows exponentially |
| Mode 2b | `2 * power2n(n-1)` | O(n): Only one recursive call per level; the number of calls grows linearly |
| Mode 3 | Recursion + Memoization | O(n): Uses a dictionary to cache previously calculated values, avoiding redundant calculations |

1. Method 1 — 2**n
   ```
   def power2n_1(n):
        return 2 ** n
   ```
   The first method does not use recursion; instead, it utilizes Python's built-in system, which is pre-programmed and detected via (**).
   
2. Method 2a — power2n_2a(n - 1) + power2n_2a(n - 1)
   ```
   def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)
   ```
   This function calls power2n_2a(n - 1) twice, resulting in redundant computation. Every time n increases by 1, the amount of work doubles. For easy example, the recursion tree for n = 3 shows 8 calls to p(0).
   ```
                       power2n_2a(3)
                   /             \
          power2n_2a(2)         power2n_2a(2)
          /         \            /         \
   power2n_2a(1)  power2n_2a(1) power2n_2a(1) power2n_2a(1)
     /    \          /    \        /    \        /    \
   p(0)  p(0)      p(0)  p(0)    p(0)  p(0)    p(0)  p(0)
   ```

3. Method 2b — 2 * power2n(n-1)
   ```
   def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)
   ```
   Each call invokes itself only once. So, for n=100, the total number of function calls is 100 (linear, O(n)). Naturally, it is fast.
   ```
   power2n_2b(100)
   -> 2 * power2n_2b(99)
        -> 2 * power2n_2b(98)
              -> ...
                    -> 2 * power2n_2b(0)  → return 1
   ```

4. Method 3 - Recursion and Memoization
   ```
   _table = {0: 1}

   def power2n_3(n):
    if n in _table:
        return _table[n]
    result = 2 * power2n_3(n - 1)
    _table[n] = result
    return result
   ```
   The logic is exactly the same as in 2b (one recursive call per step), with the addition of a check to see if `n` is in `_table`. Every calculated result is immediately stored, so the code does not need to recompute it if the same value of `n` is provided.

Result
```
============================================================
Summary of Results
============================================================
Method                                   Status         Time / Note
------------------------------------------------------------
Method 1 (2**n)                          Success        0.000006 sec
Method 2a (power2n(n-1)+power2n(n-1))    Failed/Timeout 10.000054 sec
Method 2b (2*power2n(n-1))               Success        0.000029 sec
Method 3 (recursion + memoization)       Success        0.000076 sec