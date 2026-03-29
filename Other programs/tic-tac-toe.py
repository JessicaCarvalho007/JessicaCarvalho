def play(board, mark='X', winner=False):
    i = 0
    moves = list()
    while not winner:
        for row in board:
            for col in row:
                print(col, end='')
            print()
        print()

        i += 1
        if i == 10:
            print('This game was a Push')
            break

        loc = {'7': [0, 0], '8': [0, 1], '9': [0, 2],
               '4': [1, 0], '5': [1, 1], '6': [1, 2],
               '1': [2, 0], '2': [2, 1], '3': [2, 2]}
        move = 'Get net move position'
        while not move.isdigit() or not int(move) in range(1, 10) or move in moves:
            move = input('Select your next play (1-9):\n')
        moves.append(move)
        row, col = loc[move]
        mark = mark if i % 2 == 1 else 'O'
        board[row][col] = mark

        winner = check_game(board)
    return board, mark


def check_game(board):
    """

    :param board:
    :return:
    """
    # Row Check
    for r in range(len(board)):
        row_set = [board[r][0], board[r][1], board[r][2]]
        if '-' not in row_set and len(set(row_set)) == 1:
            return True
    # Column Check
    for c in range(len(board)):
        col_set = [board[0][c], board[1][c], board[2][c]]
        if '-' not in col_set and len(set(col_set)) == 1:
            return True
    # Diagonal Checks
    di1 = [board[0][0], board[1][1], board[2][2]]
    di2 = [board[-1][-1], board[-2][-2], board[-3][-3]]
    if len(set(di1)) == 1 and '-' not in di1 or len(set(di2)) == 1 and '-' not in di2:
        return True


def main():
    board = [['-' for _ in range(3)] for _ in range(3)]
    board, mark = play(board)
    for row in board:
        for col in row:
            print(col, end='')
        print()
    print(f'Game Over "{mark}" wins!')


if __name__ == '__main__':
    main()
