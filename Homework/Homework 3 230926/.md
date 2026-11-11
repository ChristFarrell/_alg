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