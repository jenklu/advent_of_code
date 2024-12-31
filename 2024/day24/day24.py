import sys
from dataclasses import dataclass
from collections import defaultdict
from typing import Union
from copy import copy

@dataclass
class Gate:
  lhs: str
  rhs: str
  op: str
  out: str

def runGate(lhs: int, rhs: int, op: str):
  if op == "AND":
    return lhs and rhs
  elif op == "OR":
    return lhs or rhs
  elif op == "XOR":
    return lhs ^ rhs

def gateToStr(g: Gate):
  left = g.lhs if len(g.lhs) == 3 else f"({g.lhs})"
  right = g.rhs if len(g.rhs) == 3 else f"({g.rhs})"
  return f"{left} {g.op} {right}"
  
def part1(inputs: dict[str, int], gates: dict[str, list[Gate]]):
  output = 0
  cands = list(inputs.keys())
  while cands:
    nextCands = []
    for c in cands:
      for g in gates[c]:
        other = g.lhs if c != g.lhs else g.rhs
        if other in inputs and g.out not in inputs:
          nextCands.append(g.out)
          res = runGate(inputs[g.lhs], inputs[g.rhs], g.op)
          inputs[g.out] = res
          if g.out[0] == "z":
            output += res << int(g.out[1:])
    cands = nextCands
  print(output)
  return output

def genCarries(i: int, carries: dict[int, str]):
  if i == 1:
    carries[1] = "x00 AND y00"
    return carries[1]
  carries[i] = f"((x{i-1:0{2}} XOR y{i-1:0{2}}) AND ({genCarries(i-1, carries)})) OR (x{i-1:0{2}} AND y{i-1:0{2}})"
  return carries[i]

# Answer based on inspecting fishy ones and carry/replacements to find swaps
# vdc<>z12 nhn<>z21 khg<>tvb gst<>z33
# sorted: gst,khg,nhn,tvb,vdc,z12,z21,z33
def part2(inputs: dict[str, int], gates: dict[str, list[Gate]]):
  inputs = {k: k for k in inputs.keys()}
  cands = list(inputs.keys())
  carries = []
  while cands:
    nextCands = []
    for c in cands:
      for g in gates[c]:
        other = g.lhs if c != g.lhs else g.rhs
        if other in inputs and g.out not in inputs:
          gCopy = copy(g)
          nextCands.append(g.out)
          gCopy.lhs, gCopy.rhs = inputs[g.lhs], inputs[g.rhs]
          res = gateToStr(gCopy)
          inputs[g.out] = res
          if g.op == "OR":
            carries.append(res)
    cands = nextCands
  for k, v in inputs.items():
    print(f"{k}: {v}")
  replaced = {}
  longToShort = list(reversed(sorted(carries, key=len)))
  carryGates = {}
  for k, v in inputs.items():
    replaced[k] = v
    for i, carry in enumerate(longToShort):
      if carry in v:
        replaced[k] = v.replace(carry, f"c{44-i:0{2}}")
        if carry == v:
          carryGates[k] = f"c{44-i:0{2}}"
        break
  for k, v in carryGates.items():
    print(f"{v}: {k}")
  fishy_ones = []
  for k, v in replaced.items():
    print(f"{v} -> {k}")
    if "z" in k:
      num = int(k[1:])
      if v.count("XOR") != 2 or v.count(str(num)) != 2 or v.count(str(num-1)) != 1:
        fishy_ones.append(f"{k}: {v}")
  print("fishy ones:")
  for f in fishy_ones:
    print(f)
  # reversedInputs = {v: k for k, v in inputs.items()}
  # carries = {}
  # genCarries(45, carries)
  # gateToCarries = {}
  # for i, carry in carries.items():
  #   if carry in reversedInputs:
  #     gateToCarries[f"c{i:0{2}}"] = reversedInputs[carry]
  # print(carries)
  # print(gateToCarries)
  # sortedOuts = sorted(outputs.items(), key=lambda it: it[1])
  # for outRes, outGate in sortedOuts:
  #   print(f"{outGate}: {outRes}")
  # outWithReplacements = {}
  # for i, (outRes, gateName) in enumerate(sortedOuts):
  #   replaced = outRes
  #   for otherRes, otherGate in reversed(sortedOuts[:i]):
  #     replaced.replace(otherRes, otherGate)
  #   outWithReplacements[gateName] = replaced
  # [print(f"{k}: {v}") for k, v in outWithReplacements.items()]
  # for curr, (res, gateName) in enumerate(outputs.items()):
  #   print(curr)
  #   for i in range(int(gateName[1:])):
  #     x, y = f"x{i:0{2}}", f"y{i:0{2}}"
  #     if x not in res:
  #       print(f"{x} not an input to {gateName}")
  #     if y not in res:
  #       print(f"{y} not an input to {gateName}")
  #   for i in range(int(gateName[1:])+1, 45):
  #     x, y = f"x{i:0{2}}", f"y{i:0{2}}"
  #     if x in res:
  #       print(f"{x} unexpectedly an input to {gateName}")
  #     if y in res:
  #       print(f"{y} unexpectedly an input to {gateName}")
 
  # for x in [2 ** i - 1 for i in range(1, 45)]:
  #   for y in [2 ** i - 1 for i in range(1, 45)]:
  #     xs = {f"x{i:0{2}}": (x >> i) % 2 for i in range(44)}
  #     ys = {f"y{i:0{2}}": (y >> i) % 2 for i in range(44)}
  #     expected = x + y
  #     res = part1(xs | ys, gates)
  #     if expected ^ res != 0:
  #       print(f"x: {x} y: {y} res: {res} expected ^ res: {bin(expected ^ res)}")


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
    gates[g.lhs].append(g)
    gates[g.rhs].append(g)
  part1(inputs, gates) if part == "pt1" else part2(inputs, gates)
