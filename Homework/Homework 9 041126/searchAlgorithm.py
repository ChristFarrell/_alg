"""
Classic search problems in one file -- with terminal animation and GIF export
===================================================================
1. Mouse in a maze            -> DFS
2. Wolf-Goat-Cabbage crossing -> BFS
3. Eight Queens               -> DFS (backtracking)
4. NPC chasing the player     -> A*
5. IC circuit routing         -> Lee (BFS wave), A*, DFS, multi-net routing

Usage
-----
    python search_problems.py                 # run everything, animated
    python search_problems.py --only 1 3      # run only problems 1 and 3
    python search_problems.py --speed 2       # 2x faster  (0.5 = slower)
    python search_problems.py --no-animate    # static output only (no ANSI codes)
    python search_problems.py --gif           # save every animation as a .gif in ./gifs
    python search_problems.py --gif out --only 3 5   # choose folder / problems

GIF export needs Pillow:  pip install pillow

Run it in a real terminal (cmd / PowerShell / Terminal / VS Code terminal).
IDLE's shell does not understand ANSI cursor codes, so use --no-animate there.
"""

import argparse
import heapq
import os
import re
import shutil
import sys
import time
from collections import deque

# ----------------------------------------------------------------------
# Animation helpers
# ----------------------------------------------------------------------
ANIM = True      # set by main()
SPEED = 1.0      # animation speed multiplier


def C(code, text):
    """Colour a string with an ANSI code (only while animating)."""
    return f"\033[{code}m{text}\033[0m" if ANIM else text


RECORDER = None  # a GifRecorder while exporting GIFs


def pause(seconds):
    if RECORDER:
        RECORDER.hold(int(seconds * 1000 / SPEED))     # hold the last frame
    elif ANIM:
        time.sleep(seconds / SPEED)


def start_demo(title):
    if RECORDER:
        return
    if ANIM:
        sys.stdout.write("\033[2J\033[H")
    else:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)


ANSI_SEQ = re.compile(r"\x1b\[[0-9;]*m")


def term_size():
    s = shutil.get_terminal_size((100, 30))
    return s.lines, s.columns


def visible_len(line):
    return len(ANSI_SEQ.sub("", line))


def clip_ansi(line, width):
    """Cut a coloured line to `width` visible characters (so it can never wrap)."""
    out, pos, n = "", 0, 0
    for m in ANSI_SEQ.finditer(line):
        text = line[pos:m.start()][:max(0, width - n)]
        out += text + m.group(0)
        n += len(text)
        pos = m.end()
    out += line[pos:][:max(0, width - n)]
    return out + "\033[0m"


def show(title, lines, delay=0.05, final=False):
    """Draw one animation frame in place. In static mode only final frames print."""
    if RECORDER:
        RECORDER.add([C("1;37", title), ""] + list(lines), int(delay * 1000 / SPEED))
        return
    if not ANIM:
        if final:
            print("\n".join(lines))
        return
    body = [C("1;37", title), ""] + list(lines)
    rows, cols = term_size()
    if len(body) > rows - 1:             # never let a frame scroll the screen
        body = body[:rows - 2] + [C("1;31", "[terminal too small - enlarge it to see the whole frame]")]
    body = [clip_ansi(l, cols - 1) for l in body]
    sys.stdout.write("\033[H" + "\n".join(l + "\033[K" for l in body) + "\n\033[J")
    sys.stdout.flush()
    time.sleep(delay / SPEED)


# ----------------------------------------------------------------------
# GIF export: every frame passed to show() is rasterised with Pillow
# ----------------------------------------------------------------------
ANSI_RE = re.compile(r"\x1b\[([0-9;]*)m")
BG = (22, 24, 30)
FG = (225, 228, 235)
ANSI_RGB = {
    30: (60, 60, 70), 31: (240, 95, 95), 32: (95, 215, 125), 33: (245, 205, 85),
    34: (110, 155, 255), 35: (215, 125, 235), 36: (85, 205, 225), 37: (235, 235, 240),
    90: (88, 94, 108), 91: (255, 120, 120), 92: (120, 235, 150), 93: (255, 220, 110),
    94: (130, 175, 255), 95: (235, 150, 250), 96: (110, 225, 240), 97: (255, 255, 255),
}
CELL_W, CELL_H, FONT_SIZE, PAD = 11, 22, 17, 18


