from helpers import *

REQUIRED_FEATURES = {'byr', 'iyr', 'ecl', 'pid', 'hgt', 'hcl', 'eyr'}

EYE_COLOURS = {'amb', 'grn', 'oth', 'brn', 'blu', 'gry', 'hzl'}


test_data = Data("""
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""")
test_case(1, test_data, 2)

test_data2 = Data("""
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
""")

test_case(2, test_data2, 4)


def part1_and_2(d: Data, ans: Answers):
    def passports():
        records = d.split('\n\n')
        for i in records:
            features = i.split()

            feature_map = dict(j.split(':', 1) for j in features)

            if not REQUIRED_FEATURES - feature_map.keys():
                yield feature_map

    ans.part1 = len(list(passports()))

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

    ans.part2 = ct


run([1, 2], day=4, year=2020)

