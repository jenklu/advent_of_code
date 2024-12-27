import sys

def findRes(num: int, iters: int)->int:
  for i in range(iters):
    num = ((num * 64) ^ num) % 16777216
    num = ((num // 32) ^ num) % 16777216
    num = ((num * 2048) ^ num) % 16777216
  return num
def part1(seeds: list[int]):
  result = 0
  for seed in seeds:
    result += findRes(seed, 2000)
  print(f"result: {result}")
## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  seeds = [int(x) for x in f.read().splitlines()]
  part1(seeds) if part == "pt1" else part2(seeds)