def parse_ansi(line):
    """Turn a line with ANSI colour codes into [(char, rgb), ...]."""
    out, color, pos = [], FG, 0
    for m in ANSI_RE.finditer(line):
        out += [(ch, color) for ch in line[pos:m.start()]]
        pos = m.end()
        for code in (int(x) if x else 0 for x in m.group(1).split(";")):
            if code == 0:
                color = FG
            elif code in ANSI_RGB:
                color = ANSI_RGB[code]
    out += [(ch, color) for ch in line[pos:]]
    return out


def load_font():
    from PIL import ImageFont
    for name in ("DejaVuSansMono.ttf", "Consolas.ttf", "consola.ttf", "Menlo.ttc",
                 "Courier New.ttf", "cour.ttf", "LiberationMono-Regular.ttf"):
        try:
            return ImageFont.truetype(name, FONT_SIZE)
        except OSError:
            pass
    try:
        return ImageFont.load_default(FONT_SIZE)
    except TypeError:                      # very old Pillow
        return ImageFont.load_default()


class GifRecorder:
    """Collects (lines, duration_ms) frames and writes them out as an animated GIF."""

    def __init__(self):
        self.frames = []

    def add(self, lines, ms):
        self.frames.append([lines, max(20, ms)])

    def hold(self, ms):
        if self.frames:
            self.frames[-1][1] += ms

    def save(self, path):
        from PIL import Image, ImageDraw
        font = load_font()
        parsed = [[parse_ansi(l) for l in lines] for lines, _ in self.frames]
        cols = max(len(row) for fr in parsed for row in fr)
        rows = max(len(fr) for fr in parsed)
        size = (cols * CELL_W + 2 * PAD, rows * CELL_H + 2 * PAD)

        def render(fr):
            img = Image.new("RGB", size, BG)
            d = ImageDraw.Draw(img)
            for y, row in enumerate(fr):
                top = PAD + y * CELL_H
                for x, (ch, col) in enumerate(row):
                    left = PAD + x * CELL_W
                    if ch == " ":
                        continue
                    if ch == "\u2588":                      # full block -> wall tile
                        d.rectangle([left, top + 1, left + CELL_W - 1, top + CELL_H - 2], fill=col)
                    elif ch == "\u00b7":                    # middle dot -> small round dot
                        cx, cy = left + CELL_W / 2, top + CELL_H / 2
                        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=col)
                    else:
                        w = d.textlength(ch, font=font)
                        d.text((left + (CELL_W - w) / 2, top + 1), ch, font=font, fill=col)
            return img

        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        first = render(parsed[0])
        first.save(path, save_all=True, append_images=(render(f) for f in parsed[1:]),
                   duration=[ms for _, ms in self.frames], loop=0, optimize=False)
        return len(self.frames), os.path.getsize(path)


# ----------------------------------------------------------------------
# Generic grid renderer (used by maze and A*)
# ----------------------------------------------------------------------
def render_grid(world, visited=(), frontier=(), cur=None, path=(), marks=None):
    """
    '#' wall. Colours: visited = cyan dot, frontier = yellow 'o',
    path = green '*'. `marks` = {(r,c): (char, colour)} drawn on top.
    """
    marks = marks or {}
    pathset = set(path)
    lines = []
    for r, row in enumerate(world):
        out = ""
        for c, ch in enumerate(row):
            p = (r, c)
            if p in marks:
                sym, col = marks[p]
                out += C(col, sym + " ")
            elif p == cur:
                out += C("1;33", "@ ")
            elif ch == "#":
                out += C("90", "██")
            elif p in pathset:
                out += C("1;32", "* ")
            elif p in frontier:
                out += C("33", "o ")
            elif p in visited:
                out += C("36", "· ")
            else:
                out += "  "
        lines.append(out)
    return lines


# ----------------------------------------------------------------------
# 1. Mouse in a maze  (DFS)
# ----------------------------------------------------------------------
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


