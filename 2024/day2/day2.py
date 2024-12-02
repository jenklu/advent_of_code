import sys
from collections import defaultdict

def part1(filename: str):
  with open(filename, 'r') as f:
      safeCount = 0
      for line in f:
        split = list(map(int, line.split()))
        dir = ""
        for i in range(0, len(split) - 1):
          if i == 0:
            dir = "inc" if split[i+1] > split[i] else "dec"
          delta = split[i+1] - split[i]
          if delta == 0 or abs(delta) > 3:
            break
          if delta > 0 and dir == "dec":
            break
          if delta < 0 and dir == "inc":
            break
        else:
          safeCount += 1
      print(f"count of safe reports: {safeCount}")
        

def part2(left: list[int], right: list[int]):
  pass


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

if part == "pt1":
  part1(filename)
else:
  part2(left, right)

