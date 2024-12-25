import sys
from collections import namedtuple
from math import inf

Coord = namedtuple("Coord", ['x', 'y'])

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIR_MAP = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}

def dist(first: Coord, second: Coord):
  return abs(first.x - second.x) + abs(first.y - second.y)

def findPaths(curr: Coord, locs: list[Coord], path: str, plot: set[Coord], minPathLen: int=inf):
  if len(path) > minPathLen:
    return []
  if not locs:
    return [path]
  end = locs[0]
  if curr == end:
    return findPaths(curr, locs[1:], path + "A", plot)
  paths = []
  for direction in [UP, DOWN, LEFT, RIGHT]:
    nextX, nextY = curr.x + direction[0], curr.y + direction[1]
    nxt = Coord(nextX, nextY)
    if nxt in plot and dist(nxt, end) < dist(curr, end):
      paths.extend(findPaths(nxt, locs, path+DIR_MAP[direction], plot))
  return paths

def codeToCoord(c: str)->Coord:
  if c == '0':
    return Coord(1, 3)
  elif c == 'A':
    return Coord(2, 3)
  c = int(c) - 1 # -1 to zero index
  x = c % 3
  y = 2 - c // 3 # invert to start from the top
  return Coord(x, y)
NUMPAD = set([codeToCoord(c) for c in "0123456789A"])

DIRPAD_MAP = {
  "^": Coord(1, 0),
  "A": Coord(2, 0),
  "<": Coord(0, 1),
  "v": Coord(1, 1),
  ">": Coord(2, 1),
}
DIRPAD = set([DIRPAD_MAP[c] for c in "v^<>A"])

def part1(codes: list[str]):
  total = 0
  for code in codes:
    coords = [codeToCoord(c) for c in code]
    minPath = inf
    for path in findPaths(codeToCoord("A"), coords, "", NUMPAD):
      path1Coords = [DIRPAD_MAP[c] for c in path]
      for secondPath in findPaths(DIRPAD_MAP["A"], path1Coords, "", DIRPAD):
        path2Coords = [DIRPAD_MAP[c] for c in secondPath]
        minFound = min(findPaths(DIRPAD_MAP["A"], path2Coords, "", DIRPAD), key=len)
        minPath = min(len(minFound), minPath)
    codeScore = minPath * int(code[:3])
    print(f"code: {code} minPath: {minPath} score: {codeScore}")
    total += codeScore
  print(f"total: {total}")

def pathScore(path: str):
  score = 0
  # All paths end in "A", so the robot is always at "A" at the beginning of a path. So to calculate
  # the true score for a path, we add a prefix of "A" to the path
  path = 'A' + path
  for i, c in enumerate(path[1:]):
    score += dist(DIRPAD_MAP[c], DIRPAD_MAP[path[i-1]]) + 1
  return score

def getNextPathsToCheck(paths: list[list[Coord]]):
  # minScore, nextPaths = inf, set()
  # for path in paths:
  #   score = pathScore(path)
  #   if score == minScore:
  #     coords = [DIRPAD_MAP[c] for c in path]
  #     nextPaths.update(findPaths(DIRPAD_MAP["A"], coords, "", DIRPAD, minScore))
  #   elif score < minScore:
  #     minScore = score
  #     coords = [DIRPAD_MAP[c] for c in path]
  #     nextPaths = set(findPaths(DIRPAD_MAP["A"], coords, "", DIRPAD, minScore))
  # return nextPaths
  nextPaths = []
  for path in paths:
    pathCoords = [DIRPAD_MAP[c] for c in path]
    nextPaths.extend(findPaths(DIRPAD_MAP["A"], pathCoords, "", DIRPAD))
  return nextPaths

def part2(codes: list[str]):
  total = 0
  for code in codes:
    coordsList = [codeToCoord(c) for c in code]
    paths = findPaths(codeToCoord("A"), coordsList, "", NUMPAD)
    for i in range(25):
      print(f"code: {code} i: {i} len(paths): {len(paths)}")
      paths = getNextPathsToCheck(paths)
    minPath = min(paths, key=len) 
    codeScore = len(minPath) * int(code[:3])
    print(f"code ({code}) *  len(minPath) ({len(minPath)}) = score ({codeScore})")
    total += codeScore
  print(f"total: {total}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  codes = f.read().splitlines() 
  part1(codes) if part == "pt1" else part2(codes)