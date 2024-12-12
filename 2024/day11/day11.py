import sys
import math
import time

def handler(startStones: list[int], itersToTry, recursionDepth) -> int:
  stoneCount = 0
  for startIdx, startStone in enumerate(startStones):
    if recursionDepth == 0:
      print(f"processing stone {startIdx} from OG list")
    stones = [startStone]
    for i in range(itersToTry):
      if len(stones) > 10 ** 6:
        itersLeft = itersToTry - i
        print(f"splitting left at {i}, recursionDepth: {recursionDepth}, itersLeft: {itersLeft}")
        stoneCount += handler(stones[:len(stones) // 2], itersLeft, recursionDepth+1)
        print(f"splitting right at {i}, recursionDepth: {recursionDepth}, itersLeft: {itersLeft}")
        stoneCount += handler(stones[len(stones) // 2:], itersLeft, recursionDepth+1)
        break
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
    else:
      stoneCount += len(stones)
  return stoneCount

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
  print(f"stoneCount: {handler(stones, stoneIters, 0)}")
