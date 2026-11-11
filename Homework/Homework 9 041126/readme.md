# [Homework 9](https://github.com/ChristFarrell/_alg/tree/main/Homework/Homework%209%20041126)

This homework was getting helped by AI Claude for understanding.<br>
AI Claude: https://claude.ai/share/3ec24a74-e8f6-41ad-abc5-c7994082fe68

On this homework, it is a collection of classic computer science puzzles and pathfinding problems, solved using various "search algorithms."<br>

1. Mouse in a Maze (DFS)
   The computer acts like a mouse trying to find a way out ('E') from a starting point ('S') within a maze. It uses an algorithm called "Depth-First Search" (DFS), which means it travels as far as possible along one path until it hits a dead end, then backtracks to try a different route. The program for solving a maze via DFS utilizes a stack implemented as a list to explore the maze cells one by one using the Depth-First Search method.
   ```py
   def solve_maze_dfs(maze, on_step=None):
    """Iterative DFS. '#' wall, 'S' start, 'E' exit. Returns (path, visited)."""
    rows, cols = len(maze), len(maze[0])
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "E":
                end = (r, c)

    stack = [(start, None)]
    parent, visited = {}, set()
    while stack:
        cur, par = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        parent[cur] = par
        if on_step:
            on_step(cur, visited, {p for p, _ in stack})
        if cur == end:
            path, node = [], end
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], visited
        r, c = cur
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):        # U R D L
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] != "#" and (nr, nc) not in visited):
                stack.append(((nr, nc), cur))
    return None, visited
    ```

   In the result, program managed to find a way out in 22 steps.
   <img src="Homework%209%20041126/gifs/1_maze_dfs.gif" width="1500" alt="Alt text describing the GIF">

2. Wolf, Goat, and Cabbage (BFS)
   This solves a puzzle in which a farmer must transport three items across a river without letting the wolf eat the goat, or the goat eat the cabbage, when left unattended. The computer uses a "Breadth-First Search" (BFS) algorithm to determine the minimum number of safe trips required. The program implements a FIFO (First-In, First-Out) queue system to ensure that route searching is conducted breadth-wise, or level by level. As long as the queue is not empty, the program continuously retrieves and examines the route at the front of the queue (using `popleft()`). If a new, safe branch is discovered from that route, it is added to the back of the queue (using `append()`).
   ```py
   def safe(s):
        f, w, g, c = s
        return not (w == g != f or g == c != f)

    start, goal = (0, 0, 0, 0), (1, 1, 1, 1)
    queue = deque([start])
    parent = {start: (None, None)}
    explored = 0
    while queue:
        s = queue.popleft()
        explored += 1
        if s == goal:
            break
        f = s[0]
        for i in range(4):                       # i = 0: alone, else carry item i
            if i != 0 and s[i] != f:
                continue
            ns = list(s)
            ns[0] = 1 - f
            if i:
                ns[i] = 1 - f
            ns = tuple(ns)
            if safe(ns) and ns not in parent:
                parent[ns] = (s, i)
                queue.append(ns)

    steps, s = [], goal
    while parent[s][0] is not None:
        prev, i = parent[s]
        steps.append((prev, i, s))
        s = prev
    return steps[::-1], explored
   ```
   In the result, program takes exactly 7 crossings for everyone to reach the other side of the river safely.
   <img src="Homework%209%20041126/gifs/2_wolf_goat_cabbage_bfs.gif" width="1500" alt="Alt text describing the GIF">

