from helpers import *


def part1_and_2(data: Data, answers: Answers):
    t = str.maketrans('FLBR', '0011')
    seat_ids = {int(bpass.translate(t), 2) for bpass in data.lines}
    missing_id = scalar(set(interval(min(seat_ids), max(seat_ids))) - seat_ids)
    answers.part1 = max(seat_ids)
    answers.part2 = missing_id


run([1, 2], day=5, year=2020)
