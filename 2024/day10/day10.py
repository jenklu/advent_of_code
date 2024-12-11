import sys
import copy

memo = {}
def findEnds(startX: int, startY: int, topos: list[list[int]])->set[tuple[int, int]]:
  curr = topos[startY][startX]
  if curr == 9:
    return {(startX, startY)}
  reachable = set()
  right, left, down, up = (startX+1, startY), (startX-1, startY), (startX, startY+1), (startX, startY-1)
  for x, y in [right, left, down, up]:
    if 0 <= x < len(topos[0]) and 0 <= y < len(topos) and topos[y][x] == curr+1:
      if (x, y) in memo:
        reachable.update(memo[(x, y)])
      else:
        memo[(x, y)] = findEnds(x, y, topos)
        reachable.update(memo[(x, y)])
  return reachable

def part1(topos: list[list[int]], trailheads: list[tuple[int, int]]):
  score = 0
  for trailhead in trailheads:
    ends = findEnds(trailhead[0], trailhead[1], topos)
    score += len(ends)
  print(f"score: {score}")

def getScore(startX: int, startY: int, topos: list[list[int]])->int:
  curr = topos[startY][startX]
  if curr == 9:
    return 1
  score = 0
  right, left, down, up = (startX+1, startY), (startX-1, startY), (startX, startY+1), (startX, startY-1)
  for x, y in [right, left, down, up]:
    if 0 <= x < len(topos[0]) and 0 <= y < len(topos) and topos[y][x] == curr+1:
      if (x, y) in memo:
        score += memo[(x, y)]
      else:
        memo[(x, y)] = getScore(x, y, topos)
        score += memo[(x, y)]
  return score

def part2(topos: list[list[int]], trailheads: list[tuple[int, int]]):
  score = 0
  for trailhead in trailheads:
    score += getScore(trailhead[0], trailhead[1], topos)
  print(f"score: {score}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  topoMap = []
  for line in f:
    topoMap.append([int(x) for x in line.strip()])
  trailheads = []
  for y in range(len(topoMap)):
    for x in range(len(topoMap[0])):
      if topoMap[y][x] == 0:
        trailheads.append((x, y))
  if part == "pt1":
    part1(topoMap, trailheads)
  else:
    part2(topoMap, trailheads)
