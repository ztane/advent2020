from helpers import *

test_data = Data("""
0,3,6
""")

test_case(1, test_data, 436)
test_case(1, '1,3,2', 1)
test_case(1, '2,1,3', 10)
test_case(1, '2,3,1', 78)
test_case(1, '3,2,1', 438)
test_case(1, '3,1,2', 1836)


def part1(d: Data, ans: Answers) -> None:
    numbers = d.extract_ints

    spoken_before = {}
    spoken = defaultdict(int)
    spoken_in_order = [None] + list(numbers)
    spoken_counter = Counter()

    for i, e in enumerate(numbers, 1):
        spoken[e] = i
        spoken_counter[e] += 1
        last_one = e

    turn = i + 1
    while True:
        if spoken_counter[last_one] == 1:
            new_number = 0
        else:
            new_number = spoken[last_one] - spoken_before[last_one]

        if new_number in spoken:
            spoken_before[new_number] = spoken[new_number]

        spoken[new_number] = turn
        spoken_counter[new_number] += 1
        last_one = new_number
        if turn == 2020:
            break

        turn += 1

    ans.part1 = new_number


def part2(d: Data, ans: Answers) -> None:
    numbers = d.extract_ints

    spoken_before = {}
    spoken = defaultdict(int)
    spoken_in_order = [None] + list(numbers)
    spoken_counter = Counter()

    for i, e in enumerate(numbers, 1):
        spoken[e] = i
        spoken_counter[e] += 1
        last_one = e

    turn = i + 1
    while True:
        if spoken_counter[last_one] == 1:
            new_number = 0
        else:
            new_number = spoken[last_one] - spoken_before[last_one]

        if new_number in spoken:
            spoken_before[new_number] = spoken[new_number]

        spoken[new_number] = turn
        spoken_counter[new_number] += 1
        last_one = new_number
        if turn == 30000000:
            break

        turn += 1

    ans.part2 = new_number


run([2], day=15, year=2020, submit='force')
