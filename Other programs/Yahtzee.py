
from random import randint
from collections import Counter

EMPTY = None

CATEGORY_MENU = {
    1: "ones",
    2: "twos",
    3: "threes",
    4: "fours",
    5: "fives",
    6: "sixes",
    7: "three_kind",
    8: "four_kind",
    9: "full_house",
    10: "s_straight",
    11: "l_straight",
    12: "chance",
    13: "yahtzee",
    14: "show_scorecard",
}

LABELS = {
    "ones": "Ones",
    "twos": "Twos",
    "threes": "Threes",
    "fours": "Fours",
    "fives": "Fives",
    "sixes": "Sixes",
    "three_kind": "Three of a Kind",
    "four_kind": "Four of a Kind",
    "full_house": "Full House",
    "s_straight": "Small Straight",
    "l_straight": "Large Straight",
    "chance": "Chance",
    "yahtzee": "Yahtzee",
    "top_bonus": "Upper Bonus",
}


class Player:
    def __init__(self, name):
        self.name = name
        self.scorecard = make_scorecard()

    def upper_total(self):
        return sum(
            self.scorecard[key] or 0
            for key in ["ones", "twos", "threes", "fours", "fives", "sixes"]
        )

    def total_score(self):
        bonus = 35 if self.upper_total() >= 63 else 0
        self.scorecard["top_bonus"] = bonus
        return sum(value or 0 for value in self.scorecard.values())


def make_scorecard():
    return {
        "ones": EMPTY,
        "twos": EMPTY,
        "threes": EMPTY,
        "fours": EMPTY,
        "fives": EMPTY,
        "sixes": EMPTY,
        "three_kind": EMPTY,
        "four_kind": EMPTY,
        "full_house": EMPTY,
        "s_straight": EMPTY,
        "l_straight": EMPTY,
        "chance": EMPTY,
        "yahtzee": EMPTY,
        "top_bonus": 0,
    }


def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Please enter a number from {min_value} to {max_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Please enter a number from {min_value} to {max_value}.")
            continue
        return value


def get_players():
    player_count = get_int_input("How many players for this game? ", 1, 6)
    players = []

    for player_num in range(1, player_count + 1):
        while True:
            name = input(f"What is player {player_num}'s name? ").strip()
            if name:
                players.append(Player(name))
                break
            print("Please enter a name.")

    return players


def display_dice(dice):
    print("Dice:", " ".join(str(d) for d in dice))


def choose_keepers(player, current_dice):
    prompt = (
        f"Player {player.name}, which dice will you keep for the next roll?\n"
        "Press ENTER to keep none, or type the die values to keep.\n"
        "Example: 155 keeps one 1 and two 5s if available.\n> "
    )

    while True:
        pick = input(prompt).strip()

        if pick == "":
            return []

        if not pick.isdigit():
            print("Please enter only digits that match dice values.")
            continue

        picked = [int(ch) for ch in pick]
        if any(die < 1 or die > 6 for die in picked):
            print("Dice values must be between 1 and 6.")
            continue

        picked_counts = Counter(picked)
        current_counts = Counter(current_dice)

        if all(picked_counts[val] <= current_counts[val] for val in picked_counts):
            return sorted(picked)

        print("You tried to keep dice that are not available. Try again.")


def roll(player):
    keep = []
    final_dice = []

    for roll_number in range(1, 4):
        rolled = [randint(1, 6) for _ in range(5 - len(keep))]
        final_dice = sorted(keep + rolled)

        print(f"\n{player.name}'s roll #{roll_number}")
        display_dice(final_dice)

        if roll_number < 3:
            keep = choose_keepers(player, final_dice)

    write_score(player, final_dice)


def score_category(category, dice, current_score):
    counts = Counter(dice)
    total = sum(dice)
    unique = set(dice)

    if category == "ones":
        return counts[1] * 1
    if category == "twos":
        return counts[2] * 2
    if category == "threes":
        return counts[3] * 3
    if category == "fours":
        return counts[4] * 4
    if category == "fives":
        return counts[5] * 5
    if category == "sixes":
        return counts[6] * 6
    if category == "three_kind":
        return total if any(count >= 3 for count in counts.values()) else 0
    if category == "four_kind":
        return total if any(count >= 4 for count in counts.values()) else 0
    if category == "full_house":
        return 25 if sorted(counts.values()) == [2, 3] else 0
    if category == "s_straight":
        straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        return 30 if any(straight.issubset(unique) for straight in straights) else 0
    if category == "l_straight":
        return 40 if unique in ({1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}) else 0
    if category == "chance":
        return total
    if category == "yahtzee":
        if len(unique) == 1:
            if current_score is EMPTY:
                return 50
            if current_score > 0:
                return current_score + 100
        return 0 if current_score is EMPTY else current_score

    raise ValueError("Unknown category.")


def show_scorecard(player):
    print(f"\n{'-' * 45}")
    print(f"{player.name}'s scorecard")
    print("-" * 45)
    for key, value in player.scorecard.items():
        label = LABELS.get(key, key)
        shown = "OPEN" if value is EMPTY else value
        print(f"{label:<18} : {shown}")
    print(f"Upper subtotal      : {player.upper_total()}")
    print(f"Potential bonus     : {35 if player.upper_total() >= 63 else 0}")
    print(f"{'-' * 45}\n")


def write_score(player, dice):
    while True:
        print("\nOpen slots are:")
        for num, key in CATEGORY_MENU.items():
            if key == "show_scorecard":
                print(f"{num}: Show scorecard")
            elif player.scorecard[key] is EMPTY:
                print(f"{num}: {LABELS[key]}")

        choice = get_int_input(
            f"\nWhere would you like to write your score?\nYour dice: {dice}\n> ",
            1,
            14,
        )

        if choice == 14:
            show_scorecard(player)
            continue

        category = CATEGORY_MENU[choice]
        if player.scorecard[category] is not EMPTY and category != "yahtzee":
            print("That slot is already filled. Choose another one.")
            continue

        if category == "yahtzee":
            player.scorecard["yahtzee"] = score_category(
                "yahtzee", dice, player.scorecard["yahtzee"]
            )
        else:
            player.scorecard[category] = score_category(
                category, dice, player.scorecard[category]
            )
        break


def print_final_scores(players):
    print("\nThank you for playing! Final scores:\n")
    for player in players:
        show_scorecard(player)
        print(f"{player.name}'s final score: {player.total_score()}")
        print("-" * 45)


def main():
    players = get_players()
    turns = 13

    while turns > 0:
        for player in players:
            print(f"\nIt's {player.name}'s turn.")
            roll(player)
        turns -= 1

    print_final_scores(players)


if __name__ == "__main__":
    main()
