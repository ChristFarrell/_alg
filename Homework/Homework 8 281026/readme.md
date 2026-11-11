# [Homework 8](https://github.com/ChristFarrell/_alg/blob/main/Homework/Homework%208%20281026/Algorithms.py)

This homework was getting helped by AI Claude for understanding.<br>
AI Claude: https://claude.ai/share/676fff04-50e2-4f08-b49e-cc6b02dcc46f

On this homework, given a set of $n$ cities and a symmetric distance matrix $D \in \mathbb{R}^{n \times n}$, where $D_{i,j}$ represents the Euclidean distance between city $i$ and city $j$, the goal of the Traveling Salesman Problem is to find a permutation tour $\pi = (\pi_1, \pi_2, \dots, \pi_n)$ that minimizes the total tour length $L(\pi)$:

1. Improved Method (2-opt)
   The 2-opt local search algorithm is an improvement method that iteratively eliminates crossing edges in a planar graph by swapping edge pairs.
   Step by step:
   - Select two pairs of paths—for example, the paths from city $a \to b$ and $c \to d$
   - The formula for the change in distance ($\Delta$) is: 

$$
\Delta = (D_{a,c} + D_{b,d}) - (D_{a,b} + D_{c,d})
$$

      In other words: the distance of the new paths minus the distance of the original paths
   - Decision (If-Else): <br>
      a. If $\Delta < 0$ (meaning the new route is shorter), reverse the order of the cities between $b$ and $c$.<br>
      b. If $\Delta \ge 0$, take no action. Repeat this process (sweep) until no further instances of $\Delta < 0$ remain.
   - Repeat this process (sweep) until no further instances of $\Delta < 0$ remain.

   Result:
   ```
   ==============================================================================
   2-opt (Improvement)
   ==============================================================================
   [     0] Random start tour 7-8-1-5-6-2-4-9-3-10-11-0  length 6.420
   [     1] Sweep 1: swap edges (7,8)+(1,5) -> (7,1)+(8,5), delta=-0.658 (after 0 rejected tries). Length 5.762
   [     2] Sweep 1: swap edges (7,1)+(3,10) -> (7,3)+(1,10), delta=-0.178 (after 5 rejected tries). Length 5.584
   [     3] Sweep 1: swap edges (3,9)+(2,6) -> (3,2)+(9,6), delta=-0.180 (after 3 rejected tries). Length 5.404
   [     4] Sweep 1: swap edges (3,2)+(8,1) -> (3,8)+(2,1), delta=-0.302 (after 2 rejected tries). Length 5.102
   [     5] Sweep 1: swap edges (3,8)+(1,10) -> (3,1)+(8,10), delta=-0.158 (after 0 rejected tries). Length 4.944
   [     6] Sweep 1: swap edges (3,1)+(0,7) -> (3,0)+(1,7), delta=-0.265 (after 2 rejected tries). Length 4.680
   [     7] Sweep 1: swap edges (0,11)+(8,5) -> (0,8)+(11,5), delta=-0.156 (after 1 rejected tries). Length 4.523
   [     8] Sweep 1: swap edges (0,8)+(6,9) -> (0,6)+(8,9), delta=-0.092 (after 1 rejected tries). Length 4.432
   [     9] Sweep 1: swap edges (0,6)+(9,4) -> (0,9)+(6,4), delta=-0.616 (after 0 rejected tries). Length 3.816
   [    10] Sweep 1: swap edges (8,10)+(5,6) -> (8,5)+(10,6), delta=-0.809 (after 11 rejected tries). Length 3.007
   [    11] Sweep 1: swap edges (11,10)+(6,4) -> (11,6)+(10,4), delta=-0.008 (after 9 rejected tries). Length 2.999
   [    11] End of sweep 1: found improvements, scan again
   [    12] Sweep 2: swap edges (3,0)+(5,11) -> (3,5)+(0,11), delta=-0.310 (after 11 rejected tries). Length 2.689
   [    13] Sweep 2: swap edges (5,8)+(0,11) -> (5,0)+(8,11), delta=-0.010 (after 7 rejected tries). Length 2.680
   [    14] Sweep 2: swap edges (5,0)+(11,6) -> (5,11)+(0,6), delta=-0.140 (after 0 rejected tries). Length 2.540
   [    15] Sweep 2: swap edges (11,8)+(0,6) -> (11,0)+(8,6), delta=-0.102 (after 6 rejected tries). Length 2.437
   [    16] Sweep 2: swap edges (0,9)+(8,6) -> (0,8)+(9,6), delta=-0.033 (after 5 rejected tries). Length 2.404
   [    16] End of sweep 2: found improvements, scan again
   [    16] End of sweep 3: no improving move
   [    17] Local optimum for 2-opt. Final length 2.404
   ```

