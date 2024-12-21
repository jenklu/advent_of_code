import sys
from collections import namedtuple
from math import inf

Coord = namedtuple("Coord", ['x', 'y'])

def part1(obstacles: set[Coord], gridSize: int):
  cands = {Coord(0, 0)}
  visited, depth = {}, 0
  while cands:
    nextCands = set()
    for c in cands:
      visited[c] = depth
      for nextX, nextY in [(c.x, c.y+1), (c.x, c.y-1), (c.x+1, c.y), (c.x-1, c.y)]:
        nextC = Coord(nextX, nextY)
        if (0 <= nextX <= gridSize and 0 <= nextY <= gridSize and
          nextC not in visited and nextC not in obstacles):
          nextCands.add(nextC)
    cands, depth = nextCands, depth+1
  print(f"answer: {visited[Coord(gridSize, gridSize)]}")

def part2(obstacles: set[Coord], gridSize: int):
  print(obstacles)

## main
print(sys.argv)
if len(sys.argv) not in [3, 4] or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename, gridSize = sys.argv[1], sys.argv[2], 70
if len(sys.argv) == 4:
  gridSize = int(sys.argv[3])
with open(filename, 'r') as f:
  obstacles = set()
  for line in f:
    split = line.split(',')
    obstacles.add(Coord(int(split[0]), int(split[1])))
    if len(obstacles) == 1024 and part == "pt1":
      break
  part1(obstacles, gridSize) if part == "pt1" else part2(plot)