def demo_maze():
    start_demo("1. Mouse in a maze (DFS)")
    maze = [
        "##########",
        "#S   #   #",
        "# ## # # #",
        "# #    # #",
        "# # #### #",
        "#   #  # #",
        "### # ## #",
        "#   #    E",
        "##########",
    ]
    marks = {}
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == "S":
                marks[(r, c)] = ("S", "1;32")
            elif ch == "E":
                marks[(r, c)] = ("E", "1;31")
    title = "1. Mouse in a maze (DFS)   @ = mouse   o = stack   · = visited"

    def on_step(cur, visited, frontier):
        show(title, render_grid(maze, visited, frontier, cur, marks=marks)
             + ["", f"Visited cells: {len(visited)}   Stack size: {len(frontier)}"], 0.06)

    path, visited = solve_maze_dfs(maze, on_step)
    if not path:
        print("No path found.")
        return
    # replay the final path step by step
    for i in range(1, len(path)):
        show(title, render_grid(maze, visited, (), path[i], path[:i], marks)
             + ["", "Exit found! Tracing the path back..."], 0.05)
    show(title, render_grid(maze, visited, (), None, path, marks)
         + ["", f"Path length: {len(path) - 1} steps, cells explored: {len(visited)}",
            "(DFS finds *a* path, not necessarily the shortest)"], 0.1, final=True)
    pause(2)


# ----------------------------------------------------------------------
# 2. Wolf, Goat, Cabbage  (BFS)
# ----------------------------------------------------------------------
NAMES = ["Farmer", "Wolf", "Goat", "Cabbage"]


def solve_wgc_bfs():
    """
    State = (farmer, wolf, goat, cabbage); 0 = left bank, 1 = right bank.
    BFS guarantees the minimum number of crossings.
    Returns (list of (state_before, cargo_index, state_after), states_explored).
    """
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


def wgc_frame(before, cargo, frac, text):
    """One frame. frac 0..1 = how far the boat is across the river."""
    W = 28
    boat_side = before[0]
    crossing = frac is not None
    left, right = [], []
    for i, n in enumerate(NAMES):
        if crossing and (i == 0 or i == cargo):
            continue                              # on the boat
        (left if before[i] == 0 else right).append(n)
    label = "[Boat]"
    if crossing:
        label = "[" + "+".join(NAMES[j] for j in (0, cargo) if j == 0 or j == cargo) + "]"
        label = label.replace("[Farmer+Farmer]", "[Farmer]")
        pos = frac if boat_side == 0 else 1 - frac
    else:
        pos = 0.0 if boat_side == 0 else 1.0
    x = int(round(pos * (W - len(label))))
    river = "~" * x + label + "~" * (W - len(label) - x)
    return [
        C("32", f"{'LEFT BANK':<30}") + C("34", f"{'RIVER':^{W}}") + C("32", f"{'RIGHT BANK':>30}"),
        f"{', '.join(left):<30}" + C("34", river) + f"{', '.join(right):>30}",
        "", text,
    ]


def demo_wgc():
    start_demo("2. Wolf, Goat and Cabbage (BFS)")
    steps, explored = solve_wgc_bfs()
    title = "2. Wolf, Goat and Cabbage (BFS)"
    log = []
    show(title, wgc_frame((0, 0, 0, 0), None, None, "Everyone starts on the left bank."), 1.0)
    for n, (before, cargo, after) in enumerate(steps, 1):
        who = "alone" if cargo == 0 else f"with the {NAMES[cargo].lower()}"
        side = "left -> right" if before[0] == 0 else "right -> left"
        log.append(f"  Step {n}: Farmer crosses {who} ({side})")
        for k in range(0, 11):
            show(title, wgc_frame(before, cargo, k / 10, f"Step {n}: Farmer crosses {who}...")
                 + [""] + log[:-1], 0.05)
        show(title, wgc_frame(after, None, None, f"Step {n} done: farmer crosses {who}.")
             + [""] + log, 0.5)
    show(title, wgc_frame((1, 1, 1, 1), None, None, "Everyone is safe on the right bank!")
         + [""] + log + ["", f"Minimum crossings: {len(steps)}   (BFS explored {explored} states)"],
         0.1, final=True)
    pause(2)


# ----------------------------------------------------------------------
# 3. Eight Queens  (DFS / backtracking)
# ----------------------------------------------------------------------
def attacked(board, r, c):
    return any(qc == c or abs(qr - r) == abs(qc - c) for qr, qc in enumerate(board))