2. Hill Climbing
   Hill Climbing is a greedy local search strategy that evaluates the immediate neighborhood $N(\pi)$ of the current tour $\pi$ and transitions strictly to the neighbor offering the steepest reduction in total cost. 
   Step by step:
   - Try swapping the positions of two random cities, $i$ and $j$, within the route.
   - Calculate the distance of the new route, $L_{\text{new}}$.
   - Evaluate all possible neighboring swaps, then choose the swap that results in the shortest distance: 
      
$$
\text{Best Route} = \arg\min (L_{\text{new}})
$$

   - Decision (If-Else): <br>
      a. If $L_{\text{new}} < L_{\text{old}}$, move to the new route. <br>
      b. f no neighboring configuration is better, the program terminates (stuck at a local optimum).
   Result:
   ```
   ==============================================================================
   Hill Climbing
   ==============================================================================
   [     0] Random start tour 8-0-1-6-10-4-3-2-9-11-5-7  length 4.540
   [     1] Iter 1: 66 neighbours checked, 20 better. Best = swap cities 9<->7 (positions 8,11): 4.540 -> 3.793
   [     2] Iter 2: 66 neighbours checked, 14 better. Best = swap cities 1<->11 (positions 2,9): 3.793 -> 3.383
   [     3] Iter 3: 66 neighbours checked, 9 better. Best = swap cities 3<->1 (positions 6,9): 3.383 -> 2.844
   [     4] Iter 4: 66 neighbours checked, 5 better. Best = swap cities 1<->2 (positions 6,7): 2.844 -> 2.707
   [     5] Iter 5: 66 neighbours checked, 3 better. Best = swap cities 11<->9 (positions 2,11): 2.707 -> 2.631
   [     6] Iter 6: 66 neighbours checked, 2 better. Best = swap cities 8<->0 (positions 0,1): 2.631 -> 2.404
   [     7] Checked all 66 neighbours: none is better -> stuck on a peak (local optimum). Final length 2.404
   ```

3. Simulated Annealing
   Simulated Annealing models physical cooling dynamics to escape local minimum traps by probabilistically accepting inferior candidate moves based on a decreasing temperature parameter $T$.  
   Step by step:
   - Generate a new route proposal using the 2-opt method, and calculate the difference in distance: $\Delta = L_{\text{new}} - L_{\text{old}}$.
   - Metropolis Probability Formula ($P$): If the new route is worse ($\Delta > 0$), calculate the probability of accepting this inferior route: 
      
$$
P = e^{-\frac{\Delta}{T}}
$$

      Where $T$ is the current temperature.
   - Decision (If-Else):<br>
      a. If $\Delta < 0$ $\to$ ACCEPT immediately.<br> 
      b. If $\Delta > 0$ $\to$ Generate a random number $r \in [0, 1]$. If $r < P$, ACCEPT it anyway, even though it is worse!
   - Cooling Formula: 

