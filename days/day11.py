from helpers import *

test_data = Data("""#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
""")

test_case(1, test_data, 37)
test_case(2, test_data, 26)


def part1(d: Data, ans: Answers) -> None:
    the_map = SparseMap(d.lines, default=lambda *a, **kw: '.')

    while True:
        changes = {}
        for y in the_map.rows:
            for x in the_map.columns:
                counts = neighbourhood_8_counts(x, y, lambda x, y: the_map[x, y])
                if the_map[x, y] == '#' and counts['#'] >= 4:
                    changes[x, y] = 'L'

                if the_map[x, y] == 'L' and not counts['#']:
                    changes[x, y] = '#'

        if not changes:
            break

        the_map.update(changes)

    ans.part1 = list(the_map.values()).count('#')


def part2(d: Data, ans: Answers) -> None:
    the_map = SparseMap(d.lines, default=lambda *a, **kw: '.')

    def trace_along(ox, oy, dx, dy):
        while True:
            ox += dx
            oy += dy
            if not the_map.is_inside(ox, oy):
                return '.'

            if (rv := the_map[ox, oy]) in 'L#':
                return rv

    def counts_along_star(ox, oy) -> Counter:
        c = Counter()
        for dx, dy in neighbourhood_8(0, 0):
            c[trace_along(ox, oy, dx, dy)] += 1

        return c

    while True:
        changes = {}

        for y in the_map.rows:
            for x in the_map.columns:
                counts = counts_along_star(x, y)
                if the_map[x, y] == '#' and counts['#'] >= 5:
                    changes[x, y] = 'L'

                if the_map[x, y] == 'L' and not counts['#']:
                    changes[x, y] = '#'

        if not changes:
            break

        the_map.update(changes)

    ans.part2 = list(the_map.values()).count('#')


run([1, 2], day=11, year=2020, submit=True)
