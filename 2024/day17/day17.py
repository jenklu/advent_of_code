import sys

def combo(op, regs):
  return op if op < 4 else regs[op - 4]

def part1(regs: list[int], cmds: str):
  ip, out = 0, []
  print(f"regs: {regs}")
  oldA = regs[0]
  while ip < len(cmds):
    match cmds[ip]:
      case 0:
        regs[0] = regs[0] // 2 ** combo(cmds[ip+1], regs)
      case 1:
        regs[1] = regs[1] ^ cmds[ip+1]
      case 2:
        regs[1] = combo(cmds[ip+1], regs) % 8
      case 4:
        regs[1] = regs[1] ^ regs[2]
      case 5:
        out.append(combo(cmds[ip+1], regs) % 8)
      case 6:
        regs[1] = regs[0] // 2 ** combo(cmds[ip+1], regs)
      case 7:
        regs[2] = regs[0] // 2 ** combo(cmds[ip+1], regs)
    if cmds[ip] == 3 and regs[0] != 0:
      ip = cmds[ip+1]
      oldA = regs[0]
    else:
      ip += 2
  print(out)
  return out

def generateA(cmds, currA, depth)->int:
  expectedB, candidates = cmds[-1], []
  # The correctness of the previous iteration depends on the condition nextA // 8 == prevA, so we
  # only need to consider a in [prevA*8,prevA*8+7]. Values of a > prevA*8+7 invalidate the nextA //
  # 8 == prevA condition. This condition is essential for backtracking, but was tricky to figure out
  for a in [currA + i for i in range(0, 8)]:
    b = a % 8
    b = b ^ 5
    c = a // (2 ** b)
    b = b ^ 6
    b = b ^ c
    # b is a pure function of a, so if b % 8 == expectedB, consider this a for the next round.
    if b % 8 == int(expectedB):
      # If there's only one `b` left to print, then the first candidate is the lowest, so return it
      if len(cmds) == 1:
        return a
      candidates.append(a)
  # I originally tried to find a solution here without the `nextA // 8 == prevA` condition, and
  # just kept incrementing a at every backtracking iteration to find the next iteration's a. But
  # this can cause the next iterations `a` to not satisfy the above condition.
  for candidate in candidates:
    nextA = candidate * 8
    res = generateA(cmds[:-1], nextA, depth+1)
    if res != -1:
      return res
  return -1

'''
This is the program represented by `input.txt`
B = A % 8
B = B ^ 5
C = A // (2 ** B)
A = A // (2 ** 3)
B = B ^ 6
B = B ^ C
PRINT(B % 8)
GOTO(1) IF A != 0

This is how I derived B in terms of A (wasted time, not used)
B1 = (A % 8) ^ 5
C = A // (2 ** B1) = A // (2 ** (A % 8) ^ 5)
B2 = (A % 8) ^ 5 ^ 6 = (A % 8) ^ 3
B3 = B2 ^ C = ((A % 8) ^ 3) ^ (A // (2 ** (A % 8) ^ 5)
'''
def part2(regs: list[int], cmds: str):
  a = generateA(cmds, 0, 0)
  regs[0] = a
  print(f"Found a: {a}")
  print(f"part1: {part1(regs, cmds)}")


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  lines = f.read().splitlines()
  regs = [int(lines[i].split(':')[1]) for i in range(3)]
  cmds = [int(x) for x in lines[4].split(':')[1] if x.isdigit()]
  part1(regs, cmds) if part == "pt1" else part2(regs, cmds)