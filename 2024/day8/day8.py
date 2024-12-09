import sys
import copy
from collections import defaultdict
from collections.abc import Callable

def findAntinodesPart1(antennas: list[tuple[int, int]], limitX: int, limitY: int, antinodes: set[tuple[int, int]]) -> set[tuple[int, int]]:
  for i in range(len(antennas)):
    for j in range(len(antennas)):
      if i == j:
        continue
      a0, a1 = antennas[i], antennas[j]
      deltaX, deltaY = a0[0] - a1[0], a0[1] - a1[1]
      # To find antinode0 2x as far from a1 as a0, you find displacement btw a0 and a1 & add it to
      # a0. To find antinode1, negating deltaX/deltaY => adding to a1 effectively swaps which point is a0/a1.
      antinode0 = (a0[0] + deltaX, a0[1] + deltaY)
      antinode1 = (a1[0] - deltaX, a1[1] - deltaY)
      if 0 <= antinode0[0] < limitX and 0 <= antinode0[1] < limitY:
        antinodes.add(antinode0)
      if 0 <= antinode1[0] < limitX and 0 <= antinode1[1] < limitY:
        antinodes.add(antinode1)
  return antinodes

def findAntinodesPart2(antennas: list[tuple[int, int]], limitX: int, limitY: int, antinodes: set[tuple[int, int]]):
  for i in range(len(antennas)):
    for j in range(len(antennas)):
      if i == j:
        continue
      a0, a1 = antennas[i], antennas[j]
      deltaX, deltaY = a0[0] - a1[0], a0[1] - a1[1]
      plusAntinode = (a0[0], a0[1])
      minusAntinode = (a0[0] - deltaX, a0[1] - deltaY)
      while True:
        onMap = False
        # Just follow the slope line positive/negative until we go off the map
        if 0 <= plusAntinode[0] < limitX and 0 <= plusAntinode[1] < limitY:
          antinodes.add(plusAntinode)
          onMap = True
        if 0 <= minusAntinode[0] < limitX and 0 <= minusAntinode[1] < limitY:
          antinodes.add(minusAntinode)
          onMap = True
        if not onMap:
          break
        plusAntinode = (plusAntinode[0] + deltaX, plusAntinode[1] + deltaY)
        minusAntinode = (minusAntinode[0] - deltaX, minusAntinode[1] - deltaY)

def handler(mapInput: list[list[str]], findAntinodes: Callable):
  antennas = defaultdict(list)
  mapWidth, mapHeight = len(mapInput[0]), len(mapInput)
  for y in range(mapHeight):
    for x in range(mapWidth):
      el = mapInput[y][x]
      if el != ".":
        antennas[el].append((x, y))
  antinodes = set()
  for antennas in antennas.values():
    findAntinodes(antennas, mapWidth, mapHeight, antinodes)
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
    handler(mapInput, findAntinodesPart1)
  else:
    handler(mapInput, findAntinodesPart2)
