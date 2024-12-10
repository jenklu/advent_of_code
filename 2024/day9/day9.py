import sys
import copy

def part1(fileMap: list[int]):
  generated = []
  # If even, the last # is just free space, so go to last non-free file
  front, back = 0, len(fileMap) - (2 - len(fileMap) % 2)
  wroteFront = False
  while back > front:
    if not wroteFront:
      generated.extend([front // 2 for x in range(fileMap[front])])
      wroteFront = True
    # If there is space in the current gap OR this is the last
    # gap, write all of the back into the gap
    if fileMap[back] < fileMap[front + 1] or (back - front) <= 2:
      generated.extend([back // 2 for x in range(fileMap[back])])
      fileMap[front + 1] -= fileMap[back]
      back -= 2
    else:
      generated.extend([back // 2 for x in range(fileMap[front + 1])])
      fileMap[back] -= fileMap[front + 1]
      front += 2
      if fileMap[back] == 0:
        back -= 2
      wroteFront = False

  checksum = 0
  for i in range(1, len(generated)):
    checksum += i * int(generated[i])
    #print(f"i: {i} generated[i]: {generated[i]} checksum: {checksum}")
  print(f"checksum: {checksum}\ngenerated string[0:100]: {generated[0:100]}")


def part2(fileMap: list[int]):
  pass
## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  fileMap = [int(x) for x in list(f.readline().rstrip())]
  print(len(fileMap))
  if part == "pt1":
    part1(fileMap)
  else:
    part2(fileMap)
