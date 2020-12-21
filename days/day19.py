from helpers import *

test_data = Data("""\n
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

aaaabb
aaabab
c
""")

test_data2 = Data("""\n
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""")

test_case(1, test_data, 2)
test_case(2, test_data2, 12)


def match_rules(rules, messages):
    max_recursion = max(map(len, messages))
    recursion_counter = Counter()

    def deduce(rule) -> str:
        recursion_counter[rule] += 1
        if recursion_counter[rule] == max_recursion:
            return 'x'

        def recurse(match):
            return deduce(match.group(1))

        result = re.sub(r'(\d+)', recurse, rules[rule])
        result = result.replace(' ', '')

        recursion_counter[rule] -= 1

        if '|' in result:
            return f'(?:{result})'

        return result

    rule0 = re.compile(deduce('0'))
    print(len(rule0.pattern))
    return sum(map(bool, map(rule0.fullmatch, messages)))


def part1_and_2(d: Data, ans: Answers) -> None:
    rules, messages_str = d.split('\n\n')
    rule_list = {}
    for l in rules.lines:
        n, r = l.split(': ')
        rule_list[n] = r.replace('"', '')

    messages = messages_str.lines
    ans.part1 = match_rules(rule_list, messages)

    rule_list['8'] = '42 | 42 8'
    rule_list['11'] = '42 31 | 42 11 31'

    ans.part2 = match_rules(rule_list, messages)


run([1, 2], day=19, year=2020)
