from helpers import *


def part1_and_2(d: Data, ans: Answers) -> None:
    numbers = d.extract_ints

    assert(len(set(numbers)) == len(numbers))

    seen_at = {}
    for i, e in enumerate(numbers, 1):
        seen_at[e] = i

    # because of the set invariant above
    current_number = 0

    for turn in count(len(numbers) + 1):
        try:
            new_number = turn - seen_at[current_number]
        except:
            new_number = 0

        seen_at[current_number] = turn
        if turn == 2020:
            ans.part1 = current_number

        elif turn == 30000000:
            ans.part2 = current_number
            return

        current_number = new_number


run([1, 2], day=15, year=2020)
