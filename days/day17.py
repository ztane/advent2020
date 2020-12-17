from helpers import *

test_data = Data("""\
.#.
..#
###
""")

test_case(1, test_data, 112)
test_case(2, test_data, 848)


def create_initial_map(d: Data, dimensions: int) -> typing.Set[Tuple[int, ...]]:
    dimensional_map = set()
    zeroes_to_add = (0,) * (dimensions - 2)

    for y, row in enumerate(d.lines):
        for x, cell in enumerate(row):
            if cell == '#':
                dimensional_map.add((x, y) + zeroes_to_add)

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
def multid_neighbourhood(coord, n, self):
    return list(neighbour_generator(coord, n=n, self=self))


def solve_for(d: Data, dimensions: int, iterations: int = 6) -> int:
    the_map = create_initial_map(d, dimensions)

    for iteration in range(iterations):
        new_map = set()
        handled = set()
        for coord in the_map:
            for neighbour in multid_neighbourhood(coord, dimensions, True):
                if neighbour in handled:
                    continue

                handled.add(neighbour)

                occupied_neighbours_count = sum(
                    1
                    for c in multid_neighbourhood(
                        neighbour, dimensions, False)
                    if c in the_map
                )

                if ((occupied_neighbours_count == 2 and neighbour in the_map) or
                        occupied_neighbours_count == 3):
                    new_map.add(neighbour)

        the_map = new_map

    return len(the_map)


def part1(d: Data, ans: Answers) -> None:
    ans.part1 = solve_for(d, 3)


def part2(d: Data, ans: Answers) -> None:
    ans.part2 = solve_for(d, 4)


run([1, 2], day=17, year=2020)
