from helpers import *

d = get_aoc_data(day=1)
ints = sorted(d.extract_ints)


def part1():
    for a in (ia := fancyseqiter(ints)):
        for b in ia.copy(1):
            s = a + b
            if s > 2020:
                break

            if s == 2020:
                return a * b


def part2():
    for a in (ia := fancyseqiter(ints)):
        for b in (ib := ia.copy(1)):
            if a + b > 0.67 * 2020:
                break

            for c in ib.copy(1):
                s = a + b + c

                if s > 2020:
                    break

                if s == 2020:
                    return a * b * c
