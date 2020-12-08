from helpers import *


test_data = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

test_case(1, test_data, 5)

test_data2 = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

test_case(2, test_data, 8)

nop = Parser("nop <int>")
acc = Parser("acc <int>")
jmp = Parser("jmp <int>")


def run_code(instructions: Sequence[str]) -> Answers:
    a = ip = 0
    seen = set()

    while True:
        if ip == len(instructions):
            return Answers(part2=a)

        # works for part 2 too to return here
        # as it is not possible to break any *loop*
        if ip in seen:
            return Answers(part1=a)

        seen.add(ip)
        instr = instructions[ip]

        ip += 1
        if acc(instr):
            a += acc[0]

        elif jmp(instr):
            ip += jmp[0] - 1

        elif not nop(instr):
            raise ValueError("wtf")


def part1(d: Data, ans: Answers) -> None:
    ans.part1 = run_code(d.lines).part1


def part2(d: Data, ans: Answers) -> None:
    for pos, instruction in enumerate(d.lines):
        instructions = list(d.lines)

        if jmp(instruction):
            instructions[pos] = instruction.replace("jmp", "nop")

        elif nop(instruction):
            instructions[pos] = instruction.replace("nop", "jmp")

        else:
            continue

        ans.part2 = run_code(instructions).part2
        if ans.part2 is not None:
            return


run([1, 2], day=8, year=2020)
