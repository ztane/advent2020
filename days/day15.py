from helpers import *

test_data = Data("""
0,3,6
""")

test_case(1, test_data, 436)
test_case(2, '3,1,2', 362)


def part1_and_2(d: Data, ans: Answers) -> None:
    numbers = d.extract_ints

    spoken_before = {}
    spoken = defaultdict(int)
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
            ans.part1 = new_number

        if turn == 30000000:
            ans.part2 = new_number
            return

        turn += 1


run([1, 2], day=15, year=2020)
