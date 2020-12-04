from helpers import *

d = get_aoc_data(day=4)

REQUIRED_FEATURES = {'byr', 'iyr', 'ecl', 'pid', 'hgt', 'hcl', 'eyr'}

EYE_COLOURS = {'amb', 'grn', 'oth', 'brn', 'blu', 'gry', 'hzl'}


def passports():
    records = d.split('\n\n')
    for i in records:
        features = i.split()

        feature_map = dict(j.split(':', 1) for j in features)

        if not REQUIRED_FEATURES - feature_map.keys():
            yield feature_map


def part1():
    return sum(1 for _ in passports())


def part2():
    ct = 0
    for features in passports():
        hgt_unit = features['hgt'][-2:]
        if hgt_unit not in {'in', 'cm'}:
            # print(f'invalid height unit, or unit missing in {hgt_unit!r}')
            continue

        hgt = int(features['hgt'][:-2])

        ct += all([
            int(features['byr']) in interval(1920, 2002),
            int(features['iyr']) in interval(2010, 2020),
            int(features['eyr']) in interval(2020, 2030),
            features['ecl'] in EYE_COLOURS,
            re.fullmatch('#[0-9a-fA-F]{6}', features['hcl']),
            features['pid'].isdigit(),
            len(features['pid']) == 9,
            (hgt_unit == 'cm' and hgt in interval(150, 193) or
             hgt_unit == 'in' and hgt in interval(59, 76))
        ])

    return ct
