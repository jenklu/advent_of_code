import sys
from collections import namedtuple, defaultdict
from math import inf
from copy import copy
Coord = namedtuple("Coord", ['x', 'y'])

def findMinPath(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int)->dict[Coord, int]:
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

def part1(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int):
  total, baseline = 0, findMinPath(obstacles, start, end, maxX, maxY)[end]
  for counter, obstacle in enumerate(obstacles):
    testSet = copy(obstacles)
    testSet.remove(obstacle)
    res = findMinPath(testSet, start, end, maxX, maxY)[end]
    if baseline - res >= 100:
      total += 1
    if counter % 100 == 0:
      print(f"{100 * counter / len(obstacles)}% done")
  print(f"total: {total}")

def plot(obstacles: set[Coord], visited: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int):
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

def findCheats(obstacles: set[Coord], scores: dict[Coord, int], toCheck: dict[Coord, int], curr: Coord, dist: int):
  toCheck[curr] = dist
  for nxt in [Coord(curr.x+1, curr.y), Coord(curr.x-1, curr.y), Coord(curr.x, curr.y+1), Coord(curr.x, curr.y-1)]:
    if not toCheck.get(nxt, inf) > dist + 1:
      continue
    if dist <= 19:
      findCheats(obstacles, scores, toCheck, nxt, dist + 1)
    # elif nxt in scores:
      # toCheck[nxt] = dist + 1
    # if nxt in obstacles and dist < 19 and nxt not in obstSeen:
    #   obstSeen.add(nxt)
    #   findCheats(obstacles, scores, obstSeen, toCheck, nxt, dist+1)
    #   # for cheat, dist in cheats.items():
    #   #   if toCheck.get(cheat, inf) > dist + 1:
    #   #     toCheck[cheat] = dist + 1
    # elif nxt in scores and toCheck.get(nxt, inf) > dist + 1:
    #   toCheck[nxt] = dist + 1

def part2(obstacles: set[Coord], start: Coord, end: Coord, maxX: int, maxY: int):
  visited = findMinPath(obstacles, end, start, maxX, maxY)
  plot(obstacles, visited, start, end, maxX, maxY)
  #cheatMap = defaultdict(lambda: 0)
  count = 0
  for i, (point, score) in enumerate(visited.items()):
    if score < 100:
      continue
    cheatsToCheck = {}
    findCheats(obstacles, visited, cheatsToCheck, point, 0)
    for cheatLoc, cheatDist in cheatsToCheck.items():
      if not cheatLoc in visited:
        continue
      improvement = score - (visited[cheatLoc] + cheatDist)
      if improvement >= 100:
        #cheatMap[improvement] += 1
        count += 1
    if i % 50 == 0:
      print(f"processed {100 * i / len(visited)}%")
  print(f"count: {count}")
  # for improvement in sorted(cheatMap):
  #   print(f"- There are {cheatMap[improvement]} cheats that save {improvement}")
        
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
