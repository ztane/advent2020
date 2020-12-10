from helpers import *

test_data = Data("""\
16
10
15
5
1
11
7
19
6
12
4
""")

test_data2 = Data("""
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""")

test_case(1, test_data, 7 * 5)
test_case(1, test_data2, 22 * 10)
test_case(2, test_data, 8)
test_case(2, test_data2, 19208)


def joltage_list(d: Data) -> List[int]:
    joltages = sorted([0, *d.extract_ints])
    return [*joltages, max(joltages) + 3]


def diff_list(d: Data) -> List[int]:
    return list(difference(joltage_list(d)))[1:]


def part1(d: Data, ans: Answers) -> None:
    diffs = diff_list(d)
    ans.part1 = diffs.count(1) * diffs.count(3)


def part2(d: Data, ans: Answers) -> None:
    joltages = joltage_list(d)
    len_joltages = len(joltages)

    @lru_cache(maxsize=len(joltages))
    def count_from_position(i):
        # only one way because last diff is 3
        if i >= len_joltages - 2:
            return 1

        ct = 0
        current_joltage = joltages[i]
        for next_p in count(i + 1):
            if next_p >= len_joltages or joltages[next_p] > current_joltage + 3:
                break

            ct += count_from_position(next_p)

        return ct

    ans.part2 = count_from_position(0)


run([1, 2], day=10, year=2020)
