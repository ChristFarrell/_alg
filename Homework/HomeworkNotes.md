# NOTES

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
```

## [Homework 2](https://github.com/ChristFarrell/_alg/tree/main/Homework/Homework%202%20160926)

This homework was getting helped by AI for help understanding.<br>

On this homework, we asked to solves and verifies four recurrence relations that commonly appear when analyzing the time complexity of recursive algorithms. There was four recurrences from this program

| # | Recurrence | Base case | Closed-form formula | Big-O |
|---|---|---|---|---|
| 1 | `T(n) = T(n-1) + 8` | `T(1) = 1` | `T(n) = 8n - 7` | O(n) |
| 2 | `T(n) = 2·T(n-1) + 9` | `T(1) = 1` | `T(n) = 10·2^(n-1) - 9` | O(2ⁿ) |
| 3 | `T(n) = 2·T(n/2) + 1` | `T(1) = 1` | `T(n) = 2n - 1` | O(n) |
| 4 | `T(n) = T(n/2) + 1` | `T(1) = 1` | `T(n) = 1 + log₂n` | O(log n) |

1. O(n)
   ```python
   def T1_recursive(n):
       if n in _memo1:
           return _memo1[n]
      result = T1_recursive(n - 1) + 8
      _memo1[n] = result
      return result
   ```
   Each call reduces `n` by 1 and adds a constant (8). Solving the recurrence by unrolling it gives `T(n) = T(1) + 8(n-1) = 8n - 7`. Growth is proportional to `n` — linear.

2. O(2ⁿ)
   ```python
   def T2_recursive(n):
       if n in _memo2:
           return _memo2[n]
      result = 2 * T2_recursive(n - 1) + 9
      _memo2[n] = result
      return result
   ```
   At each step, the task size decreases by only 1 (n-1), yet the function is called twice. Consequently, the number of branches keeps doubling as the recursion proceeds, causing the total number of calls to explode to 2ⁿ.

3. O(n)
   ```python
   def T3_recursive(n):
      if n in _memo3:
           return _memo3[n]
     result = 2 * T3_recursive(n // 2) + 1
     _memo3[n] = result
     return result
   ```
   The concept is similar to number 2, but the task is split in half (n/2) rather than simply reduced by 1. Consequently, although the process branches twofold, the size of the task in each branch is also halved.

4. O(log n)
   ```python
   def T4_recursive(n):
    if n in _memo4:
        return _memo4[n]
    result = T4_recursive(n // 2) + 1
    _memo4[n] = result
    return result
   ```
   Each call halves the problem size and adds only a constant amount of work (no doubling). Since halving `n` repeatedly takes `log₂(n)` steps to reach the base case, `T(n) = 1 + log₂(n)`

Result
The final block in `main()` prints all four recurrences' results for the same small set of `n` values (1, 2, 4, 8, 16), making the difference in growth rate directly visible. Even though `n` only grows from 1 to 16 (a 16x increase), #2's result grows to over 327,000, while #4 only grows from 1 to 5:
```
======================================================================
Side-by-side growth comparison (same n for all four)
======================================================================
     n      #1 O(n)          #2 O(2^n)      #3 O(n)    #4 O(log n)
----------------------------------------------------------------------
     1            1                  1            1              1
     2            9                 11            3              2
     4           25                 71            7              3
     8           57               1271           15              4
    16          121             327671           31              5
```
 
# [Homework 3](https://github.com/ChristFarrell/_alg/blob/main/Homework/Homework%203%20230926/SAT.py)

This homework was getting helped by AI Opencode for understanding.<br>

On this homework, we asked to solves SAT for Boolean formulas. It uses Truth Table Generation to exhaustively test all $2^n$ possible truth assignments for $n$ boolean variables and checks if at least one assignment satisfies the formula.

1. Combinations Generation
   ```python
   itertools.product([True, False], repeat=n)
   ```
   Generates the complete search space of $2^n$ combinations (0s and 1s) systematically. For 3 variables ($A, B, C$), it generates $2^3 = 8$ combinations.

2. Environment Mapping
   ```python
   env = dict(zip(variables, values))
   ```
   Maps variable names dynamically to their boolean assignment (e.g., {'A': True, 'B': False, 'C': True}).

3. Calculation of Formula
   We remember the concept rule of truth table.
   | Math Symbol | Operator Name | Formula in Python | 1 Condition |
   |---|---|---|---|
   | v | OR | A or B | It has a value of 1 if at least one of the variables has a value of 1 |
   | ^ | AND | clause1 and clause2 | Values ​​1 if ALL clauses value 1 at once |
   | ~ | NOT | not A | Inverting the value: if A=0, it becomes 1; if A=1, it becomes 0. |

4. Result
   ```
   Find solution of SAT for formula: (A v B) ^ (~A v C) ^ (~B v ~C)

   ┌───┬───┬───┬──────────┐
   │ A │ B │ C │  Result  │
   ├───┼───┼───┼──────────┤
   │ 1 │ 1 │ 1 │    0     │
   │ 1 │ 1 │ 0 │    0     │
   │ 1 │ 0 │ 1 │ 1 (SAT)  │
   │ 1 │ 0 │ 0 │    0     │
   │ 0 │ 1 │ 1 │    0     │
   │ 0 │ 1 │ 0 │ 1 (SAT)  │
   │ 0 │ 0 │ 1 │    0     │
   │ 0 │ 0 │ 0 │    0     │
   └───┴───┴───┴──────────┘

   Result: SATISFIABLE (2 solutions found)
   └─> A=1, B=0, C=1
   └─> A=0, B=1, C=0

   Find solution of SAT for formula: (A v B) ^ (~A v C) ^ (~B v C)

   ┌───┬───┬───┬──────────┐
   │ A │ B │ C │  Result  │
   ├───┼───┼───┼──────────┤
   │ 1 │ 1 │ 1 │ 1 (SAT)  │
   │ 1 │ 1 │ 0 │    0     │
   │ 1 │ 0 │ 1 │ 1 (SAT)  │
   │ 1 │ 0 │ 0 │    0     │
   │ 0 │ 1 │ 1 │ 1 (SAT)  │
   │ 0 │ 1 │ 0 │    0     │
   │ 0 │ 0 │ 1 │    0     │
   │ 0 │ 0 │ 0 │    0     │
   └───┴───┴───┴──────────┘

   Result: SATISFIABLE (3 solutions found)
   └─> A=1, B=1, C=1
   └─> A=1, B=0, C=1
   └─> A=0, B=1, C=1
   ```

