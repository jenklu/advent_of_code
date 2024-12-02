#!/usr/local/bin/python3-32
import sys
from collections import defaultdict

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <input file path>")
    exit(0)

input = []
with open(sys.argv[1], 'r') as f:
    input = f.readlines()[0]

input = input.split(",")
input = list(map(int, input))
input.sort()
print(input)
median = int(input[(len(input) // 2)])
distance_sum = 0
for num in input:
    distance_sum += abs(median - int(num))
print(f"Median: {median}. Distance sum: {distance_sum}")
