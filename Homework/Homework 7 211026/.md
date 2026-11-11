# [Homework 7](https://github.com/ChristFarrell/_alg/blob/main/Homework/Homework%207%20211026/blast.py)

This homework was getting helped by AI Claude for understanding.<br>
AI Claude: https://claude.ai/share/49e18198-3697-4d05-b585-7d76a608a929

On this homework, we asked to make comparison program from dynamic progamming and non-dynamic progamming. At first, we do dynamic progamming, by using Smith-Waterman Algorithm. Smith-Waterman is an exact method that finds the best possible local alignment between two sequences by calculating every single cell in a grid. It works by some step:
1. Matrix Initialization: A table $H$ of size $(N+1) \times (M+1)$ is initialized with zeros, where $N$ is the query length and $M$ is the database length.

2. Matrix Filling (Recurrence Relation):
   Every cell $H[i][j]$ is calculated based on its three immediate neighbors, Setting negative values to 0 allows local alignments to start anywhere without penalty from bad preceding sequences:

$$
H[i][j] = \max \begin{cases} 
0 \\ 
H[i-1][j-1] + \text{score}(a_i, b_j) & \text{(Match / Mismatch)} \\ 
H[i-1][j] + \text{gap} & \text{(Deletion)} \\ 
H[i][j-1] + \text{gap} & \text{(Insertion)} 
\end{cases}
$$

3. Tracking the Maximum: As the table fills, the code keeps track of the absolute highest score ($best$) and its location $(bi, bj)$.

4. Traceback: Starting from $(bi, bj)$, the algorithm works backward to reconstruct the exact alignment path until it hits a cell with a value of 0.

Second, we do non-dynamic progamming, by using Seed-and-Extend Algorithm. Seed-and-extend is a fast, shortcut method (like BLAST). Instead of checking everything, it looks for short exact matches (seeds) first and only extends those. It works by some step:
1. Indexing (Step 1): The database sequence is split into overlapping words of length k (k-mers) and indexed in a hash table (dictionary) mapping each $k$-mer to its positions in the database.

2. Seed Matching (Step 2): The query sequence is scanned for $k$-mers. When a match is found in the database index, a "seed" is formed.

3. Diagonal Clustering (Step 3): Hits are grouped by diagonal index, calculated as: 

$$
\text{diagonal} = \text{database position} - \text{query position}
$$

   Real alignments yield multiple hits aligned on the same diagonal, whereas random hits scatter across different diagonals.

4. X-Drop Extension (Step 4): Each seed is extended left and right along its diagonal base-by-base:
   - Score improves: Keep extending and update the best score.
   - Score drops: If the score drops below best - xdrop, extension stops early (X-drop termination). This saves massive amounts of computation on unpromising alignment branches.