3. Eight Queens (DFS / Backtracking)
   The goal is to place 8 chess queens on a board so that none of them can attack each other. The program places them one by one, and if it makes a mistake (queens threaten each other), it goes back (backtracks) and tries a different spot. The program attempts to place queens row by row using `dfs(row)`. Whenever it finds a column position that is safe from attack (`if not attacked`), it places a queen (`board.append(c)`) and proceeds to explore the next row (`dfs(row + 1)`). However, if it reaches a dead end in a subsequent row—meaning no column is safe—the program backtracks by removing the most recently placed queen (`board.pop()`) and then shifts to try a different column in that same row.
   ```python
   def solve_n_queens(n=8, on_event=None, stop_at_first=False):
    """DFS row by row. on_event(board, kind) is called on 'place' and 'back'."""
    solutions, board = [], []

    def dfs(row):
        if row == n:
            solutions.append(board[:])
            return stop_at_first
        for c in range(n):
            if attacked(board, row, c):
                continue
            board.append(c)
            if on_event:
                on_event(board, "place")
            if dfs(row + 1):
                return True
            board.pop()
            if on_event:
                on_event(board, "back")
        return False

    dfs(0)
    return solutions
   ```

   In the result, program found a safe layout and noted that there are a total of 92 possible solutions.
   <img src="Homework%209%20041126/gifs/3_eight_queens_dfs.gif" width="1500" alt="Alt text describing the GIF">

4. NPC Chasing a Player (A Algorithm)
   Mimicking classic game mechanics, the computer employs the "A* (A-Star) algorithm" a highly intelligent and efficient method for calculating the shortest path to a target. During the search, whenever a branch path (nb) is encountered, the program calculates its score and adds it to a priority queue using `heapq.heappush()`. The command `heapq.heappop(heap)` then ensures that the program always selects and prioritizes the route with the lowest total score—the most promising one—first.
   ```python
   def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


   def astar_grid(grid, start, goal, on_step=None):
    """A* on a 4-connected grid, Manhattan heuristic. Returns (path, expanded)."""
    rows, cols = len(grid), len(grid[0])
    heap = [(manhattan(start, goal), 0, start)]
    g_cost, parent, closed = {start: 0}, {start: None}, set()
    while heap:
        _, g, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        if on_step:
            on_step(cur, closed, set(g_cost) - closed)
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], len(closed)
        r, c = cur
        for dr, dc in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            nb = (r + dr, c + dc)
            if not (0 <= nb[0] < rows and 0 <= nb[1] < cols) or grid[nb[0]][nb[1]] == "#":
                continue
            ng = g + 1
            if ng < g_cost.get(nb, float("inf")):
                g_cost[nb] = ng
                parent[nb] = cur
                heapq.heappush(heap, (ng + manhattan(nb, goal), ng, nb))
    return None, len(closed)
   ```

   In the result, the terminal displays the NPC recalculating its route as the player moves, ultimately managing to intercept the player on the 20th step.
   <img src="Homework%209%20041126/gifs/4_npc_chase_astar.gif" width="1500" alt="Alt text describing the GIF">


5. IC Circuit Routing
   This simulates the connection of small wires (nets) on a computer chip. The computer must connect corresponding points (such as pin A to pin A, pin B to pin B) across two different layers, without the wires colliding with one another or running into obstacles. We use the Lee algorithm, a wave expansion technique, from the starting point (S) to the destination point (T).<Br>
   
   The program begins its search from a starting point, S, and spreads gradually into all available empty spaces—much like ripples expanding in water (as illustrated by the distance values ​​1, 2, etc., radiating from S in the diagram). This expansion is managed using a deque (double-ended queue) to ensure it progresses uniformly, distance by distance (via `q.popleft()` and `q.append()`). <Br>
   
   Crucially, in addition to checking the adjacent cells—up, down, left, and right—the search also considers the possibility of transitioning to the opposite layer (represented as `(1 - l, r, c)`), which may provide a shortcut to bypass obstacles. Once this wave of distance values ​​reaches the target point, T, the program ceases its expansion and performs a "back-trace"—retracing the path by following the decreasing distance values ​​back toward S—to map out the shortest possible route for the cable.

   In the result, the terminal successfully connected 4 cable lines with a total cable length of 72.
   <img src="Homework%209%20041126/gifs/5_ic_routing.gif" width="1500" alt="Alt text describing the GIF">