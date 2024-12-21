import sys

memo = {}
def canMake(towels, pattern, seen):
  if not pattern:
    return True
  if pattern in memo:
    return memo[pattern]
  for towel in towels:
    l = len(towel)
    tempSeen = seen + pattern[:l]
    if towel == pattern[:l]:
      memo[tempSeen] = True
      if canMake(towels, pattern[l:], tempSeen):
        return True
      memo[pattern[l:]] = False
  return False

def part1(towels: list[str], patterns: list[str]):
  score = sum([1 for pattern in patterns if canMake(towels, pattern, "")])
  print(f"score: {score}")

def part2(towels: list[str], patterns: list[str]):
  pass

## main
print(sys.argv)
if len(sys.argv) not in [3, 4] or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]
with open(filename, 'r') as f:
  lines = f.readlines()
  towels = lines[0].rstrip().split(', ')
  patterns = [line.rstrip() for line in lines[2:]]
  part1(towels, patterns) if part == "pt1" else part2(towels, patterns)