At the end, the result shown up as this with explanation:
Dynamic Progamming
```
========================================================================
PART A - small example
========================================================================
database d = TTGACCGATCGGATTACAGCTA   # Small Example Analysis
query    q = GATCGGATAACAG            # database include 22 bases and query indluce 13 bases

[DP] Table size = 13 x 22 = 286 cells (ALL of them will be computed)  # DP Result
[DP] row   1/13 done   best score so far = 2 at cell (1,3)
[DP] row   2/13 done   best score so far = 4 at cell (2,4)
[DP] row   3/13 done   best score so far = 6 at cell (3,9)
[DP] row   4/13 done   best score so far = 8 at cell (4,10)
[DP] row   5/13 done   best score so far = 10 at cell (5,11)
[DP] row   6/13 done   best score so far = 12 at cell (6,12)
[DP] row   7/13 done   best score so far = 14 at cell (7,13)
[DP] row   8/13 done   best score so far = 16 at cell (8,14)
[DP] row   9/13 done   best score so far = 16 at cell (8,14)
[DP] row  10/13 done   best score so far = 17 at cell (10,16)
[DP] row  11/13 done   best score so far = 19 at cell (11,17)
[DP] row  12/13 done   best score so far = 21 at cell (12,18)
[DP] row  13/13 done   best score so far = 23 at cell (13,19)
[DP] New-best events during filling: 12 (last 5: [(8, 14, 16), (10, 16, 17), (11, 17, 19), (12, 18, 21), (13, 19, 23)])

[DP] Score table H:
             T   T   G   A   C   C   G   A   T   C   G   G   A   T   T   A   C   A   G   C   T   A
       0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0   0
  G    0   0   0   2   0   0   0   2   0   0   0   2   2   0   0   0   0   0   0   2   0   0   0
  A    0   0   0   0   4   2   0   0   4   2   0   0   1   4   2   0   2   0   2   0   1   0   2
  T    0   2   2   0   2   3   1   0   2   6   4   2   0   2   6   4   2   1   0   1   0   3   1
  C    0   0   1   1   0   4   5   3   1   4   8   6   4   2   4   5   3   4   2   0   3   1   2
  G    0   0   0   3   1   2   3   7   5   3   6  10   8   6   4   3   4   2   3   4   2   2   0
  G    0   0   0   2   2   0   1   5   6   4   4   8  12  10   8   6   4   3   1   5   3   1   1
  A    0   0   0   0   4   2   0   3   7   5   3   6  10  14  12  10   8   6   5   3   4   2   3
  T    0   2   2   0   2   3   1   1   5   9   7   5   8  12  16  14  12  10   8   6   4   6   4
  A    0   0   1   1   2   1   2   0   3   7   8   6   6  10  14  15  16  14  12  10   8   6   8
  A    0   0   0   0   3   1   0   1   2   5   6   7   5   8  12  13  17  15  16  14  12  10   8
  C    0   0   0   0   1   5   3   1   0   3   7   5   6   6  10  11  15  19  17  15  16  14  12
  A    0   0   0   0   2   3   4   2   3   1   5   6   4   8   8   9  13  17  21  19  17  15  16
  G    0   0   0   2   0   1   2   6   4   2   3   7   8   6   7   7  11  15  19  23  21  19  17

[DP] Traceback from best cell (13,19), H=23, until H = 0:
   (13,   19) match    G/G  H=23
   (12,   18) match    A/A  H=21
   (11,   17) match    C/C  H=19
   (10,   16) match    A/A  H=17
   ( 9,   15) MISMATCH A/T  H=15
   ( 8,   14) match    T/T  H=16
   ( 7,   13) match    A/A  H=14
   ( 6,   12) match    G/G  H=12
   ( 5,   11) match    G/G  H=10
   ( 4,   10) match    C/C  H=8
   ( 3,    9) match    T/T  H=6
   ( 2,    8) match    A/A  H=4
   ( 1,    7) match    G/G  H=2

[DP] Alignment (query starts at q[0], database starts at d[6]):
   q: GATCGGATAACAG
       ||||||||x||||
   d: GATCGGATTACAG

# DP checked all 286 cells sequentially, accumulated matching scores (+2), subtracted gaps (-2), and traced back from the highest scoring cell down to 0.

[SE] Step 1 - index: 19 k-mers -> 19 distinct 4-mers (0.0000s)
[SE] Step 2 - seeds: looked up 10 query 4-mers -> 6 seed hits
[SE] Step 3 - hits per diagonal (d-q). A real alignment = many seeds on ONE diagonal:
        diagonal      6:   6 seeds, best extended score = 23
        (0 other diagonals have just 1 hit = random noise)

[SE] Step 4 - extension in detail for seed q[0] <-> d[6] (diagonal 6):
      extend right:
        q[4]=G d[10]=G +2  cur=2 best=2 new best
        q[5]=G d[11]=G +2  cur=4 best=4 new best
        q[6]=A d[12]=A +2  cur=6 best=6 new best
        q[7]=T d[13]=T +2  cur=8 best=8 new best
        q[8]=A d[14]=T -1  cur=7 best=8 
        q[9]=A d[15]=A +2  cur=9 best=9 new best
        q[10]=C d[16]=C +2  cur=11 best=11 new best
        q[11]=A d[17]=A +2  cur=13 best=13 new best
        q[12]=G d[18]=G +2  cur=15 best=15 new best
      extend left:
      total = seed 8 + right 15 + left 0 = 23
[SE] Total extension steps = 54   (compare with DP cells)
```

