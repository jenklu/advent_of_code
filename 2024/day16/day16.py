import sys
from math import inf
from collections import defaultdict

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
def part1(plot: list[list[str]]):
  visited = defaultdict(lambda: inf)
  candidates = [(0, 1, len(plot) - 2, RIGHT)]
  endX, endY = len(plot[0]) - 2, 1
  while candidates:
    score, x, y, change = candidates.pop()
    if visited[(x, y, change)] < score:
      # we already found a better way here, don't bother processing this
      continue
    visited[(x, y, change)] = score

    if x == endX and y == endY:
      continue
    for delta in UP, DOWN, LEFT, RIGHT:
      if delta == change:
        continue
      elif visited[(x, y, delta)] > score + 1000:
        candidates.append((score + 1000, x, y, delta))
    nextX, nextY = x + change[0], y + change[1]
    if (0 < nextX <= len(plot[0]) and 0 < nextY < len(plot) and plot[nextY][nextX] != '#'
        and score + 1 < visited[(nextX, nextY, change)]):
      candidates.append((score + 1, nextX, nextY, change))
  minScore = inf
  for direction in UP, DOWN, LEFT, RIGHT:
    minScore = min(minScore, visited[(endX, endY, direction)])
  print(f"lowest score: {minScore}")
                      
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