def render_queens(n, board, status):
    """Queens in green. Squares attacked in the row currently being filled are red x."""
    row_now = len(board)
    lines = []
    for r in range(n):
        out = ""
        for c in range(n):
            if r < len(board) and board[r] == c:
                out += C("1;32", "Q ")
            elif r == row_now and attacked(board, r, c):
                out += C("31", "x ")
            else:
                out += C("90", "· ")
        lines.append(out)
    return lines + ["", status]


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


def demo_queens():
    start_demo("3. Eight Queens (DFS / backtracking)")
    title = "3. Eight Queens (DFS)   Q = queen   x = attacked in the next row"
    counter = {"place": 0, "back": 0}

    def on_event(board, kind):
        counter[kind] += 1
        msg = (f"Placed a queen in row {len(board)}" if kind == "place"
               else f"Dead end -> BACKTRACK to row {len(board) + 1}")
        show(title, render_queens(8, board, f"{msg}   (placements: {counter['place']}, "
                                               f"backtracks: {counter['back']})"),
             0.05 if kind == "place" else 0.03)

    first = solve_n_queens(8, on_event, stop_at_first=True)[0]
    total = len(solve_n_queens(8))
    show(title, render_queens(8, first, f"First solution found! Column per row: {first}")
         + [f"(8 queens have {total} solutions in total)"], 1.0, final=True)
    pause(2.5)


# ----------------------------------------------------------------------
# 4. NPC chasing the player  (A*)
# ----------------------------------------------------------------------
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


def demo_npc():
    start_demo("4. NPC chasing the player (A*)")
    world = [
        "....................",
        ".########.#########.",
        ".#......#.#.......#.",
        ".#.####.#.#.#####.#.",
        ".#.#..#.#...#...#.#.",
        ".#.#.##.#####.#.#.#.",
        ".#.#....#.....#.#.#.",
        ".#.######.#####.#.#.",
        ".#..............#...",
        "....................",
    ]
    npc, player = (2, 2), (4, 14)
    title = "4a. A* search   N = NPC   P = player   o = open list   · = closed list"

    def marks_for(npc, player):
        return {npc: ("N", "1;31"), player: ("P", "1;34")}

    def on_step(cur, closed, openset):
        show(title, render_grid(world, closed, openset, cur, marks=marks_for(npc, player))
             + ["", f"Nodes expanded: {len(closed)}   Open list: {len(openset)}"], 0.05)

    path, expanded = astar_grid(world, npc, player, on_step)
    for i in range(1, len(path)):
        show(title, render_grid(world, (), (), None, path[:i], marks_for(npc, player))
             + ["", "Target reached - drawing the path..."], 0.04)
    show(title, render_grid(world, (), (), None, path, marks_for(npc, player))
         + ["", f"Path length: {len(path) - 1}, nodes expanded: {expanded}"], 1.0, final=True)

    # ---- chase: the NPC re-plans with A* every tick while the player moves ----
    title = "4b. Chase simulation: the NPC re-plans with A* every tick"
    route = [(4, 14), (4, 15), (4, 15), (4, 14), (4, 13), (4, 13)]    # then the player stops
    trail = []
    for t in range(100):
        player = route[min(t, len(route) - 1)]
        plan, _ = astar_grid(world, npc, player)
        if plan is None:
            break
        if len(plan) > 1:
            trail.append(npc)
            npc = plan[1]
        remaining = plan[1:-1]
        marks = {p: ("·", "90") for p in trail}
        marks.update(marks_for(npc, player))
        show(title, render_grid(world, (), (), None, remaining, marks)
             + ["", f"t = {t:<3}  distance to player: {max(len(plan) - 2, 0)}"], 0.08)
        if npc == player:
            show(title, render_grid(world, (), (), None, (), marks)
                 + ["", C("1;31", f"The NPC caught the player at t = {t}!")], 0.1, final=True)
            break
    pause(2.5)


# ----------------------------------------------------------------------
# 5. IC circuit routing
# ----------------------------------------------------------------------
# 2 metal layers: layer 0 prefers horizontal wires, layer 1 prefers vertical.
# A via moves a wire between layers. Cell values: 0 free, 1 blocked.
VIA_COST = 3
WRONG_WAY_COST = 2
PLANAR = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def step_cost(layer, dr, dc):
    horizontal = dr == 0
    return 1 if (layer == 0) == horizontal else WRONG_WAY_COST


