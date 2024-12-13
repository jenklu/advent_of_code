import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Region:
  rows: dict[int, set[int]]
  startY: int
  area: int
  perim: int

seen = set()
def findRegion(farm: list[str], x: int, y: int, region: Region):
  if y < region.startY:
    region.startY = y
  region.rows[y].add(x)
  region.area += 1
  seen.add((x, y))
  for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    nextX, nextY = x + dir[0], y + dir[1]
    if nextX in region.rows[nextY]:
      continue
    # if at a map border or nextX, nextY doesn't match, we need a fence between curr and next
    if not (0 <= nextX < len(farm[0]) and 0 <= nextY < len(farm)) or farm[nextY][nextX] != farm[y][x]:
      region.perim += 1
    else:
      findRegion(farm, nextX, nextY, region)

def part1(farm: list[str]):
  price = 0
  for y in range(len(farm)):
    for x in range(len(farm[0])):
      if (x, y) not in seen:
        region = Region(defaultdict(set), y, 0, 0)
        findRegion(farm, x, y, region)
        price += region.area * region.perim
  print(f"total price: {price}")

def part2(farm: list[str]):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  farm = f.read().splitlines()
  if part == "pt1":
    part1(farm)
  else:
    part2(farm)
