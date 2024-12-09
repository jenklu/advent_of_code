import sys
import copy
from collections import defaultdict

def findAntinodes(antennas: list[tuple[int, int]], nodeType: str, limitX: int, limitY: int) -> set[tuple[int, int]]:
  antinodes = set()
  for i in range(len(antennas)):
    for j in range(len(antennas)):
      if i == j:
        continue
      a0, a1 = antennas[i], antennas[j]
      deltaX, deltaY = a0[0] - a1[0], a0[1] - a1[1]
      # These functions come from taking the displacement between antenna0 and antenna1. To find the
      # antinode twice as far from a0 as a1, you just add the displacement between a1 and a0 and add
      # it to a1. The inversion of that (i.e. swapping a0 and a1) explains why we negate deltaX and
      # deltaY for antinode0.
      antinode0 = (a0[0] + deltaX, a0[1] + deltaY)
      antinode1 = (a1[0] - deltaX, a1[1] - deltaY)
      if 0 <= antinode0[0] < limitX and 0 <= antinode0[1] < limitY:
        antinodes.add(antinode0)
      if 0 <= antinode1[0] < limitX and 0 <= antinode1[1] < limitY:
        antinodes.add(antinode1)
  return antinodes

def part1(mapInput: list[list[str]]) -> tuple[int, int, set[tuple[int, int]]]:
  antennas = defaultdict(list)
  mapWidth, mapHeight = len(mapInput[0]), len(mapInput)
  for y in range(mapHeight):
    for x in range(mapWidth):
      el = mapInput[y][x]
      if el != ".":
        antennas[el].append((x, y))
  antinodes = set()
  for nodeType, antennas in antennas.items():
    antinodes.update(findAntinodes(antennas, nodeType, mapWidth, mapHeight))
  print(f"number of unique antinodes: {len(antinodes)}\nantinodes: {antinodes}")

def findAntinodes2(antennas: list[tuple[int, int]], nodeType: str, limitX: int, limitY: int) -> set[tuple[int, int]]:
  antinodes = set()
  for i in range(len(antennas)):
    for j in range(len(antennas)):
      if i == j:
        continue
      a0, a1 = antennas[i], antennas[j]
      deltaX, deltaY = a0[0] - a1[0], a0[1] - a1[1]
      plusAntinode = (a0[0], a0[1])
      minusAntinode = (a0[0] - deltaX, a0[1] - deltaY)
      while True:
        added = False
        if 0 <= plusAntinode[0] < limitX and 0 <= plusAntinode[1] < limitY:
          antinodes.add(plusAntinode)
          added = True
        if 0 <= minusAntinode[0] < limitX and 0 <= minusAntinode[1] < limitY:
          antinodes.add(minusAntinode)
          added = True
        if not added:
          break
        plusAntinode = (plusAntinode[0] + deltaX, plusAntinode[1] + deltaY)
        minusAntinode = (minusAntinode[0] - deltaX, minusAntinode[1] - deltaY)
  return antinodes

def part2(mapInput: list[list[str]]):
  antennas = defaultdict(list)
  mapWidth, mapHeight = len(mapInput[0]), len(mapInput)
  for y in range(mapHeight):
    for x in range(mapWidth):
      el = mapInput[y][x]
      if el not in "#.":
        antennas[el].append((x, y))
  antinodes = set()
  for nodeType, antennas in antennas.items():
    antinodes.update(findAntinodes2(antennas, nodeType, mapWidth, mapHeight))
  print(f"number of unique antinodes: {len(antinodes)}\nantinodes: {antinodes}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  mapInput = [list(line) for line in f.read().splitlines()]
  if part == "pt1":
    part1(mapInput)
  else:
    part2(mapInput)
