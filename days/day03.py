from helpers import *

d = get_aoc_data(day=3)
the_map = SparseRepeatingMap(d.lines)


def trees_along_slope(dx: int, dy: int) -> int:
    x = y = trees = 0
    while y < the_map.rows:
        trees += the_map[x, y] == '#'
        y += dy
        x += dx

    return trees


def part1():
    return trees_along_slope(3, 1)


def part2():
    return prod(starmap(trees_along_slope, [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))
