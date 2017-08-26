import sys

filename = "pi.txt"

with open(filename) as f:
    digits = f.read()[2:]

digits = "".join(digits.split("\n"))

sub_digits = sys.stdin.readline()[:-1]

indices = []
index = -1  
while True:
    index = digits.find(sub_digits, index + 1)
    if index == -1:  
        break
    indices.append(index)
print(len(indices), indices[:5])
