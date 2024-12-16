import sys
from dataclasses import dataclass
import re
import math

@dataclass
class Coord:
  x: int
  y: int

@dataclass
class Machine:
  prize: Coord
  cost3: Coord
  cost1: Coord

# A system of equations is defined by (for x and y): machine.prize = machine.cost1 + machine.cost3
# If the direction of movement for cost1 and cost3 are the same (i.e equivalent slopes), then (if
# there's a solution, which we can tell by if prize is on that line), we return whichever of cost1,
# cost3 has cheaper cost per distance. Otherwise, we have 2 linear equations w/ 2 unknowns, which is
# guaranteed to have exactly 1 solution. The solution only "counts" if x,y are +ive integers, so
# double-check the solution is actually right when rounding to ints
def findSolution(m: Machine) -> int:
  # Check if the lines are on the same slope
  if m.prize.y / m.prize.x == m.cost3.y / m.cost3.x == m.cost1.x / m.cost1.y:
    return 3 * m.prize.x / m.cost1.x if m.cost3.x > 3 * m.cost1.x else m.prize.x / m.cost3.x
  # Hand-derived solution to the system of equations
  cost1presses = (m.prize.y - (m.cost3.y * m.prize.x / m.cost3.x)) / (m.cost1.y - (m.cost3.y * m.cost1.x / m.cost3.x))
  if cost1presses < 0:
    return 0
  cost3presses = (m.prize.x - (m.cost1.x * cost1presses)) / m.cost3.x
  if cost3presses < 0:
    return 0
  cost1presses, cost3presses = round(cost1presses), round(cost3presses)
  if not (cost3presses * m.cost3.x + cost1presses * m.cost1.x == m.prize.x and
          cost3presses * m.cost3.y + cost1presses * m.cost1.y == m.prize.y):
    return 0
  return cost1presses + 3 * cost3presses

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  totalCost = 0
  lines = f.read().splitlines()
  for i in range(0, len(lines), 4):
    buttonRe = r"(?<=\+)[0-9]*"
    cost3raw, cost1raw = re.findall(buttonRe, lines[i]), re.findall(buttonRe, lines[i+1])
    prizeRaw = re.findall(r"(?<=\=)[0-9]*", lines[i+2])
    prize = Coord(int(prizeRaw[0]), int(prizeRaw[1]))
    if part == "pt2":
      prize.x, prize.y = prize.x + 10000000000000, prize.y + 10000000000000
    totalCost += findSolution(Machine(prize,
      Coord(int(cost3raw[0]), int(cost3raw[1])),
      Coord(int(cost1raw[0]), int(cost1raw[1])),
    ))
  print(f"totalCost: {totalCost}")
