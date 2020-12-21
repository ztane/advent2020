from helpers import *

test_data_for_part1 = Data("""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")

test_case(1, test_data_for_part1, 4)

test_data_for_part2 = Data("""
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""")

test_case(2, test_data_for_part2, 126)


def part1_and_2(d: Data, ans: Answers) -> None:
    containers = defaultdict(set)
    contents = defaultdict(Counter)

    colour_parser = Parser('<int> <> bag<*>')

    for colour, others in d.parsed_lines('<> bags contain <>.'):
        for other in others.stripsplit(','):
            if colour_parser(other):
                n, c = colour_parser
                containers[c].add(colour)
                contents[colour][c] = n

    def trace_containers(current_bags: set):
        return current_bags.union(
            *(trace_containers(containers[colour]) for colour in current_bags)
        )

    def count_contents(current_contents: Counter):
        return (sum(current_contents.values())
                + sum(number * count_contents(contents[colour])
                      for (colour, number) in current_contents.items()))

    ans.part1 = len(trace_containers(containers['shiny gold']))
    ans.part2 = count_contents(contents['shiny gold'])


run([1, 2], day=7, year=2020)
