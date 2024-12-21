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
        print(f"b: {regs[1]} - oldA: {oldA} - b % 8: {regs[1] % 8}")
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
  return out

def part2naive(regs: list[int], cmds: str):
  #i = 1
  #while True:
  for i in [2 ** x for x in range(50)]:
    regs[0] = i
    p1 = part1(regs, cmds)
    if p1 == cmds:
      print(f"Found the correct A register: {i}")
      return
    #if i % 100000 == 0:
    print(f"checked {i} - len(p1): {len(p1)}")
    i += 1
  print(f"len(cmds): {len(cmds)}")
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

This is how I derived B in terms of A
B1 = (A % 8) ^ 5
C = A // (2 ** B1) = A // (2 ** (A % 8) ^ 5)
B2 = (A % 8) ^ 5 ^ 6 = (A % 8) ^ 3
B3 = B2 ^ C = ((A % 8) ^ 3) ^ (A // (2 ** (A % 8) ^ 5)
'''
def part2(regs: list[int], cmds: str):
  # We know a is 0 at the very end. The step before that, it must have been somewhere btw 1-7
  # But at each step, b is a function of a as described above. So start
  a = 0
  for i, expectedB in enumerate(reversed(cmds)):
    testA = 1
    while True:
      b = testA % 8
      b = b ^ 5
      c = testA // (2 ** b)
      b = b ^ 6
      b = b ^ c
      if b % 8 == int(expectedB):
        print(f"{b % 8}:found testA {testA} - b: {b}")
        break
      testA += 1
    if expectedB == 2:
      break
    a += testA << (i * 3) 

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