def lee_route(grid, src, dst, on_step=None):
    """Lee algorithm = BFS wave expansion + back-trace. Shortest in grid steps."""
    R, C_ = len(grid[0]), len(grid[0][0])
    dist = {src: 0}
    q = deque([src])
    while q:
        cur = q.popleft()
        if on_step:
            on_step(cur, dist)
        if cur == dst:
            break
        l, r, c = cur
        nbrs = [(l, r + dr, c + dc) for dr, dc in PLANAR] + [(1 - l, r, c)]
        for nb in nbrs:
            nl, nr, nc = nb
            if 0 <= nr < R and 0 <= nc < C_ and grid[nl][nr][nc] == 0 and nb not in dist:
                dist[nb] = dist[cur] + 1
                q.append(nb)
    if dst not in dist:
        return None, len(dist)
    path, cur = [dst], dst
    while cur != src:
        l, r, c = cur
        for nb in [(l, r + 1, c), (l, r - 1, c), (l, r, c + 1), (l, r, c - 1), (1 - l, r, c)]:
            if dist.get(nb, -1) == dist[cur] - 1:
                cur = nb
                path.append(cur)
                break
    return path[::-1], len(dist)


def astar_route(grid, src, dst):
    """A* router with via + preferred-direction costs. Returns (path, visited, cost)."""
    R, C_ = len(grid[0]), len(grid[0][0])
    h = lambda n: abs(n[1] - dst[1]) + abs(n[2] - dst[2])
    heap = [(h(src), 0, src)]
    best, parent, closed = {src: 0}, {src: None}, set()
    while heap:
        _, g, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        if cur == dst:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], len(closed), g
        l, r, c = cur
        cand = [((l, r + dr, c + dc), step_cost(l, dr, dc)) for dr, dc in PLANAR]
        cand.append(((1 - l, r, c), VIA_COST))
        for nb, cost in cand:
            nl, nr, nc = nb
            if 0 <= nr < R and 0 <= nc < C_ and grid[nl][nr][nc] == 0:
                ng = g + cost
                if ng < best.get(nb, float("inf")):
                    best[nb] = ng
                    parent[nb] = cur
                    heapq.heappush(heap, (ng + h(nb), ng, nb))
    return None, len(closed), None


def dfs_route(grid, src, dst):
    """DFS router: finds a legal route, usually long and winding."""
    R, C_ = len(grid[0]), len(grid[0][0])
    stack, parent = [src], {src: None}
    while stack:
        cur = stack.pop()
        if cur == dst:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], len(parent)
        l, r, c = cur
        for nb in [(l, r + dr, c + dc) for dr, dc in PLANAR] + [(1 - l, r, c)]:
            nl, nr, nc = nb
            if 0 <= nr < R and 0 <= nc < C_ and grid[nl][nr][nc] == 0 and nb not in parent:
                parent[nb] = cur
                stack.append(nb)
    return None, len(parent)


def count_vias(path):
    return sum(1 for a, b in zip(path, path[1:]) if a[0] != b[0])


def make_grid(rows, cols, obstacles):
    grid = [[[0] * cols for _ in range(rows)] for _ in range(2)]
    for r, c in obstacles:
        grid[0][r][c] = grid[1][r][c] = 1
    return grid


NET_COLOURS = ["31", "32", "33", "35", "36"]


def layer_lines(grid, wave=None, path=None, nets=None, pins=None, ends=None):
    """Draw both layers side by side. wave: {(l,r,c): dist}; path: list; nets: {name: path}."""
    R, C_ = len(grid[0]), len(grid[0][0])
    cell = {}
    for name, p in (nets or {}).items():
        col = NET_COLOURS[ord(name) % len(NET_COLOURS)]
        for i, n in enumerate(p):
            cell[n] = (name.lower(), col)
        for a, b in zip(p, p[1:]):
            if a[0] != b[0]:
                cell[a] = cell[b] = ("o", "1;35")
    for name, (s, t) in (pins or {}).items():
        col = NET_COLOURS[ord(name) % len(NET_COLOURS)]
        for n in (s, t):
            cell[(0, n[1], n[2])] = cell[(1, n[1], n[2])] = (name, "1;" + col)
    if path:
        for n in path:
            cell[n] = ("*", "1;32")
        for a, b in zip(path, path[1:]):
            if a[0] != b[0]:
                cell[a] = cell[b] = ("V", "1;35")
    for n, label in (ends or {}).items():
        cell[(0, n[1], n[2])] = cell[(1, n[1], n[2])] = (label, "1;33")

    lines = [f"{'Layer 0 (horizontal)':<{2 * C_ + 6}}Layer 1 (vertical)"]
    for r in range(R):
        row = ""
        for l in range(2):
            for c in range(C_):
                n = (l, r, c)
                if n in cell:
                    row += C(cell[n][1], cell[n][0] + " ")
                elif grid[l][r][c] == 1:
                    row += C("90", "██")
                elif wave and n in wave:
                    row += C("36", str(wave[n] % 10) + " ")
                else:
                    row += C("90", "· ")
            row += "      "
        lines.append(row.rstrip())
    return lines


