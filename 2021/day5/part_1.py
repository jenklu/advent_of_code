#!/usr/local/bin/python3-32
import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file path>")
    exit(0)

input = []
with open(sys.argv[1], 'r') as f:
    input = f.readlines()

lines = defaultdict(lambda: 0)
for line in input:
    split = line.split(",")
    if len(split) != 3:
        raise RuntimeError(f"unexpected string split: {split}")
    inner = split[1].split(" -> ")
    if len(inner) != 2:
        raise RuntimeError(f"unexpected inner split: {inner}")
    x1 = int(split[0])
    y1 = int(inner[0])
    x2 = int(inner[1])
    y2 = int(split[2])
    if x1 == x2 or y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        for x in range(x1, max(x2 + 1, x1 + 1)):
            for y in range(y1, max(y2 + 1, y1 + 1)):
                lines[(x, y)] += 1
# print(lines) 
for y in range(0, 10):
    s = ""
    for x in range(0, 10):
         val = lines.get((x, y))
         if val:
             s += str(val)
         else:
             s += "."
    print(s)
            
twodeep = 0
for val in lines.values():
    if val >= 2:
        twodeep += 1
print(f"twodeep: {twodeep}")
                
