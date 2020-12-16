from helpers import *

test_data = Data("""
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
""")


test_case(1, test_data, 71)
test_case(2, """\
departure class: 0-1 or 4-19
departure row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""", 12 * 11)


def part1(d: Data, ans: Answers) -> None:
    constraints, my_ticket, nearby = d.split('\n\n')

    all_constraints = {}
    print(constraints.lines)
    for cls, constr in [i.split(':') for i in constraints.lines]:
        constr = iter(Data(constr.replace('-', ' ')).extract_ints)
        ranges = []
        for i in constr:
            ranges.append((i, next(constr)))
        all_constraints[cls] = ranges

    my_ticket = my_ticket.extract_ints
    nearby_tickets = [i.extract_ints for i in nearby.lines]

    print(all_constraints, my_ticket, nearby_tickets)

    rate = 0
    for x in nearby_tickets:
        for y in x:
            valid = False
            for r in all_constraints.values():
                for (start, end) in r:
                    if start <= y <= end:
                        valid = True
            if not valid:
                rate += y
                break
    ans.part1 = rate


def part2(d: Data, ans: Answers) -> None:
    constraints, my_ticket, nearby = d.split('\n\n')

    all_constraints = {}
    for cls, constr in [i.split(':') for i in constraints.lines]:
        constr = iter(Data(constr.replace('-', ' ')).extract_ints)
        ranges = []
        for i in constr:
            ranges.append((i, next(constr)))
        all_constraints[cls] = ranges

    my_ticket = my_ticket.extract_ints
    nearby_tickets = [i.extract_ints for i in nearby.lines]

    rate = 0
    valid_tickets = []
    for x in nearby_tickets:
        for y in x:
            valid = False
            for r in all_constraints.values():
                for (start, end) in r:
                    if start <= y <= end:
                        valid = True
            if not valid:
                break
        else:
            valid_tickets.append(x)

    cols = len(my_ticket)
    possible = [set(all_constraints) for _ in range(cols)]
    for tkt in valid_tickets:
        for i, e in enumerate(tkt):
            for k, v in all_constraints.items():
                valid = False
                for (start, end) in v:
                    if start <= e <= end:
                        valid = True
                if not valid:
                    possible[i].discard(k)

    possible = sorted([i for i in enumerate(possible)], key=lambda x: len(x[1]))
    print(possible)

    assigned = set()
    answ = 1
    for i, e in possible:
        unassigned = scalar(e - assigned)
        print(i, unassigned)
        assigned.add(unassigned)

        if unassigned.startswith('departure'):
            answ *= my_ticket[i]

    ans.part2 = answ


run([2], day=16, year=2020, submit=True)
