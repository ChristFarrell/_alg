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