$$
T = T \times \alpha \quad (\text{e.g., } \alpha = 0.995)
$$

      As the temperature $T$ decreases, the value of $P$ approaches 0, making it increasingly rare to accept an inferior route.
   Result:
   ```
   ==============================================================================
   Simulated Annealing
   ==============================================================================
   [     0] Random start length 4.489. Start temperature T=0.4489, cooling x0.995 per stage, 100 proposals per stage.
   [     1] T=0.4489 reverse segment [1..4]: better (-0.180) -> ACCEPT. Current 4.309, best 4.309
   [     2] T=0.4489 reverse segment [4..8]: worse (+0.005), p=exp(-d/T)=0.990 > rand 0.707 -> ACCEPT anyway. Current 4.314, best 4.309
   [     3] T=0.4489 reverse segment [5..8]: better (-0.017) -> ACCEPT. Current 4.297, best 4.297
   [     4] T=0.4489 reverse segment [3..8]: better (-0.238) -> ACCEPT. Current 4.059, best 4.059
   [     5] T=0.4489 reverse segment [8..9]: worse (+0.263), p=0.556 < rand 0.588 -> reject. Current 4.059, best 4.059
   [     6] T=0.4489 reverse segment [1..7]: worse (+0.554), p=0.291 < rand 0.596 -> reject. Current 4.059, best 4.059
   [     7] T=0.4489 reverse segment [5..6]: worse (+0.616), p=0.254 < rand 0.576 -> reject. Current 4.059, best 4.059
   [     8] T=0.4489 reverse segment [2..4]: better (-0.422) -> ACCEPT. Current 3.636, best 3.636
   [     9] T=0.4489 reverse segment [2..3]: worse (+0.091), p=exp(-d/T)=0.816 > rand 0.033 -> ACCEPT anyway. Current 3.728, best 3.636
   [    10] T=0.4489 reverse segment [4..10]: worse (+0.479), p=0.344 < rand 0.477 -> reject. Current 3.728, best 3.636
   [     1] Stage 1: T=0.4489  improved 24, accepted-worse 30, rejected 46  | current 5.343  best 3.090
   [    50] Stage 50: T=0.3511  improved 21, accepted-worse 29, rejected 50  | current 3.513  best 2.575
   [   100] Stage 100: T=0.2733  improved 28, accepted-worse 27, rejected 45  | current 4.132  best 2.560
   [   150] Stage 150: T=0.2127  improved 26, accepted-worse 33, rejected 41  | current 4.921  best 2.437
   [   200] Stage 200: T=0.1656  improved 12, accepted-worse 17, rejected 71  | current 3.171  best 2.404
   [   250] Stage 250: T=0.1289  improved 6, accepted-worse 15, rejected 79  | current 3.020  best 2.404
   [   300] Stage 300: T=0.1003  improved 10, accepted-worse 8, rejected 82  | current 2.540  best 2.404
   [   350] Stage 350: T=0.0781  improved 2, accepted-worse 12, rejected 86  | current 2.710  best 2.404
   [   400] Stage 400: T=0.0608  improved 3, accepted-worse 4, rejected 93  | current 2.560  best 2.404
   [   450] Stage 450: T=0.0473  improved 2, accepted-worse 7, rejected 91  | current 2.459  best 2.404
   [   500] Stage 500: T=0.0368  improved 2, accepted-worse 6, rejected 92  | current 2.541  best 2.404
   [   550] Stage 550: T=0.0286  improved 2, accepted-worse 6, rejected 92  | current 2.404  best 2.404
   [   600] Stage 600: T=0.0223  improved 1, accepted-worse 6, rejected 93  | current 2.423  best 2.404
   [   650] Stage 650: T=0.0174  improved 1, accepted-worse 1, rejected 98  | current 2.404  best 2.404
   [   700] Stage 700: T=0.0135  improved 2, accepted-worse 5, rejected 93  | current 2.404  best 2.404
   [   750] Stage 750: T=0.0105  improved 0, accepted-worse 4, rejected 96  | current 2.423  best 2.404
   [   800] Stage 800: T=0.0082  improved 1, accepted-worse 3, rejected 96  | current 2.404  best 2.404
   [   850] Stage 850: T=0.0064  improved 2, accepted-worse 2, rejected 96  | current 2.404  best 2.404
   [   900] Stage 900: T=0.0050  improved 0, accepted-worse 7, rejected 93  | current 2.404  best 2.404
   [   950] Stage 950: T=0.0039  improved 0, accepted-worse 1, rejected 99  | current 2.404  best 2.404
   [  1000] Stage 1000: T=0.0030  improved 4, accepted-worse 5, rejected 91  | current 2.404  best 2.404
   [  1050] Stage 1050: T=0.0023  improved 2, accepted-worse 8, rejected 90  | current 2.404  best 2.404
   [  1100] Stage 1100: T=0.0018  improved 1, accepted-worse 2, rejected 97  | current 2.404  best 2.404
   [  1150] Stage 1150: T=0.0014  improved 0, accepted-worse 5, rejected 95  | current 2.404  best 2.404
   [  1200] Stage 1200: T=0.0011  improved 2, accepted-worse 5, rejected 93  | current 2.404  best 2.404
   [121901] Frozen (T<0.001). Best tour found: length 2.404
   ```

