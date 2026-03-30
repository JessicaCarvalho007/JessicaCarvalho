# Programmer: Jeffrey Carvalho

import random
from collections import namedtuple


def build_deck():
    decks = 'Get number of Decks'
    while not decks.isdigit() or int(decks) not in range(1, 21):
        decks = input(f"How many decks would you like to play with?\n"
                      f"Minimum: 1\nMaximum: 20\n{'__' * 22}\n")
    decks = int(decks)
    deck_ = []
    for i, suit in enumerate(suits):
        deck_.extend(tuple(map(lambda n: f'{n}-{suit}', range(2, 11))))
        deck_.extend(tuple(map(lambda f: f'{f}-{suit}', face)))
    deck_ = deck_ * decks
    random.shuffle(deck_)
    return deck_


def get_card():
    global used
    card = (random.randint(0, len(deck) - 1))
    if card not in used:
        used.append(card)
    else:
        while True:
            if len(used) == len(deck) - 1:
                out = ""
                while out != 'y' and out != 'n':
                    out = input(
                        f'Out of Cards!\nThe current score is {score}\n'
                        f'Would you like to start over\nY or N\n').lower()
                if out == 'y':
                    used = []
                    random.shuffle(deck)
                    deal()
                else:
                    quit()
            new_card = random.randint(0, len(deck) - 1)
            if new_card not in used:
                used.append(new_card)
                card = new_card
                break
    return card


def deal():  # change this to 1,1,1,1
    player = []
    comp = []
    p1 = 0
    c1 = 0
    for i in range(4):
        num = get_card()
        if p1 == 2:
            c1 += 1
            comp.append(deck[num])
        else:
            p1 += 1
            player.append(deck[num])
    return player, comp


def have_ace(hand):
    card_nums = []
    for card in hand:
        c_num, _ = card.split('-')
        card_nums.append(c_num)
    return card_nums.count('A')


def check_value(num):
    if num in face.keys():
        if num == 'A':
            return int(face[num][0])
        else:
            return int(face[num])
    return int(num)


def player(*hands):
    for i, hand in enumerate(hands):
        lst = p if i < 1 else c
        for card in hand:
            num, suit = card.split("-")
            n = check_value(num)
            lst.append(n)
    aces = have_ace(hands[0])

    if aces >= 1:
        if sum(p) > 21:
            if 11 in p:
                x = p.index(11)
                p[x] = 1

    if sum(c) == 21:
        if sum(p) != 21:
            print(f'Player Hand: {pl_hand}\nDealer Hand: {comp_hand}\nComputer wins with Black Jack!')
            return write_score(2)
        else:
            print(f'Player Hand: {pl_hand}\nDealer Hand: {comp_hand}\nBOTH HAVE BLACKJACK ... PUSH!')
            return write_score(3)
    elif sum(p) == 21:
        print(f'Player Hand: {pl_hand}\nDealer Hand: {comp_hand}\nYou Win with a Black Jack!!!')
        return write_score(1)

    while True:  # Toggle this code for regular play vs auto
        hit = input(f"\nDealer Shows: [{comp_hand[0]}]\n"
                    f"Your Hand: {pl_hand} with a total {sum(p)} ... {aces} Ace(s)\n\n"
                    f"Press H to Hit or ENTER to Stand or Q to Quit\n")
        if hit.lower() == 'q':
            print(f"Thanks for playing!\nFinal score is {score}")
            quit()
        elif hit.lower() == "h":
            num = get_card()
            new_card, _ = deck[num].split('-')
            pl_hand.append(deck[num])
            new_n = check_value(new_card)
            p.append(new_n)
        elif hit == "":
            return computer()

        if sum(p) > 21:
            if 11 in p:
                x = p.index(11)
                p[x] = 1
            else:
                print(f'Player Hand: {pl_hand}\nDealer Hand: {comp_hand}\nYou busted with {sum(p)}')
                return write_score(2)
    # while sum(p) < 17:  # Automatic game (comment this while loop in and the upper while loop out)
    #     num = get_card()
    #     new_card, __ = deck[num].split('-')
    #     pl_hand.append(deck[num])
    #     new_n = check_value(new_card)
    #     p.append(new_n)
    #     if sum(p) > 21:
    #         if 11 in p:
    #             x = p.index(11)
    #             p[x] = 1
    #         else:
    #             print(f'Player Hand: {pl_hand}\nDealer Hand: {comp_hand}\nYou busted with {sum(p)}')
    #             return write_score(2)
    #
    # return computer()


def computer():
    aces = have_ace(comp_hand)
    if aces >= 1:
        if sum(c) > 21:
            if 11 in c:
                x = c.index(11)
                c[x] = 1
    print(f"Player Hand: {pl_hand}\nDealer Hand: {comp_hand}")
    while sum(c) < 17:
        num = get_card()
        new_card, __ = deck[num].split('-')
        comp_hand.append(deck[num])
        new_n = check_value(new_card)
        c.append(new_n)
        print(f"Dealer Hand: {comp_hand}")
        if sum(c) > 21:
            if 11 in c:
                x = c.index(11)
                c[x] = 1
            else:
                print(f'Computer busted with {sum(c)}')
                return write_score(1)

    if sum(p) > sum(c):
        return write_score(1)
    elif sum(c) > sum(p):
        return write_score(2)
    else:
        return write_score(3)


def write_score(who):
    global score
    pl_score = sum(p)
    co_score = sum(c)
    output = {'player': f"Player: {pl_score}\nComputer: {co_score}\nYou win!\n",
              'computer': f"Player: {pl_score}\nComputer: {co_score}\nYou lose!\n",
              'tie': f'Player: {pl_score}\nComputer: {co_score}\n...It\'s a Push...\n'}
    if who == 1:
        score = score._replace(player=score.player + 1)
        return output['player']
    elif who == 2:
        score = score._replace(computer=score.computer + 1)
        return output['computer']
    elif who == 3:
        score = score._replace(tie=score.tie + 1)
        return output['tie']


Score = namedtuple('Score', ['player', 'computer', 'tie'])
score = Score(player=0, computer=0, tie=0)
used = []
suits = ['H', 'C', 'S', 'D']
face = {'J': '10', 'Q': '10', 'K': '10', 'A': ['11', '1']}
deck = build_deck()

if __name__ == '__main__':
    while True:
        p = []
        c = []
        pl_hand, comp_hand = deal()
        print(player(pl_hand, comp_hand))
