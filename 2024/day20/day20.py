import sys
from collections import namedtuple
from math import inf
from copy import copy
Coord = namedtuple("Coord", ['x', 'y'])

def findMinPath(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int)->int:
  cands = {start}
  visited, depth = {}, 0
  while cands:
    nextCands = set()
    for c in cands:
      visited[c] = depth
      if c == end:
        return visited[end]
      for nextX, nextY in [(c.x, c.y+1), (c.x, c.y-1), (c.x+1, c.y), (c.x-1, c.y)]:
        nextC = Coord(nextX, nextY)
        # we know all the edges are obstacles, so skip them
        if 0 < nextX < maxX and 0 < nextY < maxY and nextC not in visited and nextC not in obstacles:
          nextCands.add(nextC)
    cands, depth = nextCands, depth+1 

def part1(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int):
  total, baseline = 0, findMinPath(obstacles, start, end, maxX, maxY)
  for counter, obstacle in enumerate(obstacles):
    testSet = copy(obstacles)
    testSet.remove(obstacle)
    res = findMinPath(testSet, start, end, maxX, maxY)
    if baseline - res >= 100:
      total += 1
    if counter % 100 == 0:
      print(f"{100 * counter / len(obstacles)}% done")
  print(f"total: {total}")

def part2(obstacles: set[Coord], start: Coord, end: Coord):
  pass

## main
print(sys.argv)
if len(sys.argv) not in [3, 4] or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]
with open(filename, 'r') as f:
  obstacles, start, end = set(), None, None
  lines = f.read().splitlines()
  maxX, maxY = len(lines[0]) - 1, len(lines) - 1
  # we know all the edges are obstacles, so just pretend the edges don't exist
  for y, line in enumerate(lines):
    if y == 0 or y == maxY:
      continue
    for x in range(len(line)):
      if x == 0 or x == maxX:
        continue
      if line[x] == '#':
        obstacles.add((x, y))
      elif line[x] == 'S':
        start = Coord(x, y)
      elif line[x] == 'E':
        end = Coord(x, y)
  part1(obstacles, start, end, maxX, maxY) if part == "pt1" else part2(obstacles, start, end, maxX, maxY)
