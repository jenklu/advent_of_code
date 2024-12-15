import sys
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class Coord:
  x: int
  y: int
  cost: int

@dataclass
class Machine:
  prize: Coord
  cost3: Coord
  cost1: Coord

def findMachineCost(m: Machine) -> int:
  cheaps = [Coord(m.prize.x - (m.cost1.x * i), m.prize.y - (m.cost1.y * i), i) for i in range(1, 101)]
  priceys =  [Coord(m.cost3.x*i, m.cost3.y*i, 3*i) for i in range(1, 101)]
  minCost = 0
  for cheap in cheaps:
    if (cheap.x, cheap.y) == (0, 0) and (minCost == 0 or cheap.cost < minCost):
      minCost = cheap.cost
      continue
    elif cheap.x < 0 or cheap.y < 0:
      continue
    for pricey in priceys:
      cost = cheap.cost + pricey.cost
      if (pricey.x, pricey.y) == (cheap.x, cheap.y) and (minCost == 0 or cost < minCost):
        minCost = cost
      elif (pricey.x, pricey.y) == (m.prize.x, m.prize.y) and (minCost == 0 or pricey.cost < minCost):
        minCost = pricey.cost
  return minCost

def part1(machines: list[Machine]):
  totalCost = 0
  for machine in machines:
    totalCost += findMachineCost(machine)
  print(f"totalCost: {totalCost}")

def part2(machines: list[Machine]):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  lines = f.read().splitlines()
  machines = []
  for i in range(0, len(lines), 4):
    buttonRe = r"(?<=\+)[0-9]*"
    cost3raw, cost1raw = re.findall(buttonRe, lines[i]), re.findall(buttonRe, lines[i+1])
    prizeRaw = re.findall(r"(?<=\=)[0-9]*", lines[i+2])
    machines.append(Machine(
      Coord(int(prizeRaw[0]), int(prizeRaw[1]), 0),
      Coord(int(cost3raw[0]), int(cost3raw[1]), 0),
      Coord(int(cost1raw[0]), int(cost1raw[1]), 0),
    ))
  if part == "pt1":
    part1(machines)
  else:
    part2(machines)
