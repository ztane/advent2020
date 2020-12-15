from helpers import *

# different test case for part 1.
# part 1 extra X from the original test
# case cause the combined code to blow!
test_data = """\
mask = 000000000000000000000000000001XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""

test_data2 = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
"""

test_case(1, test_data, 165)
test_case(2, test_data, 3232)
test_case(1, test_data2, 51)
test_case(2, test_data2, 208)


def part1_and_2(d: Data, ans: Answers) -> None:
    address_space_p1 = defaultdict(int)
    address_space_p2 = defaultdict(int)
    floating_bits = []
    or_mask = and_mask = 0

    for i in d.lines:
        if mask_match := i.parsed('mask = <>'):
            mask = mask_match[0]

            and_mask = int(mask.replace('X', '1'), 2)
            or_mask = int(mask.replace('X', '0'), 2)
            floating_mask = int(mask.replace('1', '0').replace('X', '1'), 2)

            floating_bits = [
                bit
                for bit_num in range(36)
                for bit in [1 << bit_num]
                if floating_mask & bit
            ]

        elif address_match := i.parsed('mem[<int>] = <int>'):
            addr, value = address_match
            value_p1 = value & and_mask | or_mask
            address_space_p1[addr] = value_p1

            addr_p2 = addr | or_mask

            for bit_set in powerset(floating_bits):
                new_addr = addr_p2
                for bit in bit_set:
                    new_addr ^= bit

                address_space_p2[new_addr] = value

    ans.part1 = sum(address_space_p1.values())
    ans.part2 = sum(address_space_p2.values())


run([1, 2], day=14, year=2020)
