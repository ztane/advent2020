from helpers import *


def part1_and_2(d: Data, ans: Answers):
    the_map = SparseRepeatingComplexMap(d.lines)

    def trees_along_slope(delta: complex) -> int:
        p = trees = 0
        while p.imag < the_map.rows:
            trees += the_map[p] == '#'
            p += delta

        return trees

    ans.part1 = trees_along_slope(3 + 1j)
    ans.part2 = prod(
        map(
            trees_along_slope,
            [1 + 1j, 3 + 1j, 5 + 1j, 7 + 1j, 1 + 2j]
        )
    )


run([1, 2], day=3, year=2020)
