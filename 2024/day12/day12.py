import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Region:
  fences: dict[tuple[int, int], list[tuple[int, int]]]
  area: int
  perim: int

RIGHT, LEFT, DOWN, UP = (1, 0), (-1, 0), (0, 1), (0, -1)
seen = set()
def findRegion(farm: list[str], x: int, y: int, region: Region):
  region.area += 1
  region.fences[(x, y)] = []
  seen.add((x, y))
  for delta in [RIGHT, LEFT, DOWN, UP]:
    nextX, nextY = x + delta[0], y + delta[1]
    if (nextX, nextY) in region.fences:
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
        region = Region({}, 0, 0)
        findRegion(farm, x, y, region)
        price += region.area * region.perim
  print(f"total price: {price}")

def countSides(region: Region): 
  sides = 0
  for (x, y), fences in region.fences.items():
    if UP in fences and ((x-1, y) not in region.fences or UP not in region.fences[(x-1, y)]):
      sides += 1
    if DOWN in fences and ((x-1, y) not in region.fences or DOWN not in region.fences[(x-1, y)]):
      sides += 1
    if LEFT in fences and ((x, y-1) not in region.fences or LEFT not in region.fences[(x, y-1)]):
      sides += 1
    if RIGHT in fences and ((x, y-1) not in region.fences or RIGHT not in region.fences[(x, y-1)]):
      sides += 1
  return sides


def part2(farm: list[str]):
  price = 0
  for y in range(len(farm)):
    for x in range(len(farm[0])):
      if (x, y) not in seen:
        region = Region({}, 0, 0)
        findRegion(farm, x, y, region)
        price += region.area * countSides(region)
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
