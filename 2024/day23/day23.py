import sys
from collections import defaultdict
def part1(connections: list[int]):
  edges = defaultdict(list)
  for connection in connections:
    edges[connection[0]].append(connection[1])
    edges[connection[1]].append(connection[0])
  triples = set()
  for connection in connections:
    for other in edges[connection[0]]:
      if other != connection[1] and other in edges[connection[1]]:
        triples.add(tuple(sorted((other, connection[0], connection[1]))))
  count = 0
  for triple in triples:
    for item in triple:
      if item[0] == "t":
        count += 1
        break
  print(f"count: {count}")
    
def part2(connections):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
  print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
  exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  connections = [s.split('-') for s in f.read().splitlines()]
  part1(connections) if part == "pt1" else part2(connections)
