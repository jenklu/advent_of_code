import sys
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Gate:
  in1: str
  in2: str
  op: str
  out: str

def runGate(in1: int, in2: int, op: str):
  if op == "AND":
    return in1 and in2
  elif op == "OR":
    return in1 or in2
  elif op == "XOR":
    return in1 ^ in2

def part1(inputs: dict[str, int], gates: dict[str, list[Gate]]):
  output = 0
  cands = list(inputs.keys())
  while cands:
    nextCands = []
    for c in cands:
      for g in gates[c]:
        other = g.in1 if c != g.in1 else g.in2
        if other in inputs and g.out not in inputs:
          nextCands.append(g.out)
          res = runGate(inputs[g.in1], inputs[g.in2], g.op)
          inputs[g.out] = res
          if g.out[0] == "z":
            output += res << int(g.out[1:])
    cands = nextCands
  print(output)

def part2(inputs, gates):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  inputs, gates = {}, defaultdict(list)
  for line in f:
    if len(line) < 2:
      continue
    splt = line.split()
    if len(splt) == 2:
      # strip off : from the gate name
      inputs[splt[0][:-1]] = int(splt[1])
      continue
    g = Gate(splt[0], splt[2], splt[1], splt[4])
    gates[g.in1].append(g)
    gates[g.in2].append(g)
  part1(inputs, gates) if part == "pt1" else part2(seeds)
