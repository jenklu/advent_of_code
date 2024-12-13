import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Region:
  rows: dict[int, set[int]]
  columns: dict[int, set[int]]
  fences: dict[tuple[int, int], list[tuple[int, int]]]
  startX: int
  startY: int
  area: int
  perim: int

RIGHT, LEFT, DOWN, UP = (1, 0), (-1, 0), (0, 1), (0, -1)
seen = set()
def findRegion(farm: list[str], x: int, y: int, region: Region):
  if y < region.startY:
    region.startY = y
  if x < region.startX:
    region.startX = x
  region.rows[y].add(x)
  region.columns[x].add(y)
  region.area += 1
  seen.add((x, y))
  for delta in [RIGHT, LEFT, DOWN, UP]:
    nextX, nextY = x + delta[0], y + delta[1]
    if nextX in region.rows[nextY]:
      continue
    # if at a map border or nextX, nextY doesn't match, we need a fence between curr and next
    if not (0 <= nextX < len(farm[0]) and 0 <= nextY < len(farm)) or farm[nextY][nextX] != farm[y][x]:
      region.perim += 1
      region.fences[(x, y)].append(delta)
    else:
      findRegion(farm, nextX, nextY, region)

def part1(farm: list[str]):
  price = 0
  for y in range(len(farm)):
    for x in range(len(farm[0])):
      if (x, y) not in seen:
        region = Region(defaultdict(set), defaultdict(set), defaultdict(list), x, y, 0, 0)
        findRegion(farm, x, y, region)
        price += region.area * region.perim
  print(f"total price: {price}")
  print(f"len(seen): {len(seen)} len(farm) * len(farm[0]): {len(farm) * len(farm[0])}")


def countSides(region: Region): 
  sides = 0
  y, row = region.startY, region.rows[region.startY]
  while row:
    for x in row:
      if UP in region.fences[(x, y)] and UP not in region.fences[(x-1, y)]:
        sides += 1
      if DOWN in region.fences[(x, y)] and DOWN not in region.fences[(x-1, y)]:
        sides += 1
    # set up next iteration
    y += 1
    row = region.rows[y]
  # now do the vertical sides
  x, col = region.startX, region.columns[region.startX]
  while col:
    for y in col:
      if LEFT in region.fences[(x, y)] and LEFT not in region.fences[(x, y-1)]:
        sides += 1
      if RIGHT in region.fences[(x, y)] and RIGHT not in region.fences[(x, y-1)]:
        sides += 1
    # set up next iteration
    x += 1
    col = region.columns[x]
  return sides


def part2(farm: list[str]):
  price = 0
  for y in range(len(farm)):
    for x in range(len(farm[0])):
      if (x, y) not in seen:
        region = Region(defaultdict(set), defaultdict(set), defaultdict(list), x, y, 0, 0)
        findRegion(farm, x, y, region)
        sides = countSides(region)
        #print(f"region: {farm[y][x]} sides: {sides}")
        price += region.area * sides
  print(f"total price: {price}")


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
