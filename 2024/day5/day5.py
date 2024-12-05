import sys
from collections import defaultdict
from io import IOBase
from functools import cmp_to_key


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

def part2(rules: dict, updates: list[list[str]]):
  result = 0
  def compareItems(item1: str, item2: str) -> int:
    if item2 in rules[item1]:
      return -1
    elif item1 in rules[item2]:
      return 1
    return 0
  for update in updates:
    if not isValidUpdate(rules, update):
      update.sort(key=cmp_to_key(compareItems))
      result += int(update[len(update) // 2])

  print(f"result: {result}")

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

