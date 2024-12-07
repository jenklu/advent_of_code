import sys
from dataclasses import dataclass
from collections.abc import Callable

@dataclass
class Point:
  total: int
  s: str

def generatePart1Permutations(nums: list[Point]) -> list[Point]:
  if len(nums) <= 1:
    return nums
  rest = generatePart1Permutations(nums[:-1])
  perms = []
  for val in rest:
    perms.append(Point(nums[-1].total + val.total, f"{val.s}+{nums[-1].s}"))
    perms.append(Point(nums[-1].total * val.total, f"{val.s}*{nums[-1].s}"))
  return perms

def countTotal(resultAndNums: list[tuple[int, list[Point]]], permutationGenerator: Callable[[list[Point]], list[Point]]): 
  total = 0
  for resultAndNum in resultAndNums:
    generated = permutationGenerator(resultAndNum[1])
    print(f"goal: {resultAndNum[0]} generated: {generated}")
    if resultAndNum[0] in list(map(lambda x: x.total, generated)):
      total += resultAndNum[0]
  print(f"total: {total}")

def part1(resultAndNums: list[tuple[int, list[Point]]]):
  countTotal(resultAndNums, generatePart1Permutations)

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  resultAndNums = []
  for line in f:
    initialSplit = line.split(":")
    equation = list(map(lambda x: Point(int(x), x), initialSplit[1].split()))
    resultAndNums.append((int(initialSplit[0]), equation))
  if part == "pt1":
    part1(resultAndNums)
  else:
    part2(resultAndNums)
