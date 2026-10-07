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

# [Homework 4](https://github.com/ChristFarrell/_alg/tree/main/Homework/Homework%204%20300926)

This homework was getting helped by AI Gemini for understanding.<br>
AI Gemini: https://share.gemini.google/T74Hwf3agvLY 

On the first homework, we asked to solves iterative method. The way to solve it is by repeating the steps one by one to gradually approach the correct answer. specifically, we use the Gradient Descent algorithm on the equation $$f(x) = x^4 - 3x^3 + 2$$.
It is designed to find the local minimum of a mathematical function by iteratively moving in the direction of steepest descent.<br>

The algorithm work with some step during the code:
```python
gradient = df(x) 
new_x = x - (learning_rate * gradient)
change = abs(new_x - x)
```
1. Calculate the Gradient: At the current position $x$, calculate the slope using the derivative $f'(x)$.
2. Take a Step: Move in the opposite direction of the slope. If the slope is positive (uphill), subtract from $x$ to move left. If the slope is negative, add to $x$ to move right.
3. Check for Convergence: Measure how much $x$ changed during this step. If the change is incredibly small, the algorithm has reached the bottom of the curve and can stop.

At the end, the result of equation was printed:
```
==================================================
 ALGORITHM 1: GRADIENT DESCENT
==================================================
Iteration 01: x = 2.880000 | Change = 1.120000
Iteration 02: x = 2.670981 | Change = 0.209019
Iteration 03: x = 2.550848 | Change = 0.120134
Iteration 04: x = 2.472545 | Change = 0.078302
Iteration 05: x = 2.418124 | Change = 0.054421
Iteration 06: x = 2.378801 | Change = 0.039323
Iteration 07: x = 2.349647 | Change = 0.029154
Iteration 08: x = 2.327642 | Change = 0.022005
Iteration 09: x = 2.310816 | Change = 0.016826
Iteration 10: x = 2.297826 | Change = 0.012990
Iteration 11: x = 2.287725 | Change = 0.010101
Iteration 12: x = 2.279827 | Change = 0.007898
Iteration 13: x = 2.273626 | Change = 0.006201
Iteration 14: x = 2.268741 | Change = 0.004885
Iteration 15: x = 2.264882 | Change = 0.003858
Iteration 16: x = 2.261829 | Change = 0.003054
Iteration 17: x = 2.259408 | Change = 0.002421
Iteration 18: x = 2.257487 | Change = 0.001921
Iteration 19: x = 2.255961 | Change = 0.001526
Iteration 20: x = 2.254747 | Change = 0.001213
```

We also use the Newton's method for optimization is a second-order algorithm that aims to find the stationary point of a function by seeking the root of its first derivative ($f'(x) = 0$). We take of equation $$f''(x) = 12x^2 - 18x$$ (second derivative from main equation)
```python

for i in range(max_iterations):
    first_deriv = df(x_nt)
    second_deriv = ddf(x_nt)
    
    if second_deriv == 0:
        print("Error: Second derivative is zero, cannot divide.")
        break
        
    # Newton's method calculates its own perfect step size using the second derivative
    x_new = x_nt - (first_deriv / second_deriv)
    
    change = abs(x_new - x_nt)
    x_nt = x_new
    
    print(f"Iteration {i+1:02d}: x = {x_nt:.6f} | Change = {change:.6f}")
    
    if change < tolerance:
        print("--> Newton's Method converged!\n")
        break
```
1. The program begins the search from the point $x = 4.0$. This figure will serve as the base value for the first iteration's calculation.
2. A program to calculate the first and second derivatives.
3. Using Newton's formula, the result of dividing the first derivative by the second derivative automatically serves as the step size. The old $x$ value is reduced by this quotient to obtain the new $x$ point (x_new).
4. `change = abs(x_new - x_nt)`: The program calculates the absolute distance between the newly obtained $x$ value and the previous $x$ value. This `change` value is used to assess the significance of the shift that has occurred. 
5. `x_nt = x_new`: The value of the variable $x$ is updated to the new $x$ value so that it can be used for calculations in the next iteration.
6. Evaluation stop condition.

