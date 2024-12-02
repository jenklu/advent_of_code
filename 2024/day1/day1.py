import sys
from collections import defaultdict

def part1(left: list[int], right: list[int]):
  left.sort()
  right.sort()
  dist = 0
  for i in range(len(left)):
    dist += abs(left[i] - right[i])

  print(f"total distance: {dist}")


def part2(left: list[int], right: list[int]):
  counts = defaultdict(lambda: 0)
  for n in right:
    counts[n] += 1
  score = 0
  for n in left:
    score += n * counts[n]
  print(f"total similarity score: {score}")


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

right, left = [], []
with open(filename, 'r') as f:
    for line in f:
      split = line.split()
      left.append(int(split[0]))
      right.append(int(split[1]))

if part == "pt1":
  part1(left, right)
else:
  part2(left, right)

