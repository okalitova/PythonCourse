with open("input.txt", encoding='utf-8') as f:
    x = [int(x) for x in next(f).split()][0]
    l = f.readlines()

l = [f.strip().lower() for f in l]
l = l[:x]
d = {}
for a in l:
    word = ''.join(sorted(list(a)))
    if word == '':
        continue
    if word in d:
        d[word] += [a]
    else:
        d[word] = [a]

x = []
for i in d:
    s = sorted(list(set(d[i])))
    if len(s) > 1:
        x += [' '.join(s)]

for i in sorted(x):
    print(i)