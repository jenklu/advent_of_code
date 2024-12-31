import sys
def part1(keys: list[list[int]], locks: list[list[int]]):
  count = 0
  for lock in locks:
    for key in keys:  
      for i, k in enumerate(key):
        if k + lock[i] > 5:
          break
      else:
        count += 1
  print(f"unique pairs: {count}")

def part2(keys: list[list[int]], locks: list[list[int]]):
  print("Deliver the chronicle to Santa! But really, to yourself :)")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
  print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
  exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  lines = f.read().splitlines()
  keys, locks = [], []
  for y in range(0, len(lines), 8):
    item = []
    for x in range(len(lines[0])):
      item.append(sum([1 for y1 in range(y, y+7) if lines[y1][x] == "#"]) - 1)
    if lines[y][0] == "#":
      locks.append(item)
    else:
      keys.append(item)
  part1(keys, locks) if part == "pt1" else part2(keys, locks)
