import sys
from math import inf
from collections import defaultdict

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

def genCandidates(plot, x, y, direction, score):
  candidates = [(x, y, delta, score + 1000) for delta in [UP, DOWN, LEFT, RIGHT]]
  nextX, nextY = x + direction[0], y + direction[1]
  if 0 < nextX <= len(plot[0]) and 0 < nextY < len(plot) and plot[nextY][nextX] != '#':
    candidates.append((nextX, nextY, direction, score+1))
  return candidates

def part1(plot: list[list[str]]):
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
    if x == endX and y == endY:
      continue
    for X, Y, Dir, Score in genCandidates(plot, x, y, change, score):
      if (X, Y, Dir) not in visited and candidates[(X, Y, Dir)] > Score:
        candidates[(X, Y, Dir)] = Score
  end = min([(endX, endY, d, visited[(endX, endY, d)]) for d in [UP, DOWN, LEFT, RIGHT]], key=lambda x: x[3])
  print(f"lowest score: {end[3]}")
                      
def part2(plot: list[list[str]]):
  print(plot)

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  plot = f.read().splitlines()
  part1(plot) if part == "pt1" else part2(plot)
