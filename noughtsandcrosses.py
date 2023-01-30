"""noughtsandcrosses

A simple implementation of noughts and crosses (tic tac toe), playable at the
command line (with two players using a single computer).

"""
from random import choice


class Board:
    """Noughts and crosses game board"""

    def __init__(self):
        """Set up the game board for noughts and crosses

        Initialises Board.state as a 2D list representing the 3x3 game board,
        displays the board to the players and randomly selects the player (O or
        X) to make the first move.

        """
        row = [" "] * 3
        self.state = [row[:] for _ in range(3)]
        self.mover = choice("OX")
        print(self)
        print(f"\n{self.mover} moves first (randomly selected)")

    def __repr__(self):
        """Displays the game board"""
        col_names = "     A   B   C  "
        hline = "   +---+---+---+"
        repr_lines = [col_names, hline]

        for index, row in enumerate(self.state):
            repr_lines.append(f"{index}  | {row[0]} | {row[1]} | {row[2]} |")
            repr_lines.append(hline)

        return "\n".join(repr_lines)

    def end_turn(self):
        """End the current player's turn

        Changes Board.mover at end of current player's (i.e. Board.mover's)
        turn and displays the board to the players.

        """
        try:
            i = "OX".index(self.mover) - 1
            self.mover = "OX"[i]

        except ValueError:
            print(f"Something went wrong! Current player should be O or X, " \
                  f"not {self.mover}")

        print(self)

    def move(self):
        """Allows player to make a move

        Receives player input, validates it and places that player's marker.
        Loops until valid player input is received.

        """
        x_map = {"a": 0, "b": 1, "c": 2}

        while True:
            coord = input(
                f"\nMake your move, player {self.mover}!\n" \
                f"Type the coordinates (e.g. A0) of the square in \n" \
                f"which you would like to place a marker:\n..."
            )
            print()

            x_key = coord[0].lower()
            col_index = int(coord[1])

            try:
                # Validate user input
                assert len(coord) == 2
                assert x_key in ["a", "b", "c"]
                assert col_index in [0, 1, 2]
                row_index = x_map[x_key]
                assert self.state[col_index][row_index] == " "
                break

            except AssertionError:
                print(
                    "Invalid input. Coordinate must be of the form A0, B1 \n" \
                    "etc. (case insensitive), and must correspond to an \n" \
                    "empty square on the game board."
                )
                continue

        # Place current player's mark in the selected location
        self.state[col_index][row_index] = self.mover

    def game_won(self):
        """Returns True if the game has been won else returns false

        Transposes the board state and gets the diagonals, then checks whether
        any of the 'combinations' i.e. rows, columns, and diagonals, is a
        matching set of 3 X or 3 O marks (meaning the game has been won).

        """
        cols = [list(col) for col in zip(*self.state)]
        diags = [
            [self.state[0][0], self.state[1][1], self.state[2][2]],
            [self.state[0][2], self.state[1][1], self.state[2][0]]
        ]
        combinations = self.state + cols + diags

        for combo in combinations:
            if _three_in_a_row(combo):
                return True

        return False

    def game_over(self):
        """Returns True if the game is over else returns False"""
        if self.game_won() is True:
            return True

        for row in self.state:
            if " " in row:
                return False

        return True


def _three_in_a_row(seq):
    """Checks if a list meets the three in a row winning condition

    Args:
        seq(list): Sequence of values to check for three in a row

    Returns:
            bool: True if winning condition is met else false

    """
    if seq[0] == seq[1] and seq[0] == seq[2] and "OX".find(seq[0]) != -1:
        return True

    return False


def main():
    """Main game logic"""
    board = Board()

    while not board.game_over():
        board.move()
        board.end_turn()

    if board.game_won():
        winner = "OX".replace(board.mover, "")
        print(f"Congratulations, {winner}! You have won!")

    else:
        print("Draw")


if __name__ == "__main__":
    main()
