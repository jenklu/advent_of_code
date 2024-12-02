import sys
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file path>")
    exit(0)

right, left = [], []
with open(sys.argv[1], 'r') as f:
    for line in f:
      split = line.split()
      left.append(int(split[0]))
      right.append(int(split[1]))

left.sort()
right.sort()
dist = 0
for i in range(len(left)):
  dist += abs(left[i] - right[i])

print(f"total distance: {dist}")