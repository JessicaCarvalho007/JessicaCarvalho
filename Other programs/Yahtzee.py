# https://www.ultraboardgames.com/yahtzee/game-rules.php

from random import randint


class Player(object):
    def __init__(self, name, scorecard):
        self.name = name
        self.scorecard = scorecard.copy()
        self.yahtzee = False


def get_players():
    # This function sets the player for the game with help from the Player Class
    player_count = 0
    scorecard = {'ones': 'NaN', 'twos': 'NaN', 'threes': 'NaN', 'fours': 'NaN', 'fives': 'NaN', 'sixes': 'NaN',
                 'three_kind': 'NaN', 'four_kind': 'NaN', 'full_house': 'NaN', 's_straight': 'NaN',
                 'l_straight': 'NaN', 'chance': 'NaN', 'yahtzee': 'NaN', 'top': 0}
    try:
        player_count = int(input('How many players for this game? '))
        while player_count < 1 or player_count > 6:
            player_count = int(input('How many players for this game? '))
    except ValueError:
        get_players()
    finally:
        for player_num in range(1, player_count + 1):
            name = input(f'What is player {player_num}\'s name? ')
            user = Player(name, scorecard)
            players.append(user)


def roll(player):
    # This function controls the rolls per turn
    rolls = 0
    num_dice = 5
    keep = list()
    while rolls < 3:
        rolls += 1
        dice = sorted([randint(1, 6) for _ in range(num_dice - len(keep))])
        print(f'Player: {player.name}, Rolled {dice}'
              f' on roll #{rolls if rolls == 1 else str(rolls) + ", Holding " + str(keep)}')
        if rolls == 3:
            for die in dice:
                keep.append(die)
            keep = sorted(keep)
        else:
            keep = sorted(keep)
            rolls, dice, keep = check_picked(player, rolls, dice, keep)
    write_score(player, keep)


def check_picked(player, rolls, dice, keep):
    # This function validates the players choice before moving to the next roll
    check = False
    keep_msg = 'Which dice will you keep? Press ENTER for none, 0 to clear keepers or select each die value to keep\n'
    pick = ''
    while len(pick) > 5 or not pick.isdigit() or not check:
        pick = input(keep_msg)
        if pick == '':
            break
        else:
            if pick == '0':
                dice = sorted(keep + dice)
                keep = []
                print(f'Player: {player.name} Dice: {dice} Roll #{rolls}')
            try:
                picked = list(map(int, pick))
            except ValueError:
                check_picked(player, rolls, dice, keep)
            else:
                for d in picked:
                    if d not in dice or picked.count(d) > dice.count(d):
                        break
                    else:
                        keep.append(d)
                        check = True
    if len(keep) == 5:
        rolls = 3

    return rolls, sorted(dice), sorted(keep)


def write_score(player, keep):
    # This function writes the score to the players card after each turn
    msg = f"""{"-" * 50}\n1: Ones\n2: Twos\n3: Threes\n4: Fours\n5: Fives\n6: Sixes
7: Three of a Kind\n8: Four of a Kind\n9: Full House\n10: Small Straight\n11: Large Straight
12: Chance\n13: Yahtzee\n14: Show your Scorecard"""
    write_msg = f'Where would you like to write your score?\nYour dice: {keep}\n\n{msg}\n{"_" * 50}\n'
    print(f'\nOpen slots are:')
    for slot in player.scorecard:
        if player.scorecard[slot] == 'NaN':
            print(slot, end=', ')
    print('\n')
    try:
        where = int(input(write_msg))
        while where < 0 or where > 14:
            where = int(input(write_msg))
    except ValueError:
        print('Please select a number 0-14')
        write_score(player, keep)
    else:  # The heart of the game
        if where == 1 and player.scorecard['ones'] == 'NaN': player.scorecard['ones'] = keep.count(1)
        elif where == 2 and player.scorecard['twos'] == 'NaN': player.scorecard['twos'] = keep.count(2) * 2
        elif where == 3 and player.scorecard['threes'] == 'NaN': player.scorecard['threes'] = keep.count(3) * 3
        elif where == 4 and player.scorecard['fours'] == 'NaN': player.scorecard['fours'] = keep.count(4) * 4
        elif where == 5 and player.scorecard['fives'] == 'NaN': player.scorecard['fives'] = keep.count(5) * 5
        elif where == 6 and player.scorecard['sixes'] == 'NaN': player.scorecard['sixes'] = keep.count(6) * 6
        elif where == 7 and player.scorecard['three_kind'] == 'NaN':
            check = any([True if keep.count(die) == 3 else False for die in set(keep)])
            if check: player.scorecard['three_kind'] = sum(keep)
            else: player.scorecard['three_kind'] = 0
        elif where == 8 and player.scorecard['four_kind'] == 'NaN':
            check = any([True if keep.count(die) == 4 else False for die in set(keep)])
            if check: player.scorecard['four_kind'] = sum(keep)
            else: player.scorecard['four_kind'] = 0
        elif where == 9 and player.scorecard['full_house'] == 'NaN':
            check = all([True if keep.count(die) >= 2 else False for die in set(keep)])
            if check: player.scorecard['full_house'] = 25
            else: player.scorecard['full_house'] = 0
        elif where == 10 and player.scorecard['s_straight'] == 'NaN':
            check = sum([1 if keep[i + 1] == keep[i] + 1 else 0 for i in range(len(keep) - 1)])
            if check >= 3: player.scorecard['s_straight'] = 30
            else: player.scorecard['s_straight'] = 0
        elif where == 11 and player.scorecard['l_straight'] == 'NaN':
            check = sum([1 if keep[i + 1] == keep[i] + 1 else 0 for i in range(len(keep) - 1)])
            if check == 4: player.scorecard['l_straight'] = 40
            else: player.scorecard['l_straight'] = 0
        elif where == 12 and player.scorecard['chance'] == 'NaN': player.scorecard['chance'] = sum(keep)
        elif where == 13:
            if len(set(keep)) == 1:
                if player.scorecard['yahtzee'] == 'NaN': player.scorecard['yahtzee'] = 0
                if player.yahtzee == 0:
                    player.scorecard['yahtzee'] += 50
                    player.yahtzee = 1
                elif player.yahtzee == 1: player.scorecard['yahtzee'] += 100
            else:
                if player.scorecard['yahtzee'] == 'NaN':
                    player.scorecard['yahtzee'] = 0
                    player.yahtzee = 2
                else: write_score(player, keep)
        elif where == 14:
            for slot, score in p.scorecard.items():
                if slot == 'top':
                    continue
                print(f'{slot}: {score}')
            write_score(player, keep)
        else:
            print("Invalid Selection. Try again.\n")
            write_score(player, keep)


if __name__ == '__main__':
    players = []
    get_players()
    turns = 13
    while turns > 0:
        for p in players:
            print(f'\nIt\'s {p.name}\'s turn\n')
            roll(p)
        turns -= 1
    print(f'Thank you for playing the final scores are:\n')
    for p in players:
        for k in p.scorecard:
            if p.scorecard[k] == 'NaN':
                p.scorecard[k] = 0
        if p.scorecard['ones'] + p.scorecard['twos'] + p.scorecard['threes'] + \
                p.scorecard['fours'] + p.scorecard['fives'] + p.scorecard['sixes'] >= 63:
            print(f'Congratulations!!! {p.name} gets 35 BONUS Points!')
            p.scorecard['top'] = 35
        for key, value in p.scorecard.items():
            print(f'{key}: {value}')
        print(f'Player: {p.name}\'s final score {sum(p.scorecard.values())}\n{"-" * 35}\n')
