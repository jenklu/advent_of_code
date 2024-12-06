import sys

def nextLocAndPotentialDir(current: str, x: int, y: int) -> (int, int, str):
  nextX, nextY = x, y
  match current:
    case "^":
      return x, y-1, ">"
    case "v":
      return x, y+1, "<"
    case ">":
      return x+1, y, "v"
    case "<":
      return x-1, y, "^"
    case _:
      raise Exception(f"Got unexpected character: {current}")

def part1(mapInput: list[str]):
  mapWidth = len(mapInput[0])
  x, y = 0, 0
  for i in range(len(mapInput)):
    for j in range(mapWidth):
      if mapInput[i][j] in "^v<>":
        x, y = j, i
        break
    else:
      continue
    # only break if start x, y is found
    break
  # count the starting point as marked, as we will count places as marked before
  # actually "moving" to the next location
  markedCount = 1
  while True:
    nextX, nextY, potentialDirectionChange = nextLocAndPotentialDir(mapInput[y][x], x, y)
    if not (0 <= nextX < mapWidth) or not (0 <= nextY < len(mapInput)):
      print(f"Went off the map at ({nextX}, {nextY}). Count of x's: {markedCount}")
      return
    nextChar = mapInput[nextY][nextX]
    if nextChar == "#":
      mapInput[y][x] = potentialDirectionChange
      continue
    
    if nextChar == ".":
      markedCount += 1
    elif nextChar != "x":
      raise Exception(f"nextChar was {nextChar} not in '.x$'")
    mapInput[nextY][nextX] = mapInput[y][x]
    mapInput[y][x] = 'x'
    x, y = nextX, nextY


def part2(mapInput: list[str]):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  mapInput = [list(line) for line in f.read().splitlines()]
  if part == "pt1":
    part1(mapInput)
  else:
    part2(mapInput)
