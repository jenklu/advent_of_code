import sys
import copy

def part1(fileMap: list[int]):
  checksum, checkSumIndex = 0, 0
  # If even, the last # is just free space, so go to last non-free file
  front, back = 0, len(fileMap) - (2 - len(fileMap) % 2)
  wroteFront = False
  while back > front:
    if not wroteFront:
      checksum += sum([front // 2 * i for i in range(checkSumIndex, checkSumIndex + fileMap[front])])
      checkSumIndex += fileMap[front]
      wroteFront = True
    # If there is space in the current gap OR this is the last
    # gap, write all of the back into the gap
    if fileMap[back] < fileMap[front + 1] or (back - front) <= 2:
      checksum += sum([back // 2 * i for i in range(checkSumIndex, checkSumIndex + fileMap[back])])
      checkSumIndex += fileMap[back]
      fileMap[front + 1] -= fileMap[back]
      back -= 2
    else:
      checksum += sum([back // 2 * i for i in range(checkSumIndex, checkSumIndex + fileMap[front + 1])])
      checkSumIndex += fileMap[front + 1]
      fileMap[back] -= fileMap[front + 1]
      front += 2
      if fileMap[back] == 0:
        back -= 2
      wroteFront = False

  print(f"checksum: {checksum}")


def part2(fileMap: list[int]):
  generated = []
  files = []
  spaces = []
  for x in range(len(fileMap)):
    if x % 2 == 0:
      files.append((len(generated), fileMap[x]))
      generated.extend([x // 2 for i in range(fileMap[x])])
    else:
      spaces.append((len(generated), fileMap[x]))
      generated.extend(['.' for i in range(fileMap[x])])
  for file in reversed(files):
    for i in range(len(spaces)):
      if spaces[i][0] > file[0]:
        break
      if file[1] <= spaces[i][1]:
        fileNum = generated[file[0]]
        for x in range(file[1]):
          generated[spaces[i][0] + x] = fileNum
          generated[file[0] + x] = '.'
        spaces[i] = (spaces[i][0] + file[1], spaces[i][1] - file[1])
        break

  checksum = 0
  for idx, val in enumerate(generated):
    if val != '.':
      checksum += idx * val
  print(f"checksum: {checksum}")
  print(generated[0:100])

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