At the end, the result of equation was printed:
```
==================================================
 ALGORITHM 2: NEWTON'S METHOD FOR OPTIMIZATION
==================================================
Iteration 01: x = 3.066667 | Change = 0.933333
Iteration 02: x = 2.533806 | Change = 0.532861
Iteration 03: x = 2.301941 | Change = 0.231865
Iteration 04: x = 2.252243 | Change = 0.049699
Iteration 05: x = 2.250004 | Change = 0.002238
Iteration 06: x = 2.250000 | Change = 0.000004
--> Newton's Method converged!
```
In conclusion, Newton's Method is far smarter and more efficient, as it can account for the graph's "curvature" to calculate the perfect step size, whereas Gradient Descent still takes a long time to reach the same point.

On the second homework, there explain more variation of iterative method. At the end it shows of sophisticated algorithms from various fields are built upon the exact same basic framework: Guess ➔ Update ➔ Check for stability (convergence) ➔ Repeat.<br>

At first, the program work in (generic_iterator). This framework requires only three things to work:
```python
def generic_iterator(transition_func, is_converged, initial_state, max_iter=1000):
    """
    通用迭代法框架
    :param transition_func: 狀態推進函數 g(state) -> next_state
    :param is_converged: 終止/收斂判定函數 is_converged(state, next_state, iteration) -> bool
    :param initial_state: 初始狀態（純量、向量、矩陣或 Tuple）
    :return: 最終狀態, 實際迭代次數
    """
    state = initial_state
    
    for iteration in range(max_iter):
        next_state = transition_func(state)
        
        if is_converged(state, next_state, iteration):
            return next_state, iteration + 1
            
        state = next_state
        
    print("  [警告] 達到最大迭代次數仍未完全收斂")
    return state, max_iter
```
- initial_state: An initial guess.
- transition_func: A formula for taking a new step (refining the guess).
- is_converged: A stopping rule (determining when the guess is considered accurate or no longer changing).

The second part of the code demonstrates that the abstract framework described above can be used to implement nine well-known algorithms with widely varying functions:
| | Algorithm Name | What it Solves (The Problem) | 
| :--- | :--- | :--- | 
| **1** | Fixed-Point Iteration | Finds a point where the input of a function exactly equals its output ($x = g(x)$). | 
| **2** | Newton's Method | Finds the roots (zeroes) of a mathematical function (e.g., finding where $x^2 - 4 = 0$). | 
| **3** | Gauss-Seidel | Solves large, complex systems of linear equations (finding variables in $Ax = b$) step-by-step. | 
| **4** | Power Iteration | Finds the dominant (largest) eigenvalue and its corresponding eigenvector of a matrix. | 
| **5** | QR Algorithm | Calculates *all* the eigenvalues of a matrix simultaneously. | 
| **6** | Runge-Kutta (RK4) | Solves Ordinary Differential Equations (ODEs) to predict how a system changes over time. | 
| **7** | PageRank | Calculates the relative importance of nodes in a network based on the links connecting them. | 
| **8** | K-Means Clustering | Groups unlabelled data points into *K* distinct clusters based on their distance from a center point. |  
| **9** | EM Algorithm| Estimates hidden or missing parameters in a statistical model (like guessing the bias of two mixed-up coins). |

1. Fixed Point Iteration
   A pure mathematical algorithm for finding a point where the input value equals the output value (a fixed point).
   ```
   --- 1. 二維不動點迭代法 (Fixed-Point Iteration) ---
   結果: [0.24138  0.896552] (耗時 23 次迭代)
   ```

2. Newton's Method
   A lightning-fast method for finding the roots of mathematical equations (where the graph intersects zero).
   ```
   --- 2. 牛頓法求根 (Newton's Method: x^2 - 4 = 0) ---
   結果: 根 x = 2.000000 (耗時 5 次迭代)
   ```

3. Gauss-Seidel
   A method computers use to solve complex systems of linear equations (such as finding the values ​​of x, y, and z across multiple equations).
   ```
   --- 3. 高斯-賽得爾法 (Gauss-Seidel Linear Solver) ---
   結果: x = [2.25 2.   3.75] (耗時 9 次迭代)
   ```

4. Power Iteration
   A linear algebra algorithm used to find the most dominant vector direction (eigenvector/eigenvalue) of a matrix.
   ```
   --- 4. 冪次迭代法 (Power Iteration: SVD / 主特徵向量) ---
   結果: 最大特徵值 = 4.721570 (耗時 17 次迭代)
   ```

