import sys

def isSafeLine(split: str) -> tuple[bool, int]:
  dir = ""
  for i in range(0, len(split) - 1):
    if i == 0:
      dir = "inc" if split[i+1] > split[i] else "dec"
    delta = split[i+1] - split[i]
    if delta == 0 or abs(delta) > 3:
      return (False, i)
    if delta > 0 and dir == "dec":
      return (False, i)
    if delta < 0 and dir == "inc":
      return (False, i)
  ## All the inputs were valid, return true
  return (True, 0)

def part1(filename: str):
  with open(filename, 'r') as f:
      safeCount = 0
      for line in f:
        split = list(map(int, line.split()))
        isSafe, _ = isSafeLine(split)
        if isSafe:
          safeCount += 1
      print(f"count of safe reports: {safeCount}")
        

def part2(filename: str):
  with open(filename, 'r') as f:
    safeCount = 0
    lineCount = 0
    for line in f:
      lineCount += 1
      split = list(map(int, line.split()))
      isSafe, firstUnsafe = isSafeLine(split)
      if isSafe:
        safeCount += 1
        continue
      for j in [-1, 0, 1]:
        if j == -1 and firstUnsafe == 0:
          continue
        withoutN = split.copy()
        del withoutN[firstUnsafe + j]
        withoutIsSafe, _ = isSafeLine(withoutN)
        if withoutIsSafe:
          safeCount += 1
          break
    print(f"count of safe reports w/ dampening: {safeCount} - lineCount: {lineCount}")


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

if part == "pt1":
  part1(filename)
else:
  part2(filename)

