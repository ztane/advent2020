from helpers import *

test_data = Data("""
389125467
""")

test_case(1, test_data, 67384529)
test_case(2, test_data, 149245887792)


def part1(d: Data, ans: Answers) -> None:
    state = deque(map(int, d.data))
    for i in range(100):
        current = state[0]
        state.rotate(-1)
        cup1 = state.popleft()
        cup2 = state.popleft()
        cup3 = state.popleft()

        cups = [cup1, cup2, cup3]
        destination = (current - 2) % 9 + 1
        while destination in cups:
            destination = (destination - 2) % 9 + 1

        #print('current', current, 'destination', destination, 'pick up', cups)
        #print('state before rotate', state)
        location = state.index(destination)
        state.rotate(-location-1)
        # print('rotated', location, location - 1)
        # print('presumed', destination, 'on left', state)
        state.appendleft(cup3)
        state.appendleft(cup2)
        state.appendleft(cup1)
        location = state.index(current)
        state.rotate(-location)
        state.rotate(-1)
       # print(state)

    state.rotate(i)
    state.rotate(-state.index(1))
    state.popleft()
    ans.part1 = ''.join(map(str, state))


class CupNode:
    next: 'CupNode' = None
    prev: 'CupNode' = None

    def __init__(self, num):
        self.num = num

    def unlink(self):
        self.next.prev = self.prev
        self.prev.next = self.next

    def link(self, after):
        self.next = after.next
        self.prev = after
        self.next.prev = self
        after.next = self

    def __str__(self):
        return f'C{self.num}'


def part2(d: Data, ans: Answers) -> None:
    start: Optional[CupNode] = None
    prev: Optional[CupNode] = None

    node_map: Dict[int, CupNode] = {}
    max_cup = 0
    for i in list(map(int, d.data)) + list(interval(10, 1_000_000)):
        node = CupNode(i)
        node.prev = prev
        if prev:
            prev.next = node

        prev = node
        if start is None:
            start = node

        node_map[i] = node
        max_cup = max(i, max_cup)

    start.prev = node
    node.next = start
    current = start
    for i in range(10_000_000):
        cup1 = current.next
        cup1.unlink()
        cup2 = current.next
        cup2.unlink()
        cup3 = current.next
        cup3.unlink()
        target = current.num - 1
        if target == 0:
            target = max_cup

        if i % 100000 == 0:
            print(i)

        while target in [cup1.num, cup2.num, cup3.num]:
            target -= 1
            if target == 0:
                target = max_cup

        current = current.next
        target_node = node_map[target]
        cup3.link(target_node)
        cup2.link(target_node)
        cup1.link(target_node)


        """
        c = current
        while True:
            print(c, end=' ')
            c = c.next
            if c == current:
                break
        print()
"""

    # print(state)

    one = node_map[1]

    ans.part2 = one.next.num * one.next.next.num


run([2], day=23, year=2020, submit=True)
