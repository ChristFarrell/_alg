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
      to_idx = (from_idx + 1) % 3  
   else:
      to_idx = (from_idx + 2) % 3 

   disk_pos[disk] = to_idx
   ```
   - Initial Location (from_idx): Disc 2 is currently on the Pole 0 (Pole A).
   - Odd/Even Check: disk = 2 is Even.
   - Calculate the Goal Post (to_idx), where: `to_idx = (0 + 2) % 3 = 2` (B pole)
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

At the end, the result was printed with pure mathemathical structure:
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