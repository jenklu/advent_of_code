import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Region:
  rows: dict[int, set[int]]
  startY: int

seen = set()
def findRegion(farm: list[str], x: int, y: int, region: Region):
  if y < region.startY:
    region.startY = y
  region.rows[y].add(x)
  seen.add((x, y))
  for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    nextX, nextY = x + dir[0], y + dir[1]
    if (nextX, nextY) in seen or not (0 <= nextX < len(farm[0]) and 0 <= nextY < len(farm)):
      continue
    elif farm[nextY][nextX] == farm[y][x]:
      findRegion(farm, nextX, nextY, region)

def processRegion(region: Region):
  y = region.startY
  lastRow, row, nextRow = set(), region.rows[y], region.rows[y+1]
  area, perim = 0, 0
  while row:
    for val in row:
      area += 1
      if (val - 1) not in row:
        # fence to the left
        perim += 1
      if (val + 1) not in row:
        # fence to the left
        perim += 1
      if val not in lastRow:
        # fence on top
        perim += 1
      if val not in nextRow:
        # fence on bottom
        perim += 1
    # set up next iteration
    lastRow = row
    y += 1
    row, nextRow = region.rows[y], region.rows[y+1]
  return area, perim


def part1(farm: list[str]):
  price = 0
  for y in range(len(farm)):
    for x in range(len(farm[0])):
      if (x, y) not in seen:
        region = Region(defaultdict(set), y)
        findRegion(farm, x, y, region)
        area, perim = processRegion(region)
        price += area * perim
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
