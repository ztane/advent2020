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


def make_constraint_func(constraints):
    return lambda field: any(a <= field <= b for
                             (a, b) in constraints)


def part1(d: Data, ans: Answers) -> None:
    constraints, my_ticket, nearby = d.split('\n\n')

    all_constraints = {}
    for cls, constr in [i.split(':') for i in constraints.lines]:
        it = iter(constr.as_unsigned)
        all_constraints[cls] = make_constraint_func(tuple(zip(it, it)))

    my_ticket = my_ticket.as_unsigned
    nearby_tickets = [i.as_unsigned for i in nearby.lines]

    rate = 0
    for x in nearby_tickets:
        for y in x:
            valid = False

            for r in all_constraints.values():
                if r(y):
                    valid = True

            if not valid:
                rate += y
                break

    ans.part1 = rate


def part2(d: Data, ans: Answers) -> None:
    constraints_str, my_ticket_str, nearby_tickets_str = d.split('\n\n')

    constraints = {}
    for cls, constr in [i.split(':') for i in constraints_str.lines]:
        it = iter(constr.as_unsigned)
        constraints[cls] = make_constraint_func(tuple(zip(it, it)))

    my_ticket = my_ticket_str.extract_unsigned
    nearby_tickets = [i.extract_unsigned for i in nearby_tickets_str.lines]

    valid_tickets = []
    for ticket in nearby_tickets:
        for field in ticket:
            for field_c_func in constraints.values():
                if field_c_func(field):
                    break
            else:
                break
        else:
            valid_tickets.append(ticket)

    cols = len(my_ticket)
    possible_fields = {i: set(constraints) for i in range(cols)}
    for tkt in valid_tickets:
        for idx, ticket_field in enumerate(tkt):
            for k, field_c_func in constraints.items():
                if not field_c_func(ticket_field):
                    possible_fields[idx].discard(k)

    possible_ordered = sorted(possible_fields.items(), key=lambda x: len(x[1]))

    departure_field_product = 1
    assigned = set()

    for idx, field_set in possible_ordered:
        assigned.add(this_field := scalar(field_set - assigned))

        if this_field.startswith('departure'):
            departure_field_product *= my_ticket[idx]

    ans.part2 = departure_field_product


run([1, 2], day=16, year=2020)
