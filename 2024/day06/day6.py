import sys
import copy

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

def part1(mapInput: list[list[str]]) -> tuple[int, int, set[tuple[int, int]]]:
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
  startX, startY = x, y
  marked = set()
  marked.add((x, y))
  while True:
    direction = mapInput[y][x]
    nextX, nextY, potentialDirChange = nextLocAndPotentialDir(direction, x, y)
    if not (0 <= nextX < mapWidth) or not (0 <= nextY < len(mapInput)):
      print(f"Went off the map at ({nextX}, {nextY}). Count of x's: {len(marked)}")
      return (startX, startY, marked)
    nextChar = mapInput[nextY][nextX]
    if nextChar == "#":
      mapInput[y][x] = potentialDirChange
      continue
    
    if nextChar == ".":
      marked.add((nextX, nextY))
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
        printedLine += item + " "
      else:
        printedLine += "".join(item) + (" " * (2 - len(item)))
    print(printedLine)

def findCycle(mapInput, direction, x, y) -> bool:
  while True:
    # Check exit condition
    nextX, nextY, potentialDirChange = nextLocAndPotentialDir(direction, x, y)
    if not (0 <= nextX < len(mapInput[0])) or not (0 <= nextY < len(mapInput)):
      #print(f"Went off the map at ({nextX}, {nextY}). Potential loop obstacles: {obstacleCount}\nObstacles: {obstacles}\nmapInput{printMapInput(mapInput)}")
      return False
    nextLocation = mapInput[nextY][nextX]
    if type(nextLocation) is list and direction in nextLocation:
      return True
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
    if nextLocation == "#":
      direction = potentialDirChange
      continue
    x, y = nextX, nextY

def part2(mapInput: list[list[str]]):
  dupe = copy.deepcopy(mapInput)
  startX, startY, potentialObstacles = part1(mapInput)
  obstacles = []
  for obstacle in potentialObstacles:
    innerDupe = copy.deepcopy(dupe)
    innerDupe[obstacle[1]][obstacle[0]] = '#'
    if findCycle(innerDupe, dupe[startY][startX], startX, startY):
      obstacles.append(obstacle)
  print(f"obstacle count: {len(obstacles)}\nobstacles: {obstacles}")

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
