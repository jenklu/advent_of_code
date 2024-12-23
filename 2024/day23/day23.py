import sys
from collections import defaultdict
from copy import copy

def part1(connections: list[str]):
  edges = defaultdict(set)
  for connection in connections:
    edges[connection[0]].add(connection[1])
    edges[connection[1]].add(connection[0])
  triples = set()
  for connection in connections:
    for other in edges[connection[0]]:
      if other != connection[1] and other in edges[connection[1]]:
        for s in (other, connection[0], connection[1]):
          if s[0] == 't':
            triples.add(tuple(sorted((other, connection[0], connection[1]))))
  print(f"count: {len(triples)}")

memo = {}
def findLargestSet(start: str, seen: set[str], edges: dict[str, set[str]]):
  if start in memo:
    return memo[start]
  maxSet = seen
  for node in edges[start]:
    if node not in seen and seen.issubset(edges[node]):
      seenCopy = copy(seen)
      seenCopy.add(node)
      memo[node] = findLargestSet(node, seenCopy, edges)
      if len(memo[node]) > len(maxSet):
        maxSet = memo[node]
  return maxSet

def part2(connections):
  edges = defaultdict(set)
  for connection in connections:
    edges[connection[0]].add(connection[1])
    edges[connection[1]].add(connection[0])
  largest = set()
  for node in edges:
    res = findLargestSet(node, set(), edges)
    if len(res) > len(largest):
      largest = res 
  print(f"largest: {",".join(sorted(largest))}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
  print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
  exit(1)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  connections = [s.split('-') for s in f.read().splitlines()]
  part1(connections) if part == "pt1" else part2(connections)
