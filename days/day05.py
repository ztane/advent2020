from helpers import *

d = get_aoc_data(day=5)


def part1_and_2():
    t = str.maketrans('FLBR', '0011')
    seat_ids = {int(bpass.translate(t), 2) for bpass in d.lines}
    missing = scalar(set(interval(min(seat_ids), max(seat_ids))) - seat_ids)
    return max(seat_ids), missing
