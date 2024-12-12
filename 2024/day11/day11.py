import sys
import math

memo = {}
def handler(stones, itersLeft):
  if len(stones) == 0 or itersLeft == 0:
    return len(stones)
  stoneCount = 0
  stone = stones[0]
  if (stone, itersLeft) in memo:
    stoneCount += memo[(stone, itersLeft)]
  else:
    nextStone = [1]
    if stone != 0:
      digitCount = math.floor(math.log(stone, 10)) + 1
      if digitCount % 2 == 0:
        right = stone % (10 ** (digitCount // 2))
        left = stone // (10 ** (digitCount // 2))
        nextStone = [left, right]
      else:
        nextStone = [stone * 2024]
    for nxt in nextStone:
      res = handler([nxt], itersLeft - 1)
      memo[(nxt, itersLeft - 1)] = res
      stoneCount += res
  return stoneCount + handler(stones[1:], itersLeft)

## main
print(sys.argv)
if len(sys.argv) not in [3, 4] or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path> (stoneIters)")
    exit(0)
part, filename, stoneIters = sys.argv[1], sys.argv[2], 75
if len(sys.argv) == 4:
  stoneIters = int(sys.argv[3])
elif part == "pt1":
  stoneIters = 25

with open(filename, 'r') as f:
  stones = [int(x) for x in f.read().split()]
  print(f"stoneCount: {handler(stones, stoneIters)}")
  print(f"len(memo): {len(memo)}")
