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
    nextX, nextY, potentialDirChange = nextLocAndPotentialDir(mapInput[y][x], x, y)
    if not (0 <= nextX < mapWidth) or not (0 <= nextY < len(mapInput)):
      print(f"Went off the map at ({nextX}, {nextY}). Count of x's: {markedCount}")
      return
    nextChar = mapInput[nextY][nextX]
    if nextChar == "#":
      mapInput[y][x] = potentialDirChange
      continue
    
    if nextChar == ".":
      markedCount += 1
    elif nextChar != "x":
      raise Exception(f"nextChar was {nextChar} not in '.x$'")
    mapInput[nextY][nextX] = mapInput[y][x]
    mapInput[y][x] = 'x'
    x, y = nextX, nextY

def printMapInput(mapInput):
  for line in mapInput:
    printedLine = ""
    for item in line:
      if isinstance(item, str):
        printedLine += item + "   "
      else:
        printedLine += "".join(item) + (" " * (4 - len(item)))
    print(printedLine)

def part2(mapInput: list[str]):
  mapWidth = len(mapInput[0])
  x, y = 0, 0
  direction = "^"
  for i in range(len(mapInput)):
    for j in range(mapWidth):
      if mapInput[i][j] in "^v<>":
        x, y = j, i
        direction = mapInput[i][j]
        break
    else:
      continue
    # only break if start x, y is found
    break
  obstacleCount = 0
  obstacles = []
  while True:
    # Check exit condition
    nextX, nextY, potentialDirChange = nextLocAndPotentialDir(direction, x, y)
    if not (0 <= nextX < mapWidth) or not (0 <= nextY < len(mapInput)):
      print(f"Went off the map at ({nextX}, {nextY}). Potential loop obstacles: {obstacleCount}\nObstacles: {obstacles}\nmapInput{printMapInput(mapInput)}")
      return
    # Mark the current location as visited by create/insert direction into a list
    location = mapInput[y][x]
    if isinstance(location, str):
      mapInput[y][x] = [direction]
    elif type(location) is list:
      if direction not in location:
        mapInput[y][x] += direction
    else:
      raise Exception(f"location unexpectedly was {location}")
    # We hit an obstacle, turn right
    if mapInput[nextY][nextX] == "#":
      direction = potentialDirChange
      continue
    # Pretend there was an obstacle in front of us. If turning right would start us on a path
    # we've already taken, then we know we'll hit the current location again => cycle
    nextXWithObstacle, nextYWithObstacle, _ = nextLocAndPotentialDir(potentialDirChange, x, y)
    nextLocationWithObstacle = mapInput[nextYWithObstacle][nextXWithObstacle]
    if type(nextLocationWithObstacle) is list and potentialDirChange in nextLocationWithObstacle:
      obstacles.append((nextX, nextY))
      obstacleCount += 1
    x, y = nextX, nextY

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