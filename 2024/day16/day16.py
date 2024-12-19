import sys
from math import inf
from collections import defaultdict

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIR_MAP = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}

def genCandidates(plot, x, y, direction, score, genPrev=False):
  candidates = [(x, y, delta, score + 1000) for delta in [UP, DOWN, LEFT, RIGHT] if direction != delta]
  nextX, nextY = x + direction[0], y + direction[1]
  if genPrev:
    nextX, nextY = x - direction[0], y - direction[1]
  if 0 < nextX < len(plot[0]) and 0 < nextY < len(plot) and plot[nextY][nextX] != '#':
    candidates.append((nextX, nextY, direction, score+1))
  return candidates

def printPath(plot, visited, end):
  x, y, direction, _ = end
  while (x, y) != (1, len(plot) - 2):
    candidates = genCandidates(plot, x, y, direction, inf, True)
    nextX, nextY, nextDir, _ = min(candidates, key=lambda c: visited[(c[0], c[1], c[2])])
    plot[nextY][nextX] = DIR_MAP[nextDir]
    x, y, direction = nextX, nextY, nextDir
  print("finalplot\n" + "\n".join(["".join(row) for row in plot]))

def part1(plot: list[list[str]]) -> tuple[dict[tuple[int, int, tuple[int, int]], int], tuple[int, int, tuple[int, int]]]:
  visited, candidates = defaultdict(lambda: inf), defaultdict(lambda: inf)
  candidates[(1, len(plot) - 2, RIGHT)] = 0
  endX, endY = len(plot[0]) - 2, 1
  while candidates:
    x, y, change, score = 0, 0, UP, inf
    for (checkX, checkY, checkChange), checkScore in candidates.items():
      if checkScore < score:
        x, y, change, score = checkX, checkY, checkChange, checkScore

    del candidates[(x, y, change)]
    visited[(x, y, change)] = score
    # if x == endX and y == endY:
    #   continue
    for X, Y, Dir, Score in genCandidates(plot, x, y, change, score):
      if (X, Y, Dir) not in visited and candidates[(X, Y, Dir)] > Score:
        candidates[(X, Y, Dir)] = Score
  end = min([(endX, endY, d, visited[(endX, endY, d)]) for d in [UP, DOWN, LEFT, RIGHT]], key=lambda x: x[3])
  printPath(plot, visited, end)
  print(f"lowest score: {end[3]}")
  return visited, end

def findPaths(plot, visited, x, y, direction, processed):
  processed[(x, y, direction)] = None
  if (x, y) == (1, len(plot) - 2):
    processed[(x, y, direction)] = True
    return True
  candidates = genCandidates(plot, x, y, direction, inf, True)
  candidates = [(c[0], c[1], c[2], visited[(c[0], c[1], c[2])]) for c in candidates]
  partOfPath = False
  for c in candidates:
    if (c[0], c[1], c[2]) in processed:
      continue
    if c[3] < visited[(x, y, direction)]:
      if findPaths(plot, visited, c[0], c[1], c[2], processed):
        partOfPath = True
  processed[(x, y, direction)] = partOfPath
  return partOfPath

def findPaths2(plot, visited, x, y, direction, prev):
  if (x, y, direction) in prev:
    return
  if (x, y) == (1, len(plot) - 2):
    prev[(x, y, direction)] = set()
    return 
  candidates = genCandidates(plot, x, y, direction, inf, True)
  candidates = [(c[0], c[1], c[2], visited[(c[0], c[1], c[2])]) for c in candidates]
  curr = (x, y, direction)
  prev[curr] = set()
  for c in map(lambda x: (x[0], x[1], x[2]), candidates):
    if visited[c] < visited[curr]:
      findPaths2(plot, visited, c[0], c[1], c[2], prev)
      if c in prev:
        prev[curr].add(c)
  if not prev[curr]:
    del prev[curr]
  return

def part2(plot: list[list[str]]):
  visited, end = part1(plot)
  partsOfPath = {}
  findPaths2(plot, visited, end[0], end[1], end[2], partsOfPath)
  paths = set([(part[0], part[1]) for part in partsOfPath])
  for y in range(len(plot)):
    s = ""
    for x in range(len(plot[0])):
      s += (plot[y][x] if (x, y) not in paths else 'O')
    print(s)
  print(f"len(paths): {len(paths)}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  plot = [list(line.rstrip()) for line in f.readlines()]
  part1(plot) if part == "pt1" else part2(plot)