4. Gradient Descent via Continuous Relaxation
   Because standard TSP is discrete and non-differentiable, continuous relaxation techniques relax the discrete permutation vector into a doubly stochastic matrix $P \in \mathbb{R}^{n \times n}$ via log-domain Sinkhorn normalization.
   Step by step:
   - An $N \times N$ matrix containing probability values ​​(e.g., $P_{i,k}$ = the probability that city $i$ is visited at position $k$).
   - Transforms a matrix of arbitrary values ​​($\Theta$) into a doubly stochastic matrix (where the sum of each row and each column is always 1)
   - Gradient Update Formula: 
   
$$
\Theta_{\text{new}} = \Theta_{\text{old}} - \text{learning rate} \times \nabla L
$$

      Adjusts the values ​​in $\Theta$ in a direction that minimizes the total route distance.
   - Converts the relaxed probability matrix back into a definitive (discrete) sequence of city visits.
   Result:
   ```
   ==============================================================================
   Gradient Descent
   ==============================================================================
   [     0] Random logits -> P is ~uniform (every city equally likely at every position). lr=0.5, tau=0.3
   [     1] Step 1: expected length 4.963, |grad|=9.982, confidence(mean max P)=0.13, rounded tour 4.161, best 4.161
   [    50] Step 50: expected length 2.246, |grad|=10.706, confidence(mean max P)=0.61, rounded tour 3.495, best 2.404
   [   100] Step 100: expected length 2.217, |grad|=10.602, confidence(mean max P)=0.67, rounded tour 3.260, best 2.404
   [   150] Step 150: expected length 2.219, |grad|=10.605, confidence(mean max P)=0.66, rounded tour 3.260, best 2.404
   [   200] Step 200: expected length 2.214, |grad|=10.601, confidence(mean max P)=0.66, rounded tour 3.260, best 2.404
   [   250] Step 250: expected length 2.213, |grad|=10.601, confidence(mean max P)=0.66, rounded tour 3.633, best 2.404
   [   300] Step 300: expected length 2.213, |grad|=10.604, confidence(mean max P)=0.66, rounded tour 3.633, best 2.404
   [   350] Step 350: expected length 2.207, |grad|=10.602, confidence(mean max P)=0.65, rounded tour 3.633, best 2.404
   [   400] Step 400: expected length 2.198, |grad|=10.597, confidence(mean max P)=0.63, rounded tour 3.417, best 2.404
   [   450] Step 450: expected length 2.191, |grad|=10.597, confidence(mean max P)=0.62, rounded tour 3.417, best 2.404
   [   500] Step 500: expected length 2.192, |grad|=10.599, confidence(mean max P)=0.62, rounded tour 3.417, best 2.404
   [   550] Step 550: expected length 2.202, |grad|=10.617, confidence(mean max P)=0.63, rounded tour 3.417, best 2.404
   [   600] Step 600: expected length 2.208, |grad|=10.693, confidence(mean max P)=0.65, rounded tour 3.678, best 2.404
   [   601] Projected back to a valid permutation. Best rounded tour length 2.404
   ```

