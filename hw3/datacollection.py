#!/usr/bin/env python3

import re
from random import uniform
import argparse
import unittest


def get_tokens(line):
    tokens = re.findall("\d+|[a-zA-Zа-яА-Я]+|.", line)
    word_tokens = re.findall("\w+", line)
    return tokens, word_tokens


def get_probabilities(depth, word_tokens):
    probabilities = {}
    for d in range(depth + 1):
        for line_tokens in word_tokens:
            for i in range(len(line_tokens) - d):
                history = ' '.join(line_tokens[i:i+d])
                word = line_tokens[i + d]
                if history in probabilities:
                    if word in probabilities[history]:
                        probabilities[history][word] = probabilities[history][word] + 1
                    else:
                        probabilities[history][word] = 1
                else:
                    probabilities[history] = {word: 1}
    for history in probabilities:
        cnt = 0
        for word in probabilities[history]:
            cnt = cnt + probabilities[history][word]
        for word in probabilities[history]:
            probabilities[history][word] = probabilities[history][word] / cnt
    return probabilities


def probabilities(depth, word_tokens):
    prob = get_probabilities(depth, word_tokens)
    for history in sorted(prob):
        print(history)
        for word in sorted(prob[history]):
            print("  " + word + ': ' + "%.2f" % prob[history][word])


def generate(depth, size, word_tokens):
    prob = get_probabilities(depth, word_tokens)
    punctuation = {'.': 0.6, ',': 0.3, '-': 0.03, ':': 0.03, '!': 0.02, '?': 0.02}
    word_probability = 0.85
    text = []
    sentence_words = []

    if len(word_tokens) == 0:
        return ''

    word_patter = re.compile("\w+")

    for i in range(size):
        history = []
        max_depth = min(len(sentence_words), depth)
        for j in range(max_depth):
            history.append(sentence_words[len(sentence_words) - max_depth + j])
        for j in range(max_depth):
            if ' '.join(history) in prob:
                break
            else:
                history = history[1:]
        history = ' '.join(history)
        is_word = uniform(0, 1) < word_probability or len(text) < 1
        if len(text) >= 1:
            is_word = is_word or (not word_patter.match(text[len(text) - 1][-1]))
        if is_word:
            rand = uniform(0, 1)
            value = 0
            for i, word in enumerate(prob[history]):
                value = value + prob[history][word]
                if value >= rand or i == len(prob[history]) - 1:
                    if len(sentence_words) != 0:
                        text.append(word)
                    else:
                        text.append(word[0].upper() + word[1:])
                    sentence_words.append(word)
                    break
        else:
            rand = uniform(0, 1)
            value = 0
            for i, pun in enumerate(punctuation):
                value = value + punctuation[pun]
                if value >= rand or i == len(punctuation) - 1:
                    text[len(text) - 1] = text[len(text) - 1] + pun
                    if pun == '.':
                        sentence_words = []
                    break
    if not word_patter.match(text[len(text) - 1][-1]):
        return ' '.join(text)[:-1] + '.'
    return ' '.join(text) + '.'


class TestTokenize(unittest.TestCase):

    def test_get_tokens(self):
        line = "kek5kek? ooops123!   bbbbhbhbv@fdf67? lalka.azaza@gmail.com"
        tokens = ["kek", "5", "kek", "?", " ", "ooops", "123",
                  "!", " ", " ", " ", "bbbbhbhbv", "@", "fdf",
                  "67", "?", " ", "lalka", ".", "azaza", "@", "gmail", ".", "com"]
        actual_tokens = get_tokens(line)[0]
        self.assertEqual(tokens, actual_tokens)

    def test_get_tokens_empty(self):
        line = ""
        self.assertEqual(get_tokens(line)[0], [])


class TestProbabilities(unittest.TestCase):

    def test_get_probabilities(self):
        tokens = [["0", "1", "2", "3"],
                  ["1", "4", "5", "1"],
                  ["5", "0", "0", "1", "7"]]
        d = {"": {"0": 0.23, "1": 0.31, "2": 0.08, "3": 0.08, "4": 0.08, "5": 0.15, "7": 0.08}}
        actual_d = get_probabilities(0, tokens)
        for h in d:
            for w in d[h]:
                actual_d[h][w] = round(actual_d[h][w], 2)
        self.assertEqual(d, actual_d)

    def test_get_probabilities_empty(self):
        tokens = []
        d = {}
        self.assertEqual(get_probabilities(5, tokens), d)


class TestGenerate(unittest.TestCase):

    def test_generate(self):
        tokens = [["0", "1", "2", "3"],
                  ["1", "4", "5", "1"],
                  ["5", "0", "0", "1", "7"]]
        d = {"": {"0": 0.23, "1": 0.31, "2": 0.08, "3": 0.08, "4": 0.08, "5": 0.15, "7": 0.08}}
        text = generate(2, 10, tokens)

        self.assertEqual(text[-1], ".")
        for i, t in enumerate(text):
            if t in {'.', ',', '-', '?', '!', ':'} and i != len(text) - 1:
                self.assertEqual(text[i + 1], " ")

    def test_generate_empty(self):
        tokens = []
        text = generate(2, 10, tokens)
        self.assertEqual(text, "")


def main(filename):

    with open(filename, "r") as f:

        args = f.readline().split()
        command = args[0]

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        parser_probabilities = subparsers.add_parser("probabilities")
        parser_probabilities.add_argument("--depth", type=int, default=0)

        parser_generate = subparsers.add_parser("generate")
        parser_generate.add_argument("--size", type=int, default=0)
        parser_generate.add_argument("--depth", type=int, default=0)

        parser_tokenize = subparsers.add_parser("tokenize")

        parser_test = subparsers.add_parser("test")

        args = parser.parse_args(args)
        if command == "test":
            unittest.main()
        else:
            tokens = []
            word_tokens = []
            for line in f.readlines():
                tokens.append(get_tokens(line)[0])
                word_tokens.append(get_tokens(line)[1])

            if command == "tokenize":
                for t in tokens:
                    print('\n'.join(t))

            if command == "probabilities":
                probabilities(args.depth, word_tokens)

            if command == "generate":
                text = generate(args.depth, args.size, word_tokens)
                with open('final', 'w') as output:
                    output.write(text)


if __name__ == '__main__':
    main("input.txt")
