from helpers import *

test_data = """\
939
7,13,x,x,59,x,31,19
"""

test_case(2, test_data, 1068781)
test_case(1, test_data, 295)
test_case(2, "1\n17,x,13,19", 3417)
test_case(2, "1\n67,7,59,61", 754018)
test_case(2, "1\n67,x,7,59,61", 779210)
test_case(2, "1\n67,7,x,59,61", 1261476)
test_case(2, "1\n1789,37,47,1889", 1202161486)


def part1(d: Data, ans: Answers) -> None:
    ts = d.lines[0].as_int
    buses = d.lines[1].extract_ints

    waits = [(-ts % bus_id, bus_id) for bus_id in buses]
    ans.part1 = prod(min(waits))  # !!


def part2(d: Data, ans: Answers) -> None:
    buses_and_offsets = [(int(bus), -offset % int(bus))
                         for (offset, bus) in enumerate(d.lines[1].split(','))
                         if bus.isdigit()]

    ans.part2 = crt(buses_and_offsets).lowest


run([1, 2], day=13, year=2020)