5. QR Algorithm
   A more advanced version of Power Iteration used to find all eigenvalues.
   ```
   --- 5. QR 演算法 (QR Algorithm: 計算所有特徵值) ---
   結果: 所有特徵值 = [5.732051 2.267949 1.      ] (耗時 19 次迭代)
   ```

6. Runge-Kutta (RK4)
   An algorithm used in physics engines for games or weather simulations to predict movement over time (solving differential equations).
   ```
   --- 6. 龍格-庫塔法 (RK4 ODE Solver: dy/dt = y - t + 1) ---
   結果: 於 t = 2.0 時, y = 9.388889 (耗時 10 步)
   ```

7. PageRank
   The legendary algorithm that made Google wealthy; it determines the importance of a webpage based on the number of links pointing to it.
   ```
   --- 7. PageRank (Power Iteration 隨機衝浪者模型) ---
   結果: 網頁權重分佈 = [0.3246 0.2251 0.2251 0.2251] (耗時 15 次迭代)
   ```

8. K-Means
   A machine learning algorithm for clustering data (e.g., grouping customers based on their shopping habits).
   ```
   --- 8. K-Means 聚類 (Hard EM 演算法) ---
   結果: 最終分群中心 = 
   [[-2.1143 -2.128 ]
    [ 1.826   1.7977]] (耗時 4 次迭代)

   ```

9. EM Algorithm (Expectation-Maximization)
   A clever statistical algorithm for estimating probabilities when data is incomplete (for instance, estimating the probability of getting heads or tails when using two mixed-up coins).
   ```
   --- 9. EM 演算法 (Two-Coin Problem 潛在變數估計) ---
   結果: 估計硬幣機率 Theta_A = 0.7968, Theta_B = 0.5196 (耗時 16 次迭代)
   ```

# [Homework 5](https://github.com/ChristFarrell/_alg/tree/main/Homework/Homework%205%20071026)

This homework was getting helped by AI Gemini for understanding.<br>
AI Gemini: https://share.gemini.google/dEAhx6n5rP3z

On the first homework, we asked to finish The Tower of Hanoi using recursion. The rules are:<br>
1. Only one disk can be moved at a time.
2. Each move involves removing the top disc from one of the poles.
3. A larger plate cannot be placed on top of a smaller plate.

The formula for the minimum number of steps for n the disc is: $2^n - 1$

At the end, the result was printed:
```
=== Tower of Hanoi with (3 plates) ===
Move the disc from Pole A to Pole C using Pole B

Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C

Finish on 7 step recursion!
```

Now after we finishing using recursion, we now use iterative. The main program itself:
1. Which disk moves, where The disk that needs to move at step $i$ corresponds directly to the position of the lowest set bit (rightmost 1) in the binary representation of $i$.
2. Where the disk moves, each disk cycles through the pegs in a fixed direction. 
   - Odd Disks (1, 3, 5...): Always move forward along the pegs ($A \rightarrow B \rightarrow C \rightarrow A$).
   - Even Disks (2, 4, 6...): Always move backward along the pegs ($A \rightarrow C \rightarrow B \rightarrow A$).

During the code itself, It have some part of rules:
1. Total moves & Parity Adjustment
   ```python
   total_moves = (1 << n) - 1  # Equivalent to 2^n - 1

   if n % 2 == 0:
      pegs = [source, auxiliary, target]
   else:
      pegs = [source, target, auxiliary]
   ```
   - 1 << nuses bit-shifting to calculate$2^n$efficiently.
   - Parity Adjustment: If the total number of disks $n$ is even, swapping target and auxiliary in the pegs list ensures the largest disk lands on the correct target peg at the final move.

2. Tracking disk positions
   ```python
   disk_pos = [0] * (n + 1)
   ```

3. Find out which disc is moving
   ```python
   for i in range(1, total_moves + 1):
      disk = (i & -i).bit_length()
   ```
   - (i & -i): Uses bitwise AND with standard Two's Complement arithmetic to isolate the lowest set bit of $i$. For example in (Step $i$ = 2), Binary of 2 is 010. 1. The lowest bit is in the 2nd position. So, disk = 2.

