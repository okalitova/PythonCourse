import re

with open("input.txt", "r") as f:
    text = f.readlines()

ans = []
for i, line in enumerate(text):
    if i != len(text) - 1:
        line = line[:-1]
    words = re.split(r"\b(import|from)\b", line, re.MULTILINE)
    if len(words) > 1:
        j = 0
        while j < len(words):
            if words[j] == "from":
                word = words[j + 1].strip()
                if word[len(word) - 1] == ";":
                    word = word[:-1]
                ans.append(word)
                j = j + 3
            if words[j] == "import":
                word = words[j + 1].strip()
                if word[len(word) - 1] == ";":
                    word = word[:-1]
                ans.append(word)
                j = j + 1
            j = j + 1

ans = ', '.join(ans)
ans = ans.split(', ')
ans = ', '.join(sorted(set(ans)))
print(ans)
