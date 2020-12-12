from helpers import *

test_data = Data("""\
F10
N3
F7
R90
F11
"""
)

test_data2 = Data("""\
N10
W10
E10
S10
F10
L180
F10
"""
)

test_case(1, test_data, 25)
test_case(1, test_data2, 0)
test_case(2, test_data, 286)


def part1(data: Data, ans: Answers) -> None:
    position = 0
    direction = cdir.parse("E1")

    for action, number in data.parsed("<chr><int>"):
        if action in "NSWE":
            position += cdir.compass(action, number)

        elif action in "LR":
            direction = cdir.rotate_degrees(direction, action, number)

        elif action == "F":
            position += number * direction

        else:
            ValueError("Unexpected direction")

    ans.part1 = cmanhattan(position)


def part2(data: Data, ans: Answers) -> None:
    waypoint = cdir.parse("E10 N1")
    ship = 0

    for action, number in data.parsed("<chr><int>"):
        if action in "NSWE":
            waypoint += cdir.compass(action, number)

        elif action in "LR":
            waypoint = cdir.rotate_degrees(waypoint, action, number)

        elif action == "F":
            ship += number * waypoint

        else:
            ValueError("Unexpected action")

    ans.part2 = cmanhattan(ship)


run([1, 2], day=12, year=2020, submit=True)