def demo_routing():
    start_demo("5. IC circuit routing")
    R, C_ = 12, 16
    obstacles = {(r, 7) for r in range(2, 10)} | {(5, 3), (5, 4), (6, 11), (7, 11), (3, 12)}
    grid = make_grid(R, C_, obstacles)
    src, dst = (0, 5, 1), (0, 6, 14)
    ends = {src: "S", dst: "T"}

    # ---- Lee wave expansion, animated ----
    title = "5a. Lee algorithm: wave expansion from S (digits = distance mod 10)"
    tick = {"n": 0}

    def on_step(cur, dist):
        tick["n"] += 1
        if tick["n"] % 4 == 0:
            show(title, layer_lines(grid, wave=dist, ends=ends)
                 + ["", f"Cells reached by the wave: {len(dist)}"], 0.03)

    lee_path, lee_visited = lee_route(grid, src, dst, on_step)
    wave_final = {}
    lee_route(grid, src, dst, lambda cur, dist: wave_final.update(dist))
    for i in range(1, len(lee_path) + 1):
        show("5a. Lee algorithm: back-trace from T to S   (V = via)",
             layer_lines(grid, wave=wave_final, path=lee_path[:i], ends=ends)
             + ["", "Target reached - tracing the shortest path..."], 0.04)
    show("5a. Lee algorithm: done", layer_lines(grid, wave=wave_final, path=lee_path, ends=ends)
         + ["", f"Wire length: {len(lee_path) - 1}, vias: {count_vias(lee_path)}"], 1.0, final=True)
    pause(1.5)

    # ---- comparison table ----
    astar_path, astar_visited, _ = astar_route(grid, src, dst)
    dfs_path, dfs_visited = dfs_route(grid, src, dst)
    table = ["", f"{'Method':<22}{'Length':>8}{'Vias':>6}{'Visited':>9}",
             f"{'Lee (BFS wave)':<22}{len(lee_path)-1:>8}{count_vias(lee_path):>6}{lee_visited:>9}",
             f"{'A* (weighted cost)':<22}{len(astar_path)-1:>8}{count_vias(astar_path):>6}{astar_visited:>9}",
             f"{'DFS':<22}{len(dfs_path)-1:>8}{count_vias(dfs_path):>6}{dfs_visited:>9}",
             "", "Lee: shortest wire. A*: respects via/direction costs. DFS: legal but wasteful."]
    show("5b. Router comparison for one net", layer_lines(grid, path=dfs_path, ends=ends)
         + ["", "(drawn: the DFS route)"] + table, 0.1, final=True)
    pause(3.5)

    # ---- multi-net routing, one net at a time ----
    pins = {
        "A": ((0, 1, 1), (0, 10, 14)),
        "B": ((0, 1, 14), (0, 10, 1)),
        "C": ((0, 0, 8), (0, 11, 8)),
        "D": ((0, 4, 1), (0, 8, 6)),
    }
    title = "5c. Multi-net routing with A*  (each routed net blocks the next ones)"
    work = make_grid(R, C_, obstacles)
    routed, report = {}, []
    show(title, layer_lines(grid, pins=pins), 1.0)
    for name, (s, t) in pins.items():
        for other, (os_, ot) in pins.items():          # other nets' pins are off limits
            if other != name:
                for p in (os_, ot):
                    work[0][p[1]][p[2]] = work[1][p[1]][p[2]] = 1
        path, visited, cost = astar_route(work, s, t)
        for other, (os_, ot) in pins.items():
            if other != name:
                for p in (os_, ot):
                    if (p[1], p[2]) not in obstacles:
                        work[0][p[1]][p[2]] = work[1][p[1]][p[2]] = 0
        if path is None:
            report.append(f"Net {name}: FAILED (a real router would rip-up & re-route)")
        else:
            routed[name] = path
            for l, r, c in path:
                work[l][r][c] = 1
            report.append(f"Net {name}: length {len(path)-1:>3}, vias {count_vias(path)}, cost {cost}")
        show(title, layer_lines(grid, nets=routed, pins=pins) + [""] + report, 1.0)
    total_len = sum(len(p) - 1 for p in routed.values())
    total_via = sum(count_vias(p) for p in routed.values())
    show(title, layer_lines(grid, nets=routed, pins=pins) + [""] + report
         + ["", f"Routed {len(routed)}/{len(pins)} nets, total wire length {total_len}, vias {total_via}",
            "Legend: UPPERCASE = pins, lowercase = wires, o = via, ██ = macro block"],
         0.1, final=True)