Non-Dynamic Progamming
```
========================================================================
PART B - original program: 20,000-base database
========================================================================
query = d[12000:12060] with 3 mutations at q[10], q[30], q[50]  

------------------------------ DP ------------------------------
[DP] Table size = 60 x 20000 = 1,200,000 cells (ALL of them will be computed)
[DP] row  10/60 done   best score so far = 20 at cell (10,12010)
[DP] row  20/60 done   best score so far = 37 at cell (20,12020)
[DP] row  30/60 done   best score so far = 57 at cell (30,12030)
[DP] row  40/60 done   best score so far = 74 at cell (40,12040)
[DP] row  50/60 done   best score so far = 94 at cell (50,12050)
[DP] row  60/60 done   best score so far = 111 at cell (60,12060)
[DP] New-best events during filling: 61 (last 5: [(56, 12056, 103), (57, 12057, 105), (58, 12058, 107), (59, 12059, 109), (60, 12060, 111)])

[DP] Traceback from best cell (60,12060), H=111, until H = 0:
   (60,12060) match    T/T  H=111
   (59,12059) match    T/T  H=109
   (58,12058) match    G/G  H=107
   ...                                    # continue program until small H
   ( 1,12001) match    G/G  H=2

[DP] Alignment (query starts at q[0], database starts at d[12000]):
   q: GACAACGGCACTATATCGACCAAACATAGCCAGTCCTAGCGGCAATCGAAAGGGGGCGTT
       ||||||||||x|||||||||||||||||||x|||||||||||||||||||x|||||||||
   d: GACAACGGCAATATATCGACCAAACATAGCAAGTCCTAGCGGCAATCGAAGGGGGGCGTT

------------------------ Seed-and-extend ------------------------
[SE] Step 1 - index: 19,996 k-mers -> 1024 distinct 5-mers (0.0072s)
[SE] Step 2 - seeds: looked up 56 query 5-mers -> 1,142 seed hits
[SE] Step 3 - hits per diagonal (d-q). A real alignment = many seeds on ONE diagonal:
        diagonal  12000:  41 seeds, best extended score = 111
        diagonal   8240:   5 seeds, best extended score = 27
        diagonal  16484:   5 seeds, best extended score = 16
        diagonal   6215:   5 seeds, best extended score = 18
        diagonal  16629:   4 seeds, best extended score = 22
        (562 other diagonals have just 1 hit = random noise)

[SE] Step 4 - extension in detail for seed q[0] <-> d[12000] (diagonal 12000):
      extend right:
        q[5]=C d[12005]=C +2  cur=2 best=2 new best
        q[6]=G d[12006]=G +2  cur=4 best=4 new best
        q[7]=G d[12007]=G +2  cur=6 best=6 new best
        q[8]=C d[12008]=C +2  cur=8 best=8 new best
        q[9]=A d[12009]=A +2  cur=10 best=10 new best
        ...                              # continue program until last q
        q[59]=T d[12059]=T +2  cur=101 best=101 new best
      extend left:
      total = seed 10 + right 101 + left 0 = 111

[SE] Noise check: 1,101 hits off the true diagonal, best noise score = 31  (they die quickly by X-drop)
[SE] Total extension steps = 28,281   (compare with DP cells)
```

At the end, the final result will be printed as:
```
Smith-Waterman : score=111  position in d=12000  time=0.941s
Seed-extend    : score=111  position in d=12000  time=0.0378s
Speedup        : 25x
```
| Metric | Smith-Waterman (DP) | Seed-and-Extend |
| :--- | :--- | :--- |
| **Method Type** | Exact | Heuristic |
| **Alignment Score** | 111 | 111 |
| **Position in Database ($d$)** | 12000 | 12000 |
| **Execution Time** | 0.941s | 0.0378s |
| **Speedup Factor** | Baseline ($1\times$) | **$25\times$ faster** |

Non-DP (Seed-and-Extend) methods are significantly faster because they utilize an indexing system (k-mer) to focus the search directly on sequence regions with high potential, while also employing an "X-drop" mechanism to terminate evaluation prematurely if alignment scores decline. In contrast to Dynamic Programming (Smith-Waterman), which uses a brute-force approach to calculate all 1,200,000 matrix cells uniformly, including irrelevant, random regions—Seed-and-Extend prunes the vast majority of the search space. It processes only the areas surrounding matching seeds, thereby delivering identical accuracy (a score of 111 at position 12,000) while achieving an execution speed 25 times faster.