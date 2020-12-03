from helpers import *

d = get_aoc_data(day=3)
the_map = SparseRepeatingComplexMap(d.lines)


def trees_along_slope(delta: complex) -> int:
    p = trees = 0
    while p.imag < the_map.rows:
        trees += the_map[p] == '#'
        p += delta

    return trees


def part1():
    return trees_along_slope(3+1j)


def part2():
    return prod(map(trees_along_slope, [1+1j, 3+1j, 5+1j, 7+1j, 1+2j]))
