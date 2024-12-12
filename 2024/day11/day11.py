import sys
import math

def part1(stones: list[int], stoneIters):
  for i in range(stoneIters):
    nextStones = []
    for stone in stones:
      if stone == 0:
        nextStones.append(1)
      else:
        digitCount = math.floor(math.log(stone, 10)) + 1
        if digitCount % 2 == 0:
          right = stone % (10 ** (digitCount // 2))
          left = stone // (10 ** (digitCount // 2))
          nextStones.append(left)
          nextStones.append(right)
        else:
          nextStones.append(stone * 2024)
    stones = nextStones
  print(f"len(stones): {len(stones)}\nstones[:30]: {stones[:30]}")
  
def part2(stones: list[str]):
  pass

## main
print(sys.argv)
if len(sys.argv) not in [3, 4] or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path> (stoneIters)")
    exit(0)
part, filename, stoneIters = sys.argv[1], sys.argv[2], 25
if len(sys.argv) == 4:
  stoneIters = int(sys.argv[3])

with open(filename, 'r') as f:
  stones = [int(x) for x in f.read().split()]
  if part == "pt1":
    part1(stones, stoneIters)
  else:
    part2(stones)
