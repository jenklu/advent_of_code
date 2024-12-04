import sys
from io import IOBase
def countXmas(stringArray: list[str]) -> int:
  count = 0
  for s in stringArray:
    for i in range(len(s) - 3):
      if s[i:i+4] == "XMAS" or s[i:i+4] == "SAMX":
        count += 1
  return count

def part1(file: IOBase):
  rows, cols, upDiags, downDiags = [], [], [], []
  lines = file.readlines()
  for line in lines:
    line = line.rstrip()
    yPos = len(rows)
    rows.append(line)
    # for first iteration
    if yPos == 0:
      cols = ["" for x in range(len(line))]
      upDiags = ["" for x in range(len(line) + len(lines) - 1)]
      downDiags = ["" for x in range(len(line) + len(lines) - 1)]
    for xPos in range(len(line)):
      cols[xPos] += line[xPos]
      # upDiags rows correspond to the following formula - each diagonal has xPos + yPos = N
      # So we can just build the upDiags by adding the char to the right diagonal
      upDiags[xPos + yPos] += line[xPos]
      # Downdiags are a bit more complicated - each diagonal has xPos - yPos = M, which can now be
      # negative. We could just use a dict here, but I find that unsatisfying, so instead use the
      # "Centerpoint" diag. This is the diagonal starting from (0,0). downDiags starting on (X, 0)
      # will always have M >= 0, downDiags starting on (0, Y) will have M <= 0. As such, we know
      # there will be len(X) diags where M >= 0, so we should use the "centerpoint" from which to
      # add/subtract as len(x)
      centerPointForDownDiags = len(downDiags) - len(line)
      M = xPos - yPos
      downDiags[centerPointForDownDiags - M] += line[xPos]
  print(f"rows: {rows}")
  print(f"cols: {cols}")
  print(f"upDiags: {upDiags}")
  print(f"downDiags: {downDiags}")
  count = countXmas(rows)
  count += countXmas(cols)
  count += countXmas(upDiags)
  count += countXmas(downDiags)

  print(f"result: {count}")


def part2(file: IOBase):
 
  print(f"result: {file}")


## main
print(sys.argv)
if len(sys.argv) != 3 or sys.argv[1] not in ["pt1", "pt2"]:
    print(f"Usage: {sys.argv[0]} (pt1|pt2) <input file path>")
    exit(0)
part, filename = sys.argv[1], sys.argv[2]

with open(filename, 'r') as f:
  if part == "pt1":
    part1(f)
  else:
    part2(f)

