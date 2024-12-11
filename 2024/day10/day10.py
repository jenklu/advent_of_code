import sys
import copy
memo = {}
def findEnds(x: int, y: int, topos: list[list[int]])->set[tuple[int, int]]:
  curr = topos[y][x]
  if curr == 9:
    return {(x, y)}
  reachable = set()
  if x+1 < len(topos[0]) and topos[y][x+1] == curr+1:
    if (x+1, y) in memo:
      reachable.update(memo[(x+1, y)])
    else:
      memo[(x+1, y)] = findEnds(x+1, y, topos)
      reachable.update(memo[(x+1, y)])
  if x-1 >= 0 and topos[y][x-1] == curr+1:
    if (x-1, y) in memo:
      reachable.update(memo[(x-1, y)])
    else:
      memo[(x-1, y)] = findEnds(x-1, y, topos)
      reachable.update(memo[(x-1, y)])
  if y+1 < len(topos) and topos[y+1][x] == curr+1:
    if (x, y+1) in memo:
      reachable.update(memo[(x, y+1)])
    else:
      memo[(x, y+1)] = findEnds(x, y+1, topos)
      reachable.update(memo[(x, y+1)])
  if y-1 >= 0 and topos[y-1][x] == curr+1:
    if (x, y-1) in memo:
      reachable.update(memo[(x, y-1)])
    else:
      memo[(x, y-1)] = findEnds(x, y-1, topos)
      reachable.update(memo[(x, y-1)])
  return reachable

def part1(topos: list[list[int]]):
  starts, ends = [], []
  for y in range(len(topos)):
    for x in range(len(topos[0])):
      if topos[y][x] == 0:
        starts.append((x, y))
  score = 0
  for trailHead in starts:
    ends = findEnds(trailHead[0], trailHead[1], topos)
    print(f"trailHead {trailHead}, len(ends): {len(ends)}")
    score += len(ends)
  print(f"score: {score}")

def part2(topos: list[list[int]]):
  pass

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
  print(len(topoMap))
  if part == "pt1":
    part1(topoMap)
  else:
    part2(fileMap)
