import sys

DIR_MAP = {'<': (-1, 0), '>': (1, 0), 'v': (0, 1), '^': (0, -1)}
def part1(plot: list[list[str]], seq: str, bot: tuple[int, int]):
  for s in seq:
    deltaX, deltaY = DIR_MAP[s][0], DIR_MAP[s][1]
    nextX, nextY = bot[0] + deltaX, bot[1] + deltaY
    nextNextX, nextNextY = nextX, nextY
    # while to handle multiple boxes next to each other
    while plot[nextNextY][nextNextX] == 'O':
      nextNextX, nextNextY = nextNextX + deltaX, nextNextY + deltaY
    if plot[nextNextY][nextNextX] == '#':
      continue
    # There was at least 1 box
    if nextNextX != nextX or nextNextY != nextY:
      plot[nextNextY][nextNextX] = 'O'
    plot[bot[1]][bot[0]] = '.'
    plot[nextY][nextX], bot = '@', (nextX, nextY)
  print("finalplot\n" + "\n".join(["".join(row) for row in plot]))
  total = 0
  for y in range(len(plot)):
    for x in range(len(plot[0])):
      if plot[y][x] == 'O':
        total += x + 100*y
  print(f"total: {total}")

def findVerticalBoxUpdates(plot: list[list[str]], startX: int, y: int, delta: int) -> list[tuple[int, int, str]]:
  updates = {}
  candidates = {startX}
  while candidates:
    nextCandidates = set()
    for x in candidates:
      if plot[y][x] == '#':
        return None
      # either we already handled this X or it's not a box
      if x in nextCandidates or plot[y][x] not in '[]':
        continue
      # Create the updates for the current box
      otherX = x + (1 if plot[y][x] == '[' else -1)
      updates[(x, y+delta)] = plot[y][x]
      updates[(otherX, y+delta)] = plot[y][otherX]
      # no box is taking this box's places, so fill in with a '.'
      if (otherX, y) not in updates:
        updates[(otherX, y)] = '.'
      # Add items to check
      nextCandidates.update((x, otherX))
    y, candidates = y+delta, nextCandidates
  return [(loc[0], loc[1], val) for loc, val in updates.items()]

def findHorizontalBoxUpdates(plot: list[list[str]], x: int, y: int, delta: int) -> list[tuple[int, int, str]]:
  endX = x
  while plot[y][endX] in '[]':
    endX += delta
  if plot[y][endX] == '#':
    return None
  return [(i, y, plot[y][i-delta]) for i in range(x, endX+delta, delta)]
                           
def part2(plot: list[list[str]], seq: str, bot: tuple[int, int]):
  DIR_MAP = {'<': (-1, 0), '>': (1, 0), 'v': (0, 1), '^': (0, -1)}
  for s in seq:
    deltaX, deltaY = DIR_MAP[s][0], DIR_MAP[s][1]
    nextX, nextY = bot[0] + deltaX, bot[1] + deltaY
    if plot[nextY][nextX] == '#':
      continue
    # Move those boxes
    boxUpdates = {}
    if s in "<>":
      boxUpdates = findHorizontalBoxUpdates(plot, nextX, nextY, deltaX)
    else:
      boxUpdates = findVerticalBoxUpdates(plot, nextX, nextY, deltaY)
    # one of the boxes hit a wall
    if boxUpdates is None:
      continue
    for update in boxUpdates:
      plot[update[1]][update[0]] = update[2]
    # move the bot
    plot[bot[1]][bot[0]] = '.'
    plot[nextY][nextX], bot = '@', (nextX, nextY)

  print("finalplot\n" + "\n".join(["".join(row) for row in plot]))
  total = 0
  for y in range(len(plot)):
    for x in range(len(plot[0])):
      if plot[y][x] == '[':
        total += x + 100*y
  print(f"total: {total}")

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  plot, seq, bot, isPart1 = [], "", (-1, 0), part == "pt1"
  for y, line in enumerate(f):
    if line[0] in "<>^v":
      seq += line.rstrip()
      continue
    if line == "\n":
      continue
    if isPart1:
      bot = (line.find("@"), y) if bot[0] == -1 else bot
      plot.append(list(line.rstrip()))
      continue
    plot.append([])
    for x, c in enumerate(line):
      if c == '@':
        bot = (2*x, y)
        plot[-1].extend([c, '.'])
      elif c == 'O':
        plot[-1].extend(['[', ']'])
      elif c != "\n":
        plot[-1].extend([c, c])
  part1(plot, seq, bot) if isPart1 else part2(plot, seq, bot)
