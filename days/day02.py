from helpers import *

d = get_aoc_data(day=2)


def part1():
    return sum(
        pw.count(letter) in interval(a, b)
        for a, b, letter, pw in d.parsed('<int>-<int> <>: <>')
    )


def part2():
    return sum(
        (pw[a-1] == letter) ^ (pw[b-1] == letter)
        for a, b, letter, pw in d.parsed('<int>-<int> <>: <>')
    )
