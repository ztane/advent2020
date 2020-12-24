from helpers import *

test_data = Data("""
389125467
""")

test_case(1, test_data, 67384529)
test_case(2, test_data, 149245887792)


class CupNode:
    __slots__ = ['num', 'next']
    num: int
    next: 'CupNode'

    def __init__(self, num):
        self.num = num

    def pop_next(self):
        rv = self.next
        self.next = rv.next
        return rv

    def link(self, after):
        self.next = after.next
        after.next = self

    def __str__(self):
        return f'C{self.num}'


def iterate(start, iterations, max_cup, node_map):
    current = start
    for i in range(iterations):
        cup1 = current.pop_next()
        cup2 = current.pop_next()
        cup3 = current.pop_next()

        if i and i % 100000 == 0:
            print(i)

        target = current.num - 1
        if target == 0:
            target = max_cup

        while target in [cup1.num, cup2.num, cup3.num]:
            target -= 1
            if target == 0:
                target = max_cup

        current = current.next
        target_node = node_map[target]
        cup3.link(target_node)
        cup2.link(target_node)
        cup1.link(target_node)


def make_ring_list(items: List[int], node_map: List[CupNode]) -> CupNode:
    start: Optional[CupNode] = None
    prev: Optional[CupNode] = None
    max_cup = 0
    for i in items:
        node = CupNode(i)
        if prev:
            prev.next = node

        prev = node
        if start is None:
            start = node

        node_map[i] = node
        max_cup = max(i, max_cup)

    node.next = start
    return start


def part1(d: Data, ans: Answers) -> None:
    max_cup = 9
    node_map: List[CupNode] = [None] * (max_cup + 1)
    start = make_ring_list(list(map(int, d)), node_map)

    iterate(start, 100, max_cup, node_map)

    one = node_map[1]
    ans.part1 = ''
    while one.next.num != 1:
        ans.part1 += str(one.pop_next().num)


def part2(d: Data, ans: Answers) -> None:
    start: Optional[CupNode] = None
    max_cup = 1_000_000
    node_map: List[CupNode] = [None] * (max_cup + 1)

    start = make_ring_list(list(map(int, d)) + list(interval(10, max_cup)), node_map)
    iterate(start, 10_000_000, max_cup, node_map)

    one = node_map[1]
    ans.part2 = one.next.num * one.next.next.num


run([1, 2], day=23, year=2020)
