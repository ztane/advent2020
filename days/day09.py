from helpers import *

test_data = Data("""\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
""")

test_case(1, test_data, 127)
test_case(2, test_data, 62)


def part1_and_2(d: Data, ans: Answers) -> None:
    preamble = 25
    if d == test_data:
        preamble = 5

    numbers = d.extract_ints
    previous_set = set(numbers[:preamble])
    for i in count(preamble):
        current = numbers[i]
        for j in previous_set:
            if current - j in previous_set:
                break
        else:
            part1 = ans.part1 = current
            break

        previous_set.remove(numbers[i - preamble])
        previous_set.add(numbers[i])
    else:
        raise Exception("No solution for part 1")

    start = end = sliding_sum = 0
    while sliding_sum != part1:
        if sliding_sum < part1:
            sliding_sum += numbers[end]
            end += 1
        else:  # sliding_sum > part1:
            sliding_sum -= numbers[start]
            start += 1

    r = numbers[start:end]
    ans.part2 = min(r) + max(r)


run([1, 2], day=9, year=2020)
