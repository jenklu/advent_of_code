import sys


def part1(plot: list[list[str]], seq: str, bot: tuple[int, int]):
  nextMap = {'<': (-1, 0), '>': (1, 0), 'v': (0, 1), '^': (0, -1)}
  for s in seq:
    deltaX, deltaY = nextMap[s][0], nextMap[s][1]
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
  print("finalplot")
  print("\n".join(["".join(row) for row in plot]))
  sum = 0
  for y in range(len(plot)):
    for x in range(len(plot[0])):
      if plot[y][x] == 'O':
        sum += x + 100*y
  print(f"sum: {sum}")

def part2(topos: list[list[int]], trailheads: list[tuple[int, int]]):
  pass

## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  plot, seq, bot = [], "", (0, 0)
  for y, line in enumerate(f):
    if line[0] == '#':
      botX = line.find('@')
      if botX != -1:
        bot = (botX, y)
      plot.append(list(line.rstrip()))
    else:
      seq += line.rstrip()
  if part == "pt1":
    part1(plot, seq, bot)
  else:
    part1(plot, seq, bot)