5. Greedy Method: Nearest Neighbor
   The Nearest Neighbor algorithm builds a valid tour construction sequentially by making greedy local decisions: picking the closest unvisited city at every step.
   Step by step:
   - Currently at city ($cur$).
   - Find the destination city $j$ from the list of unvisited cities ($U$) that has the smallest distance $D_{cur, j}$: 

$$
\text{Next City} = \arg\min_{j \in U} D_{cur, j}
$$

   - Move to city $j$, remove $j$ from the list $U$, and repeat the process until all cities have been visited. 
   - Return to the starting city to close the route loop.
   Result:
   ```
   ==============================================================================
   Nearest Neighbor (Greedy)
   ==============================================================================
   [     0] Start at city 0. Rule: always go to the closest unvisited city.
   [     1] At city 0. Closest unvisited: 11(d=0.092), 9(d=0.148), 8(d=0.234) ... -> go to 11. Path length so far 0.092
   [     2] At city 11. Closest unvisited: 5(d=0.180), 9(d=0.235), 8(d=0.299) ... -> go to 5. Path length so far 0.271
   [     3] At city 5. Closest unvisited: 3(d=0.237), 7(d=0.385), 2(d=0.409) ... -> go to 3. Path length so far 0.508
   [     4] At city 3. Closest unvisited: 7(d=0.174), 2(d=0.291), 1(d=0.366) ... -> go to 7. Path length so far 0.682
   [     5] At city 7. Closest unvisited: 2(d=0.188), 1(d=0.198), 4(d=0.362) ... -> go to 2. Path length so far 0.870
   [     6] At city 2. Closest unvisited: 1(d=0.172), 4(d=0.182), 10(d=0.382) ... -> go to 1. Path length so far 1.041
   [     7] At city 1. Closest unvisited: 4(d=0.329), 10(d=0.484), 6(d=0.516) ... -> go to 4. Path length so far 1.371
   [     8] At city 4. Closest unvisited: 10(d=0.222), 6(d=0.260), 9(d=0.461) ... -> go to 10. Path length so far 1.592
   [     9] At city 10. Closest unvisited: 6(d=0.038), 9(d=0.529), 8(d=0.651) -> go to 6. Path length so far 1.631
   [    10] At city 6. Closest unvisited: 9(d=0.548), 8(d=0.668) -> go to 9. Path length so far 2.179
   [    11] At city 9. Closest unvisited: 8(d=0.128) -> go to 8. Path length so far 2.307
   [    12] All cities visited. Close the loop 8 -> 0 (+0.234). Final length 2.541

   ==============================================================================
   ```

At the end, only the Nearest Neighbor that taking the greedy length to finish the algorithm, compare to other 4 algorithm
```
==============================================================================
SUMMARY (shorter is better)
==============================================================================
Simulated Annealing          length = 2.4039   tour = 2-4-10-6-9-8-0-11-5-3-7-1
Gradient Descent             length = 2.4039   tour = 4-10-6-9-8-0-11-5-3-7-1-2
2-opt (Improvement)          length = 2.4039   tour = 7-3-5-11-0-8-9-6-10-4-2-1
Hill Climbing                length = 2.4039   tour = 0-8-9-6-10-4-2-1-7-3-5-11
Nearest Neighbor (Greedy)    length = 2.5414   tour = 0-11-5-3-7-2-1-4-10-6-9-8`
```