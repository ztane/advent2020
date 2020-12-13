from helpers import *

test_data = Data("""\
939
7,13,x,x,59,x,31,19
""")

test_case(1, test_data, 295)
test_case(2, test_data, 1068781)
test_case(2, Data("1\n1789,37,47,1889"), 1202161486)


def part1(d: Data, ans: Answers) -> None:
    ts, = d.lines[0].extract_ints
    buses = d.lines[1].extract_ints

    waits = [(-(ts % -bus_id), bus_id) for bus_id in buses]
    ans.part1 = prod(min(waits))  # !!


def part2(d: Data, ans: Answers) -> None:
    # sort by bus id in reverse so that we reach maximum increment fastest
    buses = sorted([
        (int(item), offset)
        for (offset, item) in enumerate(d.lines[1].split(','))
        if item != 'x'
    ], reverse=True)

    increment = 1
    timestamp = 0

    # now the trick. The increment will be the lcm() of the buses that
    # we've synced at the given timestamp. As buses are synced, they can be
    # removed from the list. No head-aching math.
    while buses:
        timestamp += increment
        newly_synced = set()
        for bus_id, offset in buses:
            if (timestamp + offset) % bus_id == 0:
                newly_synced.add(bus_id)
                increment = lcm(increment, bus_id)

        if newly_synced:
            # filter to speed up increments
            buses = [bus for bus in buses if bus[0] not in newly_synced]

    ans.part2 = timestamp


run([1, 2], day=13, year=2020, submit=False)
