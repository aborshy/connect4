import numpy as np
import itertools

program_on = True


class Connect:

    def __init__(self):
        self.board = np.full((6, 7), " ")
        self.turn = None
        self.piece = 'x'
        self.turn = 1
        self.playing = True

    def change_turn(self):
        """
        changes piece and turn when called
        :return: None
        """
        if self.turn == 1:
            self.turn = 2
            self.piece = 'o'
        else:
            self.turn = 1
            self.piece = 'x'

    def display(self):
        """
        displays current board
        :return: None
        """
        for x in self.board:
            print("|" + "|".join(x) + "|")

    def play(self):
        """
        takes in valid input from prompt, checks if there is room to place piece, and places piece
        """
        valid_state = False
        while not valid_state:
            input_var = -1
            try:
                input_var = int(input(f"Player {self.turn}, please enter valid empty column (1-7)"))
            except ValueError:
                pass
            input_var -= 1
            if input_var in range(0, (len(self.board[0]))) and ' ' in ''.join(self.board[:, input_var]):
                valid_state = True

        drop_col = self.board[:, input_var]
        drop_col = ''.join(drop_col[::-1])
        drop_col = drop_col.replace(" ", self.piece, 1)
        self.board[:, input_var] = [x for x in drop_col[::-1]]

    def check(self):
        """
        generates lists of all rows, columns, forward diagonals and backward diagonals and checks all for substrings
        'oooo' or 'xxxx' (in the future could not use set substrings, rather concatenate or multiply the piece used,
        and also checks if board is full for tie
        """
        max_col = len(self.board[0])
        max_row = len(self.board)
        cols = [[] for _ in range(max_col)]
        rows = [[] for _ in range(max_row)]
        fdiag = [[] for _ in range(max_row + max_col - 1)]
        bdiag = [[] for _ in range(len(fdiag))]
        min_bdiag = -max_row + 1

        for x in range(max_col):
            for y in range(max_row):
                cols[x].append(self.board[y][x])
                rows[y].append(self.board[y][x])
                fdiag[x + y].append(self.board[y][x])
                bdiag[x - y - min_bdiag].append(self.board[y][x])

        cols = [''.join(x) for x in cols]
        rows = [''.join(x) for x in rows]
        fdiag = [''.join(x) for x in fdiag if len(x) > 3]
        bdiag = [''.join(x) for x in bdiag if len(x) > 3]

        win_list = ['xxxx', 'oooo']
        check_list = list(set((itertools.chain(cols, rows, fdiag, bdiag))))
        current_board = self.board.flatten()

        # check for win
        for x in check_list:
            if x.find(win_list[0]) >= 0 or x.find(win_list[1]) >= 0:
                self.playing = False
                break

        # check if full
        if len([x for x in current_board if x != " "]) == len(current_board):
            print('tie!')
            self.playing = False


while program_on:
    game = Connect()
    while game.playing:
        game.display()
        game.play()
        game.check()
        if game.playing:
            game.change_turn()
        else:
            game.display()
            print(f'Player {game.turn} has won!')
