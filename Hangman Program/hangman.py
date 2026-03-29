import random
import string

# local imports
from hangman_data import xmas, hard, animals, art, finance, gallows


def random_line():
    print('Pick a THEME\n____________')
    theme = {1: (xmas, 'Christmas'), 2: (hard, 'Hard'), 3: (animals, 'Animals'), 4: (art, 'Art'),
             5: (finance, 'Finance')}

    index = input('1. Christmas\n2. Hard\n3. Animals\n4. Art\n5. Finance\n0. Random\n')
    while index not in '012345':
        index = input('1. Christmas\n2. Hard\n3. Animals\n4. Art\n5. Finance\n0. Random\n')
    index = int(index)
    if index == 0:
        index = random.randint(1, 5)

    print(f'The theme is : {theme[index][1]}')
    return random.choice(theme[index][0])


def play_game(word, used):
    # print(f'Secret word hacked: {word}')
    guessed = False
    case_word = word.lower()
    tries = 7
    lower = string.ascii_lowercase
    punc = string.punctuation
    hidden = ['_' if ch in string.ascii_letters else ' ' for w in word for ch in w]

    if ' ' in word:
        words = word.split()
        msg = f'There are {len(words)} words.\n'
        for i, w in enumerate(words, 1):
            msg += f'Word {i} is {len(w)} letters long. '
    else:
        msg = f'There is 1 word that is {len(word)} letters long'

    while not guessed:
        print(gallows[tries])
        print(f'\n{msg}\nThe word is : {"".join(hidden)}\n\nTries left: {tries}\nUsed: {used}')

        guess = input('What letter would you like to try?\nPress ENTER for random letter\n').lower()
        if guess == '' or guess == ' ':
            guess = random.choice(lower)
        while guess in used:
            print(f'you have already used {guess.upper()}')
            guess = input('What letter would you like to try?\nPress ENTER for random letter\n').lower()
            if guess == '' or guess == ' ':
                guess = random.choice(lower)
        used.append(guess)

        if len(guess) != 1 and len(guess) != len(case_word) or guess.isdigit() or guess in punc:
            print(f'{guess} was an invalid guess. Try again.')
        elif len(guess) == len(case_word) and guess == case_word:
            print(f'Congratulations! You win\n{word.upper()} was the word')
            guessed = True
        elif guess in case_word:
            print(f'Your guess {guess.upper()} is in the word.')
            indexes = [i for i in range(len(case_word)) if case_word[i] == guess]
            for x in range(len(indexes)):
                hidden[indexes[x]] = word[indexes[x]]
            if "".join(hidden).lower() == case_word:
                print(f'Congratulations! You win\n"{word.upper()}" was the word')
                guessed = True
        else:
            tries -= 1
            print(f'Your guess {guess.upper()} was not in the word. Try again')
            if tries == 0:
                final = input('What is your final guess of the word?\n')
                if final.lower() != case_word:
                    print(gallows[0])
                    print(f'Game Over! "{word.upper()}" was the word.\n')
                    break
                else:
                    print(f'Congratulations! You win\n"{word.upper()}" was the word\n')
                    guessed = True


def main():
    while True:
        word = random_line()
        play_game(word, [])
        play = input('\nWould you like to play again?\nPress ENTER to Continue or any key to Quit\n')
        if play != '':
            print('Thank you for playing!!!')
            break


if __name__ == '__main__':
    main()