from helpers import *


def part1(d: Data, ans: Answers):
    ans.part1 = sum(
        pw.count(letter) in interval(a, b)
        for a, b, letter, pw in d.parsed_lines('<int>-<int> <>: <>')
    )


def part2(d: Data, ans: Answers):
    ans.part2 = sum(
        (pw[a-1] == letter) ^ (pw[b-1] == letter)
        for a, b, letter, pw in d.parsed_lines('<int>-<int> <>: <>')
    )


run([1, 2], day=2, year=2020)