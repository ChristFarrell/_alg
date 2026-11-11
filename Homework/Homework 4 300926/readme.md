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
