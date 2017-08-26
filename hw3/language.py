with open("input.txt", "r") as f:
    text = f.readlines()
    d = {}
    first = True
    second = False
    for line in text:
        line = line[:-1]
        words = line.split(" ")
        if len(words) == 2 and first:
            d[words[0]] = set(words[1])
        else:
            first = False
            second = True

        languages = set()
        if len(words) > 0 and second:
            for word in words:
                word = word.lower()
                count = {}
                for key in d:
                    for letter in word:
                        if letter in d[key]:
                            if key in count:
                                count[key] += 1
                            else:
                                count[key] = 1
                l = zip(count.values(), count.keys())

                def cmp(elem):
                    return [-elem[0], elem[1]]

                l = sorted(l, key=cmp)
                if len(l) > 0:
                    languages.add(l[0][1])
            print(' '.join(sorted(list(languages))))
