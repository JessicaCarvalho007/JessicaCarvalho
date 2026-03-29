from random import randint, choice
import tkinter as tk
from tkinter import ttk
import time


def play():
    def get_guess(user_guess):
        if isinstance(user_guess, tk.Event):
            user_guess = int(guess_.get())
        else:
            user_guess = int(user_guess)
        if winner.get():
            new_game(rng.get())
        else:
            try:
                tries.set(tries.get() + 1)
                guesses.append(guess_.get())
                secret_number = secret.get()
                print(f'guess: {user_guess}\t secret: {secret_number}')
                if user_guess == secret_number:
                    won_game()
                else:
                    if not winner.get() and tries.get() == 15:
                        over1 = f'Sorry,You\'ve lost.\n' \
                                f'"{secret_number.get()}" was the SECRET number.'
                        over2 = 'All 15 tries were used\nTime to play again!'
                        guessed.config(text=over1)
                        game_msg.config(text=over2, foreground='royal blue')
                        win.update()
                        time.sleep(3)
                        new_game(rng.get())
                    elif user_guess < secret_number:
                        if user_guess >= start.get():
                            start.set(user_guess + 1)
                            guess_.set(user_guess + 1)
                        else:
                            guess_.set(start.get())
                        game_msg.config(text=f'The secret number\nis HIGHER than "{user_guess}"')
                    else:
                        if user_guess <= end.get():
                            end.set(user_guess - 1)
                            guess_.set(user_guess - 1)
                        else:
                            guess_.set(end.get())
                        game_msg.config(text=f'The secret number\nis LOWER than "{user_guess}"')
                    new_nums = list(range(start.get(), end.get() + 1))
                    guess_.config(values=new_nums)
                    guessed.config(text=f'Guessed: {", ".join(guesses)}\nTries: {tries.get()}')
                    win.update()
            except ValueError:
                print(f'Must be a number in range 0 to {end.get():,}')

    def won_game():
        winner.set(True)
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        user_guess = int(guess_.get())
        while winner:
            color = choice(colors)
            win_msg1 = f'{user_guess}-' * 3 + f'{user_guess}\n'
            win_msg2 = f'{user_guess} was the secret number!\nTries: {tries.get()}'
            guessed.config(text=win_msg1, foreground=color)
            game_msg.config(text=win_msg2, foreground=color)
            win.update()
            time.sleep(.1)
            if not winner.get():
                break

    def new_game(r):
        if winner.get():
            winner.set(False)
            wins.set(wins.get() + 1)
        games.set(games.get() + 1)
        tries.set(0)
        start.set(0)
        end.set(r)
        guess_.set(int(end.get()) // 2)
        guesses.clear()
        secret.set(randint(start.get(), end.get()))
        new_nums = list(range(start.get(), end.get() + 1))
        new_msg1 = f'Guessed: {", ".join(guesses)}\nTries: {tries.get()}'
        new_msg2 = f'Time to start Guessing!\nThe number is between 0 to {r:,}'
        guess_.config(values=new_nums)
        guessed.config(text=new_msg1, foreground='royal blue')
        game_msg.config(text=new_msg2, foreground='black')
        win.update()

    def end_game():
        if winner.get():
            wins.set(wins.get() + 1)
        winner.set(False)
        good_bye = f'You played: {games.get()} games\nYou won: {wins.get()}'
        guessed.config(text='Goodbye,\nThank you for playing!!!', foreground='royal blue')
        game_msg.config(text=good_bye, foreground='royal blue')
        win.update()
        time.sleep(1.5)
        exit()

    win = tk.Tk()
    win.geometry('755x440')
    body = ttk.Frame(win)

    guesses = []
    winner = tk.BooleanVar(win)
    winner.set(False)
    wins = tk.IntVar(win)
    wins.set(0)
    start = tk.IntVar(win)
    start.set(0)  # <--change to limit by guesses
    end = tk.IntVar(win)
    end.set(100)
    rng = tk.IntVar(win)
    rng.set(100)
    games = tk.IntVar(win)
    games.set(0)
    cur_nums = list(range(start.get(), end.get() + 1))
    secret = tk.IntVar(win)
    secret.set(randint(start.get(), end.get()))
    tries = tk.IntVar(win)
    tries.set(0)
    img = tk.PhotoImage(file='nums.png')

    logo = ttk.Label(win, image=img, borderwidth=5, relief="ridge")
    guessed = ttk.Label(win, font=('Arial', 20, 'bold'), foreground='royal blue', justify='center',
                        text=f'Guessed:{", ".join(guesses)}\nTries: {tries.get()}')
    game_msg = ttk.Label(win, font=('Arial', 18, 'bold'), justify='center',
                         text='Time to start Guessing!\nThe number is between 1 to 100')
    guess_ = ttk.Combobox(win, values=cur_nums)
    guess_.set(50)
    guess_.bind('<Return>', get_guess)
    change = tk.OptionMenu(win, rng, *[10, 50, 100, 500, 1000], command=new_game)
    change_name = ttk.Label(win, text='Set Range: ')
    enter = ttk.Button(win, text='Enter', command=lambda: get_guess(guess_.get()))
    new = ttk.Button(win, text='New Game', command=lambda: new_game(rng.get()))
    quit_ = ttk.Button(win, text='Quit', command=end_game)

    body.grid(column=0, row=0, columnspan=6, rowspan=7, sticky=('N', 'E', 'S', 'W'))
    logo.grid(column=0, row=0, columnspan=6, rowspan=2, sticky=('N', 'E', 'S', 'W'))
    guessed.grid(column=0, row=2, columnspan=6, rowspan=2, pady=10)
    game_msg.grid(column=0, row=4, columnspan=6, rowspan=2, pady=5)
    change_name.grid(column=0, row=6, columnspan=1, rowspan=1, pady=5)
    change.grid(column=1, row=6, columnspan=1, rowspan=1, pady=10)
    guess_.grid(column=2, row=6, columnspan=1, rowspan=1, pady=10, padx=20)
    enter.grid(column=3, row=6, columnspan=1, rowspan=1, pady=10, padx=1)
    new.grid(column=4, row=6, columnspan=1, rowspan=1, pady=10, padx=1)
    quit_.grid(column=5, row=6, columnspan=1, rowspan=1, pady=10, padx=1)

    win.columnconfigure(0, weight=1)
    win.rowconfigure(0, weight=1)

    win.resizable(False, False)
    win.mainloop()


if __name__ == '__main__':
    play()
