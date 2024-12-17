import sys
from collections import defaultdict
from dataclasses import dataclass 
import re

@dataclass
class Coord:
  x: int
  y: int


def part1(bots: list[tuple[Coord, Coord]], maxX: int, maxY: int):
  endPos = defaultdict(lambda: 0)
  for bot in boys:
    endX, endY = (bot[0].x + 100 * bot[1].x) % maxX, (bot[0].y + 100 * bot[1].y) % maxY
    endPos[(endX, endY)] += 1
  quadLenX, quadLenY = maxX // 2, maxY // 2
  count = 1
  for startX, startY in [(0, 0), (0, quadLenY+1), (quadLenX+1, 0), (quadLenX+1, quadLenY+1)]:
    quadCount = 0
    for x in range(startX, startX + quadLenX):
      for y in range(startY, startY + quadLenY):
        quadCount += endPos[(x, y)]
    print(f"quad: {(startX, startY)}, count: {quadCount}")
    count *= quadCount
  print(f"count: {count}")
def part2(bots: list[tuple[Coord, Coord]], maxX: int, maxY: int):
  second = 0
  while second < 10000:
    botMap = defaultdict(lambda: '.')
    for bot in bots:
      if botMap[(bot[0].x, bot[0].y)] == '.':
        botMap[(bot[0].x, bot[0].y)] = 1
      else:
        botMap[(bot[0].x, bot[0].y)] += 1
    maxRunLen = 0
    s = ""
    for row in range(maxY):
      rowStr = "".join([str(botMap[(col, row)]) for col in range(maxX)])
      s += rowStr + "\n"
      splitCounts = [len(x) for x in rowStr.split('.')]
      maxRunLen = max(maxRunLen, max(splitCounts))
    if (second % 100) == 0:
      print(f"second: {second}")
    if maxRunLen >= 10: 
      print(f"candidate: {second}\n{s}")
    second, bots = second + 1, [(Coord((bot[0].x + bot[1].x) % maxX, (bot[0].y + bot[1].y) % maxY), Coord(bot[1].x, bot[1].y)) for bot in bots]

## main
print(sys.argv)
if len(sys.argv) != 4 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path> maxX,maxY")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]
maxes = sys.argv[3].split(',')
maxX, maxY = int(maxes[0]), int(maxes[1])

with open(filename, 'r') as f:
  totalCost = 0
  bots = []
  for line in f:
    vals = re.findall(r"[\-\d]+", line)
    bots.append(
      (Coord(int(vals[0]), int(vals[1])), Coord(int(vals[2]), int(vals[3])))
    )
  if part == "pt1":
    part1(bots, maxX, maxY)
  else:
    part2(bots, maxX, maxY)