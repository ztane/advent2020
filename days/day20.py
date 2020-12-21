import numpy as np
import scipy.ndimage.morphology

from helpers import *

DEBUG = False

test_data = Data("""\n
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
""")

test_case(1, test_data, 20899048083289)
test_case(2, test_data, 273)


sea_monster = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """.splitlines()

seamonster_stamp = np.zeros([3, 20], dtype=bool)
for y, line in enumerate(sea_monster):
    for x, c in enumerate(line):
        seamonster_stamp[y, x] = c == '#'


def part1(d: Data, ans: Answers) -> None:
    all_sides = []
    tiles_and_sides = {}
    side_counts = Counter()
    for tile in d.split('\n\n'):
        num, = Parser('Tile <int>:')(tile.lines[0])
        tile = SparseMap(tile.lines[1:])

        sides = [
            tuple(tile[0, r] for r in tile.rows),
            tuple(tile[tile.rows - 1, r] for r in tile.rows),
            tuple(tile[r, 0] for r in tile.rows),
            tuple(tile[r, tile.rows - 1] for r in tile.rows),
        ]

        sides = sides + [
            i[::-1] for i in sides
        ]

        all_sides.extend(sides)
        tiles_and_sides[num] = sides
        side_counts.update(sides)

    all_side_set = set(all_sides)
    ans.part1 = (prod(sorted(tiles_and_sides, key=lambda x:
                      sum(side_counts[i] for i in tiles_and_sides[x]))[:4]))


def part2(d: Data, ans: Answers) -> None:
    class Tile(SparseMap):
        id: int

        def __init__(self, id: int, lines=None, size=None):
            if lines:
                super().__init__(lines)
            else:
                super().__init__()

            if size:
                self.rows = self.columns = IterableInt(size)

            self.id = id

        def __hash__(self):
            return self.id

        def __eq__(self, other):
            if not isinstance(other, Tile):
                return False

            return other.id == self.id

        @reify
        def sides(self):
            sides = [
                tuple(self[0, r] for r in self.rows),
                tuple(self[self.rows - 1, r] for r in self.rows),
                tuple(self[r, 0] for r in self.rows),
                tuple(self[r, self.rows - 1] for r in self.rows),
            ]

            sides = sides + [
                i[::-1] for i in sides
            ]

            return sides

        def get_left_side(self):
            return tuple(self[0, r] for r in self.rows)

        def get_upside(self):
            return tuple(self[r, 0] for r in self.rows)

        def get_flipped(self):
            flipped_tile = Tile(self.id, size=self.rows)
            for y in self.rows:
                for x in self.columns:
                    flipped_tile[x, y] = self[x, self.rows - y - 1]

            return flipped_tile

        def rotate_90(self):
            rotated_tile = Tile(self.id, size=self.rows)
            for y in self.rows:
                for x in self.columns:
                    rotated_tile[x, y] = self[self.rows - y - 1, x]

            return rotated_tile

        def get_rotated(self, rotation, flipped=False):
            current = self
            if flipped:
                current = self.get_flipped()

            for i in range(rotation):
                current = current.rotate_90()

            return current

        def place_corner(self, map):
            found = False
            for f in [False, True]:
                for r in range(4):
                    rotation = self.get_rotated(r, f)
                    if side_counts[rotation.get_left_side()] == 1 and \
                        side_counts[rotation.get_upside()] == 1:
                            rotation.draw_at(map, 0, 0)
                            return

            raise ValueError('NO VALID CORNER ROTATION FOUND')

        def draw_at(self, map, x, y):
            for dy in self.rows:
                for dx in self.columns:
                    map[x + dx, y + dy] = self[dx, dy]

        def find_rotation(self, left_edge, top_edge):
            for f in [False, True]:
                for r in range(4):
                    tile = self.get_rotated(r, f)
                    if left_edge and tile.get_left_side() == left_edge \
                        or top_edge and tile.get_upside() == top_edge:
                        return tile

            raise ValueError('Rotation not found')

    all_sides = []
    tiles_and_sides = {}
    side_counts: Dict[Tuple[str, ...], int] = Counter()

    sides_to_tiles: Dict[Tuple[str, ...], typing.Set[Tile]] = defaultdict(set)
    tiles = {}

    for tile in d.split('\n\n'):
        num, = Parser('Tile <int>:')(tile.lines[0])
        tile = Tile(num, tile.lines[1:])

        sides = tile.sides
        all_sides.extend(sides)
        tiles_and_sides[num] = sides
        side_counts.update(sides)
        tiles[num] = tile

        for side in sides:
            sides_to_tiles[side].add(tile)

    all_side_set = set(all_sides)
    corner = min(tiles_and_sides, key=lambda x:
                 sum(side_counts[i] for i in tiles_and_sides[x]))

    mega_grid_size = IterableInt(sqrt(len(tiles_and_sides)))

    mega_square = SparseMap(default=' ')
    corner_tile = tiles[corner]
    corner_tile.place_corner(mega_square)

    tile_size = corner_tile.rows
    mega_square.rows = mega_square.columns = IterableInt(mega_grid_size * corner_tile.rows)

    used_tiles: typing.Set[Tile] = {corner_tile}

    def place_tile(x, y):
        left_edge = tuple(mega_square[x - 1, y + i] for i in range(tile_size))
        top_edge = tuple(mega_square[x + i, y - 1] for i in range(tile_size))

        if ' ' in left_edge:
            left_edge = None

        if ' ' in top_edge:
            top_edge = None

        assert left_edge or top_edge
        the_edge = left_edge or top_edge

        next_possible = sides_to_tiles[the_edge]
        for t in next_possible:
            if t not in used_tiles:
                break
        else:
            raise ValueError('No next tile to lay')

        to_lay_out = t.find_rotation(left_edge=left_edge, top_edge=top_edge)
        to_lay_out.draw_at(mega_square, x, y)
        used_tiles.add(to_lay_out)

    for y in range(0, mega_square.rows, tile_size):
        for x in range(0, mega_square.rows, tile_size):
            if x == y == 0:
                continue

            place_tile(x, y)

    tgt_y = 0

    seamonster_map = SparseMap(default=' ')
    max_x = 0
    for y in range(0, mega_square.rows):
        tgt_x = 0
        if y % tile_size == 0 or y % tile_size == tile_size - 1:
            continue

        tgt_y += 1
        for x in range(0, mega_square.columns):
            if x % tile_size == 0 or x % tile_size == tile_size - 1:
                continue

            seamonster_map[tgt_x, tgt_y] = mega_square[x, y]
            tgt_x += 1
            max_x = max(max_x, tgt_x)


    seamonster_map.rows = IterableInt(tgt_y + 1)
    seamonster_map.columns = IterableInt(max_x + 1)

    np_image = np.zeros([seamonster_map.rows,
                               seamonster_map.columns],
                              dtype=bool)
    for y in seamonster_map.rows:
        for x in seamonster_map.columns:
            np_image[x, y] = seamonster_map[x, y] == '#'

    seamonsters_drawn = np.zeros(np_image.shape, dtype=bool)

    for flipped in [False, True]:
        seam = seamonster_stamp
        if flipped:
            seam = np.fliplr(seam)

        for rotation in range(4):
            new_seamons = scipy.ndimage.morphology.binary_opening(
                np_image,
                seam
            )

            seamonsters_drawn |= new_seamons
            seam = np.rot90(seam)

    if DEBUG:
        import matplotlib.pyplot as plt
        plt.imshow(seamonsters_drawn)
        plt.show()

    ans.part2 = np.count_nonzero(np_image ^ seamonsters_drawn)


run([1, 2], day=20, year=2020, submit=False)
