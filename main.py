from random import choice


class Board:
    def __init__(self):
        row = [' '] * 3
        self.state = [row[:], row[:], row[:]]
        self.first_move = choice('OX')
        self.show()
        print(f"{self.first_move} Move first (randomly selected)")
        self.mover = self.first_move

    def show(self):
        col_names = '     A   B   C  '
        hline = '   +---+---+---+'
        print(col_names)
        print(hline)
        for index, row in enumerate(self.state):
            print(f'{index}  | {row[0]} | {row[1]} | {row[2]} |')
            print(hline)

    def end_turn(self):
        if self.mover == 'O':
            self.mover = 'X'
        elif self.mover == 'X':
            self.mover = 'O'
        else:
            raise ValueError('mover should be O or X')
        self.show()

    def move(self, coord):
        try:
            assert isinstance(coord, str)
            assert len(coord) == 2
        except AssertionError:
            print('Coordinate must be a string of the form: A0')
            player_input = input(f'Make your move, player {self.mover}!\n')
            self.move(player_input)
            return

        try:
            x_map = {'a': 0, 'b': 1, 'c': 2}
            x = x_map[coord[0].lower()]
            y = int(coord[1])
            assert self.state[y][x] == ' '
            self.state[y][x] = self.mover
        except IndexError:
            print('Coordinate must be a string of the form: A0')
            player_input = input(f'Make your move, player {self.mover}!\n')
            self.move(player_input)
            return
        except AssertionError:
            print('Invalid move. Pick an empty square.')
            player_input = input(f'Make your move, player {self.mover}!\n')
            self.move(player_input)
            return
        self.end_turn()

    def _check_rows(self):
        for row in self.state:
            if _three_in_a_row(row) is True:
                return True
        return False

    def _check_cols(self):
        cols = [[], [], []]
        for row in self.state:
            for index, entry in enumerate(row):
                cols[index].append(entry)
        for col in cols:
            if _three_in_a_row(col) is True:
                return True
        return False

    def _check_diags(self):
        diags = [
            [self.state[0][0], self.state[1][1], self.state[2][2]],
            [self.state[0][2], self.state[1][1], self.state[2][0]]
        ]
        for diag in diags:
            if _three_in_a_row(diag) is True:
                return True
        return False

    def game_won(self):
        if self._check_rows() is True:
            return True
        elif self._check_cols() is True:
            return True
        elif self._check_diags() is True:
            return True
        return False

    def stalemate(self):
        if self.game_won() is True:
            return False
        for row in self.state:
            if ' ' in row:
                return False
        print('Stalemate. No more valid moves are possible.')
        return True

    def game_over(self):
        if self.game_won() is True:
            return True
        elif self.stalemate() is True:
            return True
        return False


def _three_in_a_row(seq):
    if seq[0] == seq[1] and seq[1] == seq[2] and seq[0] != ' ':
        return True
    return False


def congratulate(winner):
    print(f'Congratulations, {winner}! You have won!')


def main():
    board = Board()
    while board.game_over() is False:
        player_input = input(f'Make your move, player {board.mover}!\n')
        board.move(player_input)
    if board.stalemate() is False:
        winner = 'OX'.replace(board.mover, '')
        congratulate(winner)


if __name__ == '__main__':
    main()