# ----------------------------------------------------------------------
def main():
    global ANIM, SPEED, RECORDER
    ap = argparse.ArgumentParser(description="Search problems with terminal animation")
    ap.add_argument("--no-animate", action="store_true", help="static output only")
    ap.add_argument("--speed", type=float, default=1.0, help="animation speed (default 1.0)")
    ap.add_argument("--only", type=int, nargs="+", choices=range(1, 6), metavar="N",
                    help="run only these problems (1-5)")
    ap.add_argument("--gif", nargs="?", const="gifs", metavar="DIR",
                    help="save each animation as a GIF in DIR (default ./gifs); needs Pillow")
    args = ap.parse_args()
    ANIM, SPEED = (not args.no_animate) or bool(args.gif), max(args.speed, 0.01)
    if args.gif:
        try:
            import PIL  # noqa: F401
        except ImportError:
            sys.exit("GIF export needs Pillow:  pip install pillow")
    if os.name == "nt":
        os.system("")                          # enable ANSI escape codes on Windows

    demos = {1: demo_maze, 2: demo_wgc, 3: demo_queens, 4: demo_npc, 5: demo_routing}
    gif_names = {1: "1_maze_dfs.gif", 2: "2_wolf_goat_cabbage_bfs.gif",
                 3: "3_eight_queens_dfs.gif", 4: "4_npc_chase_astar.gif",
                 5: "5_ic_routing.gif"}
    order = args.only or sorted(demos)
    if ANIM and not args.gif:
        # Dry run (no drawing, no sleeping) to measure the biggest frame.
        global RECORDER
        need_r = need_c = 0
        for n in order:
            RECORDER = GifRecorder()
            demos[n]()
            for lines, _ in RECORDER.frames:
                need_r = max(need_r, len(lines) + 1)
                need_c = max(need_c, max(visible_len(l) for l in lines) + 1)
        RECORDER = None
        have_r, have_c = term_size()
        if have_r < need_r or have_c < need_c:
            print(f"Your terminal is {have_c} columns x {have_r} rows, but the animation "
                  f"needs about {need_c} x {need_r}.")
            print("Enlarge the terminal first (in VS Code: click 'Maximize Panel Size' on the "
                  "terminal toolbar, or drag the panel taller),")
            print("or use --gif to save the animations instead.")
            try:
                input("Press Enter to start (frames will be cropped), or Ctrl+C to quit... ")
            except EOFError:
                pass
    try:
        if ANIM and not args.gif:
            sys.stdout.write("\033[?25l")      # hide cursor
        for n in order:
            if args.gif:
                RECORDER = GifRecorder()
                print(f"Problem {n}: recording...", end=" ", flush=True)
            demos[n]()
            if args.gif:
                path = os.path.join(args.gif, gif_names[n])
                frames, size = RECORDER.save(path)
                print(f"saved {path}  ({frames} frames, {size / 1024:.0f} KB)")
                RECORDER = None
    except KeyboardInterrupt:
        pass
    finally:
        if ANIM and not args.gif:
            sys.stdout.write("\033[?25h\n")    # show cursor again


if __name__ == "__main__":
    main()