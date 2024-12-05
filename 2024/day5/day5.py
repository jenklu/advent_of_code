import sys
from collections import defaultdict
from io import IOBase


def isValidUpdate(rules: dict, update: list[str]) -> bool:
  for i in range(len(update)):
    for j in range(i):
      if update[j] in rules[update[i]]:
        return False
  return True

def part1(rules: dict, updates: list[list[str]]):
  result = 0
  for update in updates:
    if isValidUpdate(rules, update):
      result += int(update[len(update) // 2])
  print(f"result: {result}")


def part2(rules: list[str], updates: list[list[str]]):
  pass
  #print(f"result: {result}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  rules = defaultdict(set)
  updates = []
  for line in f:
    if "|" in line:
      split = line.rstrip().split("|")
      rules[split[0]].add(split[1])
    elif line.rstrip() != "":
      updates.append(line.rstrip().split(","))
  if part == "pt1":
    part1(rules, updates)
  else:
    part2(rules, updates)

