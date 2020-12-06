from helpers import *


def part1(d: Data, ans: Answers):
    ints = sorted(d.as_ints)
    for a in (ia := fancyseqiter(ints)):
        for b in ia.copy(1):
            s = a + b
            if s > 2020:
                break

            if s == 2020:
                ans.part1 = a * b
                return


def part2(d: Data, ans: Answers):
    ints = sorted(d.as_ints)
    for a in (ia := fancyseqiter(ints)):
        for b in (ib := ia.copy(1)):
            if a + b > 0.67 * 2020:
                break

            for c in ib.copy(1):
                s = a + b + c

                if s > 2020:
                    break

                if s == 2020:
                    ans.part2 = a * b * c
                    return


run([1, 2], day=1, year=2020)