4. Calculate the displacement of the pole
   ```python
   from_idx = disk_pos[disk]

   if disk % 2 == 1:
      to_idx = (from_idx + 1) % 3  # Piringan Ganjil: Maju 1 langkah
   else:
      to_idx = (from_idx + 2) % 3  # Piringan Genap: Mundur 1 langkah

   disk_pos[disk] = to_idx
   ```
   - Initial Location (from_idx): Disc 2 is currently on the Pole 0 (Pole A).
   - Odd/Even Check: disk = 2 is Even.
   - Calculate the Goal Post (to_idx), where: $\text{to\_idx} = (0 + 2) \pmod 3 = 2 \quad \text{(B pole)}$
   - Result: Disc 2 is updated to position 2(Pole B). Output: Move disk 2 from A to B.

At the end, the result was printed:
```
=== Tower of Hanoi with (3 plates) ===
Move the disc from Pole A to Pole C using Pole B

Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C

Finish on 7 step iteration!
```

On second homework, we asked to finish symbolic differentiation. It is a computational method for automatically deriving mathematical functions by applying pure calculus rules to an Abstract Syntax Tree (AST) data structure in the form of a Tuple/List. Applied Mathematical Rules are constants, target variables, addition/subtraction, multiplication, differentiation, exponents, trigonometric functions, and the chain rule are fundamental concepts in symbolic calculus.

There are 6 Calculus Differentiation RUles Applied
1. Constant Rule<br>
$\frac{d}{dx}\left(c\right) = 0$
2. Power Rule <br>
$\frac{d}{dx}\left(u^{n}\right) = n\,u^{\,n-1}\,u'$
3. Sum & Difference Rule <br>
$(f \pm g)' = f' \pm g'$
4. Product Rule <br>
$(u \cdot v)' = u'v + uv'$
5. Quotient Rule <br>
$\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^{2}}$
6. Chain Rule <br>
$\big(f(u)\big)' = f'(u)\cdot u',\quad \text{e.g. } \frac{d}{dx}\sin(u)=\cos(u)\,u'$

THe main component of code are:
1. sym_diff(expr, var): A primary recursive function that breaks down complex expressions into smaller sub-expressions and then applies differentiation rules based on the operators involved.

2. _smart_binop(op, u, v): An internal helper that performs real-time simplification (eliminating redundant nodes such as x * 0, 1 * x, or x + 0).

At the end, the result was printed:
```
f(x)   = ('+', ('**', 'x', 2), ('*', 3, 'x'))
f'(x)  = ('+', ('*', 2, 'x'), 3)
----------------------------------------
g(x)   = ('sin', ('**', 'x', 2))
g'(x)  = ('*', ('cos', ('**', 'x', 2)), ('*', 2, 'x'))
```

On third homework, we asked to replaces all conventional looping mechanisms (for / while) with Recursion (Recursive Approach). During map, filter, and reduce implementation, there are 3 main functions.

1. my_map, apply the function to the head, then combine it (+) with the result of the recursion on the tail. If the list is empty (not lst), return [].
2. my_filter, Check if the head satisfies the predicate. If True, keep the head plus the result of the recursive call on the tail; if False, take only the result of the recursive call on the tail. If the list is empty (not lst), return [].
3. my_reduce, accumulates values ​​from left to right. Passes the intermediate accumulated result `func(initial, head)` as the new `initial` for the next recursion (Tail Recursion). If the list is empty (`not lst`), returns `initial`.

ON the bubble sort, we use Inner Pass and Outer Pass
1. Inner Pass (bubble_pass)
   - Compares two adjacent elements: head (element 1) and second (element 2). 
   - If head > second, their positions are swapped, and the larger element continues to "bubble" to the right via recursion on the remainder of the list. 
   - At the end of one pass, the largest element is guaranteed to be in the rightmost position.
2. Outer Pass (bubble_sort)
   - Call `bubble_pass` $n$ times. 
   - Each time a pass is completed, the parameter $n$ is decremented by 1 ($n - 1$) until the entire list is perfectly sorted.

At the end, the result was printed:
```
=== 1. Testing my_map, my_filter, my_reduce ===
Input List:     [1, 2, 3, 4, 5, 6]
my_map (^2):    [1, 4, 9, 16, 25, 36]
my_filter (evens): [2, 4, 6]
my_reduce (sum):   21

=== 2. Testing Bubble Sort (Loop-free) ===
Before Sort:    [64, 34, 25, 12, 22, 11, 90]
After Sort:     [11, 12, 22, 25, 34, 64, 90]
```