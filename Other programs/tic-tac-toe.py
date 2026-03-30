def play(board, winner=False):
    i = 0
    moves = []

    players = {
        'X': 'Player 1',
        'O': 'Player 2'
    }

    while not winner:
        for row in board:
            for col in row:
                print(col, end=' ')
            print()
        print()

        i += 1
        if i == 10:
            print('This game was a Push')
            return board, None

        mark = 'X' if i % 2 == 1 else 'O'
        print(f"{players[mark]}'s turn ({mark})")

        loc = {
            '7': [0, 0], '8': [0, 1], '9': [0, 2],
            '4': [1, 0], '5': [1, 1], '6': [1, 2],
            '1': [2, 0], '2': [2, 1], '3': [2, 2]
        }

        move = ''
        while not move.isdigit() or int(move) not in range(1, 10) or move in moves:
            move = input('Select your next play (1-9):\n')

        moves.append(move)
        row, col = loc[move]
        board[row][col] = mark

        winner = check_game(board)

    return board, mark


def check_game(board):
    # Row check
    for r in range(3):
        row_set = [board[r][0], board[r][1], board[r][2]]
        if '-' not in row_set and len(set(row_set)) == 1:
            return True

    # Column check
    for c in range(3):
        col_set = [board[0][c], board[1][c], board[2][c]]
        if '-' not in col_set and len(set(col_set)) == 1:
            return True

    # Diagonal checks
    di1 = [board[0][0], board[1][1], board[2][2]]
    di2 = [board[0][2], board[1][1], board[2][0]]

    if ('-' not in di1 and len(set(di1)) == 1) or ('-' not in di2 and len(set(di2)) == 1):
        return True

    return False


def main():
    board = [['-' for _ in range(3)] for _ in range(3)]
    board, mark = play(board)

    players = {
        'X': 'Player 1',
        'O': 'Player 2'
    }

    for row in board:
        for col in row:
            print(col, end=' ')
        print()

    if mark is None:
        print('Game Over - Push!')
    else:
        print(f'Game Over - {players[mark]} wins!')


if __name__ == '__main__':
    main()