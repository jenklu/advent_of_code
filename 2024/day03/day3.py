import sys

def getInt(slice: str, expectedLast: str) -> str:
  if not slice[0].isdecimal():
    return ""
  val = slice[0]
  for i in range(1, 4):
    if i > len(slice):
      return ""
    if slice[i] == expectedLast:
      return val
    if slice[i].isdecimal():
      val += slice[i]
    else:
      return ""

def part1(contents: str):
  i = 0
  result = 0
  while i < len(contents) - 3:
    if contents[i:i+4] != "mul(":
      i += 1
      continue
    i += 4

    leftVal = getInt(contents[i:i+4], ",")
    if leftVal == "":
      continue
    
    i += len(leftVal) + 1
    rightVal = getInt(contents[i:i+4], ")")
    if rightVal == "":
      continue
    result += int(leftVal) * int(rightVal)
  print(f"result: {result}")


def part2(contents: str):
  i = 0
  result = 0
  do = True
  while i < len(contents) - 3:
    if contents[i:i+4] == "mul(" and do:
      i += 4
    elif contents[i:i+7] == "don't()":
      do = False
      i += 7
      continue
    elif contents[i:i+4] == "do()":
      do = True
      i += 4
      continue
    else:
      i += 1
      continue

    leftVal = getInt(contents[i:i+4], ",")
    if leftVal == "":
      continue
    
    i += len(leftVal) + 1
    rightVal = getInt(contents[i:i+4], ")")
    if rightVal == "":
      continue
    result += int(leftVal) * int(rightVal)
  print(f"result: {result}")


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  contents = f.read()
  if part == "pt1":
    part1(contents)
  else:
    part2(contents)

