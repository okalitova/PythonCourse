import re

with open("input.txt", "r") as f:
    text = f.readlines()

for i, line in enumerate(text):
    if i != len(text) - 1:
        line = line[:-1]
    pattern1 = re.compile("\d{2}[.]\d{2}[.]\d{4}$")
    pattern2 = re.compile("\d{2}[/]\d{2}[/]\d{4}$")
    pattern3 = re.compile("\d{2}[-]\d{2}[-]\d{4}$")
    pattern4 = re.compile("\d{4}[.]\d{2}[.]\d{2}$")
    pattern5 = re.compile("\d{4}[/]\d{2}[/]\d{2}$")
    pattern6 = re.compile("\d{4}[-]\d{2}[-]\d{2}$")
    pattern7 = re.compile("\d{1,2}\s*[а-яА-Я]+\s*\d{4}$", re.IGNORECASE)

    res1 = pattern1.match(line)
    res2 = pattern2.match(line)
    res3 = pattern3.match(line)
    res4 = pattern4.match(line)
    res5 = pattern5.match(line)
    res6 = pattern6.match(line)
    res7 = pattern7.match(line)

    if res1 is not None or res2 is not None or res3 is not None \
            or res4 is not None or res5 is not None or res6 is not None or res7 is not None:
        print("YES")
    else:
        print("NO")
