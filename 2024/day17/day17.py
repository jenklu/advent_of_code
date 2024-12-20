import sys

def combo(op, regs):
  return op if op < 4 else regs[op - 4]

def part1(regs: list[int], cmds: str):
  ip, out = 0, []
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
    else:
      ip += 2
  print(",".join([str(s) for s in out]))

def part2():
  pass

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
  part1(regs, cmds) if part == "pt1" else part2(plot)