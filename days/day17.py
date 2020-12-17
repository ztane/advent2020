from helpers import *

test_data = Data("""\
.#.
..#
###
""")

test_case(1, test_data, 112)
test_case(2, test_data, 848)


def create_initial_map(d: Data, dimensions: int):
    twod_map = SparseMap(d.lines)
    dimensional_map = defaultdict(bool)
    zeroes_to_add = (0,) * (dimensions - 2)

    for (c, v) in twod_map.items():
        if v == '#':
            dimensional_map[c + zeroes_to_add] = True

    return dimensional_map


def neighbour_generator(coord, *, n, self=False):
    zero = ('dummy',)
    if not self:
        zero = (0,) * n

    for delta in product(interval(-1, 1), repeat=n):
        if delta == zero:
            continue

        yield tuple(i + j for (i, j) in zip(delta, coord))


@lru_cache(None)
def cached_neighbours(coord, n, self):
    return list(neighbour_generator(coord, n=n, self=self))


def solve_for(d: Data, dimensions: int) -> int:
    the_map = create_initial_map(d, dimensions)

    for iteration in range(6):
        new_map = defaultdict(bool)
        handled = set()
        for coord, val in list(the_map.items()):
            for neighbour in cached_neighbours(coord, dimensions, True):
                if neighbour in handled:
                    continue

                handled.add(neighbour)

                occupied_neighbours_count = sum(the_map[c]
                                                for c in cached_neighbours(neighbour, dimensions, False))
                if ((the_map[neighbour] and occupied_neighbours_count == 2) or
                    occupied_neighbours_count == 3):
                    new_map[neighbour] = True

        the_map = new_map

    return sum(the_map.values())


def part1(d: Data, ans: Answers) -> None:
    ans.part1 = solve_for(d, 3)


def part2(d: Data, ans: Answers) -> None:
    ans.part2 = solve_for(d, 4)


run([1, 2], day=17, year=2020, submit=False)
