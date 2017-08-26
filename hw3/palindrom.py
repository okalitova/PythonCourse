with open("input.txt", "r") as f:
    n = int(f.readline())
    d = {}
    text = f.readlines()

for line in text[:n]:
    line = line.lower().strip()
    letters = ''.join(sorted(line))
    if letters in d:
        d[letters] += [line]
    else:
        d[letters] = [line]

ans = []
for x in d:
    ans_line = sorted(list(set(d[x])))
    if len(ans_line) > 1:
        ans += [' '.join(ans_line)]

for x in sorted(ans):
    print(x)
