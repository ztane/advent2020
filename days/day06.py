from helpers import *

test_data = Data("""
abc

a
b
c

ab
ac

a
a
a
a

b
""")

test_case(1, test_data, 11)
test_case(2, test_data, 6)


def part1(input_data: Data, answers: Answers):
    answers.part1 = sum(
        len(set(group.without_spaces))
        for group in input_data.split('\n\n')
    )


def part2(input_data: Data, answers: Answers):
    answers.part2 = sum(
        len(intersection(group.lines))
        for group in input_data.split('\n\n')
    )


run([1, 2], day=6, year=2020)
