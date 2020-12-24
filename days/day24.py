from helpers import *

test_data = Data("""\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""")

test_case(1, test_data, 10)
test_case(2, test_data, 2208)


direction_vectors = {
    'w': -1,
    'e': 1,
    'nw': -1-1j,
    'sw': 1j,
    'ne': -1j,
    'se': 1+1j,
}


neighbours = list(direction_vectors.values())
neighbours_and_self = neighbours + [0]


def part1_and_2(d: Data, ans: Answers) -> None:
    black_cells = ToggleSet()
    for i in d.lines:
        dirs = re.findall(r'se|ne|nw|sw|e|w', i)
        coord = 0
        for x in dirs:
            coord += direction_vectors[x]

        black_cells.toggle(coord)

    ans.part1 = len(black_cells)

    for _ in range(100):
        new_environment = black_cells.copy()
        handled = set()
        for c in black_cells:
            for n in neighbours_and_self:
                ref = c + n
                if ref in handled:
                    continue

                handled.add(ref)
                nblack = sum(ref + n in black_cells for n in neighbours)

                if ref in black_cells and (nblack == 0 or nblack > 2):
                    new_environment.discard(ref)

                if ref not in black_cells and nblack == 2:
                    new_environment.add(ref)

        black_cells = new_environment

    ans.part2 = len(black_cells)


run([1, 2], day=24, year=2020)
