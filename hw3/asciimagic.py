import argparse

with open("input.txt", "r") as f:
    args = f.readline().split()
    command = args[0]
    args = args[1:]
    parser = argparse.ArgumentParser()
    if command == 'rotate':
        parser.add_argument("rotate", type=int)
    if command == 'expose':
        parser.add_argument("expose", type=int)
    if command == 'crop':
        parser.add_argument("-l", "--left", type=int, default=0)
        parser.add_argument("-r", "--right", type=int, default=0)
        parser.add_argument("-t", "--top", type=int, default=0)
        parser.add_argument("-b", "--bottom", type=int, default=0)
    args = parser.parse_args(args)
    text = f.readlines()

image = []
for i, line in enumerate(text):
    if i != len(text) - 1:
        line = line[:-1]
    image.append(line)

h = len(image)
w = 0
if h != 0:
    w = len(image[0])

if command == 'crop':
    for i in range(args.top, h - args.bottom):
        new_line = []
        for j in range(args.left, w - args.right):
            new_line.append(image[i][j])
        print(''.join(new_line))

if command == 'expose':
    intens = "@%#*+=-:. "
    image_intens = []
    for i in range(h):
        intens_line = []
        for j in range(w):
            for z in range(10):
                if intens[z] == image[i][j]:
                    if z + args.expose < 0:
                        intens_line.append(0)
                    elif z + args.expose > 9:
                        intens_line.append(9)
                    else:
                        intens_line.append(z + args.expose)
        image_intens.append(intens_line)

    new_image = []
    for i in range(h):
        new_line = []
        for j in range(w):
            new_line.append(intens[image_intens[i][j]])
        print(''.join(new_line))

if command == 'rotate':
    rotation = int(args.rotate / 90)
    for r in range(rotation):
        new_image = []
        for i in range(w):
            new_line = []
            for j in range(h):
                new_line.append(image[j][w - 1 - i])
            new_image.append(new_line)
        image = new_image
        h = len(image)
        w = 0
        if h != 0:
            w = len(image[0])

    for i in range(h):
        print(''.join(image[i]))