import sys
from collections import defaultdict

# zzzzxyyyyy
# (z^y)(z^y)(z^y)(z^y)xyyyyy

# num = (num[:18] ^ num[6:24]) << 6 + num[:6]
# num = num[5:29] ^ num
# num = (num[:13] ^ num[13:24]) << 11 + num[:11]

# num[:9] = (num[6:9] ^ num[:3]) << 6 + num[:6]
# num[:4] = num[:4] ^ num[5:9] = num[:4] ^ (num[6:9] ^ num[:3] + num[5])
# num[:11] = num[:11]

def nextNum(num)->int:
  num = ((num << 6) ^ num) % 16777216
  num = ((num >> 5) ^ num)# % 16777216
  return ((num << 11) ^ num) % 16777216

def part1(seeds: list[int]):
  result = 0
  for num in seeds:
    for i in range(2000):
      num = nextNum(num)
    result += num
  print(f"result: {result}")

def getScores(seed: int)->dict[tuple[int], int]:
  last4, prev = (), seed
  scores = {}
  for i in range(2000):
    curr = nextNum(prev)
    currPrice = curr % 10
    last4 = (currPrice - prev % 10, *last4[:3])
    if len(last4) == 4 and last4 not in scores:
      scores[last4] = currPrice
    prev = curr
  return scores

def part2(seeds: list[int]):
  scores = defaultdict(lambda: 0)
  for seed in seeds:
    seedScores = getScores(seed)
    for seq, score in seedScores.items():
      scores[seq] += score
  maxSeq = max(scores, key=scores.get)
  print(f"maxScore: {scores[maxSeq]} - seq: {maxSeq}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  seeds = [int(x) for x in f.read().splitlines()]
  part1(seeds) if part == "pt1" else part2(seeds)
