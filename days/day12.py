from helpers import *

test_data = Data("""\
F10
N3
F7
R90
F11
""")

test_case(1, test_data, 25)
test_case(2, test_data, 286)


def part1(data: Data, ans: Answers) -> None:
    pos = 0, 0
    d = 1, 0
    for i in data.lines:
        l, n = i[0], i[1:]
        n = int(n)

        if l == 'N':
            pos = pos[0], pos[1] - n

        elif l == 'S':
            pos = pos[0], pos[1] + n

        elif l == 'E':
            pos = pos[0] + n, pos[1]

        elif l == 'W':
            pos = pos[0] - n, pos[1]

        elif l == 'R':
            for i in range(n // 90):
                d = -d[1], d[0]

        elif l == 'L':
            for i in range(n // 90):
                d = d[1], -d[0]

        elif l == 'F':
            pos = pos[0] + n * d[0], pos[1] + n * d[1]

        else:
            ValueError

    ans.part1 = manhattan(*pos)


def part2(data: Data, ans: Answers) -> None:
    pos = 10, -1
    ship = 0, 0

    for i in data.lines:
        l, n = i[0], i[1:]
        n = int(n)

        if l == 'N':
            pos = pos[0], pos[1] - n

        elif l == 'S':
            pos = pos[0], pos[1] + n

        elif l == 'E':
            pos = pos[0] + n, pos[1]

        elif l == 'W':
            pos = pos[0] - n, pos[1]

        elif l == 'R':
            for i in range(n // 90):
                pos = -pos[1], pos[0]

        elif l == 'L':
            for i in range(n // 90):
                pos = pos[1], -pos[0]

        elif l == 'F':
            ship = ship[0] + n * pos[0], ship[1] + n * pos[1]

        else:
            ValueError

    ans.part2 = manhattan(*ship)


run([1, 2], day=12, year=2020, submit=True)
