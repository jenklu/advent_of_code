import sys
from collections import namedtuple
from math import inf

Coord = namedtuple("Coord", ['x', 'y'])

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
DIR_MAP = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}

def dist(first: Coord, second: Coord):
  return abs(first.x - second.x) + abs(first.y - second.y)

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

def findPaths(curr: Coord, end: Coord, path: str, plot: set[Coord])->list[str]:
  if curr == end:
    return [path + "A"]
  paths = []
  for direction in [UP, DOWN, LEFT, RIGHT]:
    nextX, nextY = curr.x + direction[0], curr.y + direction[1]
    nxt = Coord(nextX, nextY)
    if nxt in plot and dist(nxt, end) < dist(curr, end):
      paths.extend(findPaths(nxt, end, path+DIR_MAP[direction], plot))
  return paths

memo = {}
def findComponentScore(c1, c2, itersLeft)->str:
  if (c1+c2, itersLeft) in memo:
    return memo[(c1+c2, itersLeft)]
  paths = findPaths(DIRPAD_MAP[c1], DIRPAD_MAP[c2], "", DIRPAD)
  if itersLeft == 0:
    memo[(c1+c2, 0)] = len(paths[0])
    return memo[(c1+c2, 0)]
  minScore = inf
  for path in paths:
    path = "A" + path
    score = 0
    for i in range(0, len(path) - 1):
      score += findComponentScore(path[i], path[i+1], itersLeft-1)
    minScore = min(score, minScore)
  memo[(c1 + c2, itersLeft)] = minScore
  return minScore

def findCodeScores(codes: list[str], numDirpads: int):
  total = 0
  for code in codes:
    coordsList = [codeToCoord("A")] + [codeToCoord(c) for c in code]
    paths = [""]
    for i in range(len(coordsList) - 1):
      componentPaths = findPaths(coordsList[i], coordsList[i+1], "", NUMPAD)
      paths = [curr + componentPath for curr in paths for componentPath in componentPaths]
    minScore = inf
    for path in paths:
      path = "A" + path
      score = 0
      for i in range(len(path)-1):
        score += findComponentScore(path[i], path[i+1], numDirpads - 1)
      minScore = min(score, minScore)
    codeScore = minScore * int(code[:3])
    total += codeScore
    print(f"code {code}: minScore: {minScore} = score ({codeScore})")
  print(f"total: {total} - len(memo): {len(memo)}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  codes = f.read().splitlines() 
  findCodeScores(codes, 2) if part == "pt1" else findCodeScores(codes, 25)
