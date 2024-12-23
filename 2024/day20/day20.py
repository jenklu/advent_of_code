import sys
from collections import namedtuple
from math import inf

Coord = namedtuple("Coord", ['x', 'y'])

def findDistances(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int)->dict[Coord, int]:
  cands = {start}
  visited, depth = {}, 0
  while cands:
    nextCands = set()
    for c in cands:
      visited[c] = depth
      for nextX, nextY in [(c.x, c.y+1), (c.x, c.y-1), (c.x+1, c.y), (c.x-1, c.y)]:
        nextC = Coord(nextX, nextY)
        # we know all the edges are obstacles, so skip them
        if 0 < nextX < maxX and 0 < nextY < maxY and nextC not in visited and nextC not in obstacles:
          nextCands.add(nextC)
    cands, depth = nextCands, depth+1 
  return visited

def findCheats(obstacles: set[Coord], toCheck: dict[Coord, int], curr: Coord, dist: int, maxDist: int):
  toCheck[curr] = dist
  if dist >= maxDist:
    return
  for nxt in [Coord(curr.x+1, curr.y), Coord(curr.x-1, curr.y), Coord(curr.x, curr.y+1), Coord(curr.x, curr.y-1)]:
    if not toCheck.get(nxt, inf) > dist + 1:
      continue
    findCheats(obstacles, toCheck, nxt, dist + 1, maxDist)

def handler(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int, maxDist: int):
  visited = findDistances(obstacles, end, start, maxX, maxY)
  #printPlot(obstacles, visited, start, end, maxX, maxY)
  count = 0
  for i, (point, score) in enumerate(visited.items()):
    if score < 100:
      continue
    cheatsToCheck = {}
    findCheats(obstacles, cheatsToCheck, point, 0, maxDist)
    for cheatLoc, cheatDist in cheatsToCheck.items():
      if not cheatLoc in visited:
        continue
      improvement = score - (visited[cheatLoc] + cheatDist)
      if improvement >= 100:
        count += 1
    if i % 1000 == 0:
      print(f"processed {100 * i / len(visited)}%")
  print(f"count: {count}")

def printPlot(obstacles: set[Coord], visited: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int):
  for y in range(maxY+1):
    s = ""
    for x in range(maxX+1):
      if Coord(x, y) == start:
        s += "S  "
      elif Coord(x, y) == end:
        s += "E  "
      elif Coord(x, y) in obstacles or x == 0 or x == maxX:
        s += "#  "
      elif Coord(x, y) in visited:
        val = str(visited[Coord(x, y)])
        s += val + ' ' * (3 - len(val))
      else:
        s += "."
    if y == 0 or y == maxY:
      s = "#" * (maxX + 1) * 3
    print(s)

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
  if part == "pt1":
    handler(obstacles, start, end, maxX, maxY, 2)
  else:
    handler(obstacles, start, end, maxX, maxY, 20)
