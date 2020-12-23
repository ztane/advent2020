from helpers import *

test_data = Data("""
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""")

test_case2 = """
Player 1:
43
19

Player 2:
2
29
14
"""

test_case(1, test_data, 306)
test_case(2, test_data, 291)
test_case(2, test_case2, 105)


def part1(d: Data, ans: Answers) -> None:
    players = d.split('\n\n')
    player_list = {}
    for i, p in enumerate(players):
        player_list[i] = deque(p.extract_ints[1:])

    while player_list[0] and player_list[1]:
        first = player_list[0].popleft()
        second = player_list[1].popleft()
        if first > second:
            player_list[0].append(first)
            player_list[0].append(second)
        else:
            player_list[1].append(second)
            player_list[1].append(first)

    winning = player_list[0] or player_list[1]
    print(player_list)
    rv = 0
    for i, v in zip(range(len(winning), 0, -1), winning):
        rv += i * v
    ans.part1 = rv


def part2(d: Data, ans: Answers) -> None:
    next_gameno = 1

    def play_game(p1, p2):
        nonlocal next_gameno
        gameno = next_gameno
        print(f'=== Game {gameno} ===\n')
        next_gameno += 1

        round = 0
        previous_rounds = set()
        while p1 and p2:
            round += 1
            print(f'-- Round {round} (Game {gameno}) --')
            print(f"Player 1's deck: {', '.join(map(str, p1))}")
            print(f"Player 2's deck: {', '.join(map(str, p2))}")

            if (x := tuple(p1)) in previous_rounds:
                p2 = []
                break

            previous_rounds.add(x)
            c1 = p1.popleft()
            c2 = p2.popleft()

            print(f"Player 1 plays: {c1}")
            print(f"Player 2 plays: {c2}")

            if not (len(p1) >= c1 and len(p2) >= c2):
                if c1 > c2:
                    winner = 1
                else:
                    winner = 2

                print(f"Player {winner} wins round {round} of game {gameno}!\n")
            else:
                new_p1 = deque(islice(p1, 0, c1))
                new_p2 = deque(islice(p2, 0, c2))
                print("Playing a sub-game to determine the winner...\n")
                winner = play_game(new_p1, new_p2)
                print(f"...anyway, back to game {gameno}")

            if winner == 1:
                p1.append(c1)
                p1.append(c2)

            elif winner == 2:
                p2.append(c2)
                p2.append(c1)

            else:
                raise ValueError("WTF")

        winning = p1 or p2
        if p1:
            winner = 1
        else:
            winner = 2

        print(f"The winner of game {gameno} is player {winner}!\n")
        if gameno == 1:
            ans.part2 = 0
            for i, v in zip(range(len(winning), 0, -1), winning):
                ans.part2 += i * v
        return winner

    players = d.split('\n\n')
    player_list = {}
    for i, p in enumerate(players):
        player_list[i] = deque(p.extract_ints[1:])

    play_game(player_list[0], player_list[1])


run([2], day=22, year=2020, submit=True)
