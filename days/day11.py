from helpers import *

test_data = Data("""\
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""")

test_case(1, test_data, 37)
test_case(2, test_data, 26)


def solve(seat_map,
          seat_coordinates,
          neighbourhoods,
          intolerable_neighbour_count):
    while True:
        changes = {}
        for seat in seat_coordinates:
            if (seat_state := seat_map[seat]) in 'L#':
                occupied_count = sum(
                    seat_map[neighbour] == '#'
                    for neighbour in neighbourhoods[seat]
                )

                if (seat_state == '#' and
                        occupied_count >= intolerable_neighbour_count):
                    changes[seat] = 'L'

                elif seat_state == 'L' and occupied_count == 0:
                    changes[seat] = '#'

        if not changes:
            break

        seat_map.update(changes)

    return list(seat_map.values()).count('#')


def part1_and_2(d: Data, ans: Answers) -> None:
    seat_map_part1 = SparseMap(d.lines, default='.')
    seat_map_part2 = SparseMap(d.lines, default='.')

    seat_coordinates: List[Tuple[int, int]] = [
        pos for pos in product(seat_map_part1.columns, seat_map_part1.rows)
        if seat_map_part1[pos] == 'L'
    ]

    p1_neighbours: Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(
        list, {
            seat: neighbourhood_8(
                *seat, lambda nx, ny: seat_map_part1[nx, ny] == 'L'
            )
            for seat in seat_coordinates
        })

    def trace_along(ox: int, oy: int, dx: int, dy: int) -> Optional[
        Tuple[int, int]
    ]:
        while True:
            ox += dx
            oy += dy
            if not seat_map_part2.is_inside(ox, oy):
                return None

            if seat_map_part2[ox, oy] == 'L':
                return ox, oy

    def star_neighbours(ox, oy) -> List[Tuple[int, int]]:
        seats = []
        for dx, dy in neighbourhood_8(0, 0):
            if neighbouring_seat := trace_along(ox, oy, dx, dy):
                seats.append(neighbouring_seat)

        return seats

    p2_neighbours: Dict[Tuple[int, int], List[Tuple[int, int]]]
    p2_neighbours = {
        seat: star_neighbours(*seat)
        for seat in seat_coordinates
    }

    ans.part1 = solve(seat_map_part1, seat_coordinates, p1_neighbours, 4)
    ans.part2 = solve(seat_map_part2, seat_coordinates, p2_neighbours, 5)


run([1, 2], day=11, year=2020, submit=True)
