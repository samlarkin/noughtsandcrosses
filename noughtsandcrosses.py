"""noughtsandcrosses

A simple implementation of noughts and crosses (tic tac toe), playable at the
command line (with two players using a single computer).

"""
from random import choice


MARKERS = "OX"
EMPTY_STATE = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "],
]


class Player:
    """Player in the game of noughts and crosses"""

    def __init__(self, name, marker):
        """Initialise player with a name and marker (O or X)

        Args:
            name (str): Player name
            marker (str): Player marker (O or X)

        """
        self.name = name
        self.marker = marker

    def __repr__(self):
        return f"Player {marker}: {self.name}"


class Board:
    """Noughts and crosses game board"""

    def __init__(self, state=EMPTY_STATE):
        """Set up the game board for noughts and crosses

        Initialises Board.state as a 2D list representing the 3x3 game board,
        displays the board to the players and randomly selects the player (O or
        X) to make the first move.

        """
        self.state = state
        self.mover = choice(MARKERS)
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
            i = MARKERS.index(self.mover) - 1
            self.mover = MARKERS[i]

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

            try:
                # Validate user input
                assert len(coord) == 2

                x_key = coord[0].lower()
                col_index = int(coord[1])

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


class GamePvP:
    """Player vs Player game of noughts and crosses"""

    def __init__(self, state, players):
        """Set up a game of noughts and crosses between two players"""
        self.board = Board(state)
        self.players = (Player(*players[0]), Player(*players[1]))

    def is_won(self):
        """Returns True if the game has been won else returns false

        Transposes the board state and gets the diagonals, then checks whether
        any of the 'combinations' i.e. rows, columns, and diagonals, is a
        matching set of 3 X or 3 O marks (meaning the game has been won).

        """
        rows = self.board.state
        cols = [list(col) for col in zip(*rows)]
        diags = [
            [rows[0][0], rows[1][1], rows[2][2]],
            [rows[0][2], rows[1][1], rows[2][0]]
        ]
        combinations = rows + cols + diags

        for sequence in combinations:
            if _three_in_a_row(sequence):
                return True
        return False

    def is_over(self):
        """Returns True if the game is over else returns False"""
        if self.is_won() is True:
            return True

        for row in self.board.state:
            if " " in row:
                return False
        return True

    def save(self, fn):
        """Save game to json file"""
        pass

    def load(self, fn):
        """Load game from json file"""


def _three_in_a_row(seq):
    """Checks if a list meets the three in a row winning condition

    Args:
        seq(list): Sequence of values to check for three in a row

    Returns:
            bool: True if winning condition is met else false

    """
    if seq[0] == seq[1] and seq[0] == seq[2] and MARKERS.find(seq[0]) != -1:
        return True
    return False


def main():
    """Main game logic"""
    game = GamePvP(EMPTY_STATE, players=(("Tom", "O"), ("Jerry", "X")))

    while not game.is_over():
        game.board.move()
        game.board.end_turn()

    if game.is_won():
        winner = MARKERS.replace(game.board.mover, "")
        print(f"Congratulations, {winner}! You have won!")

    else:
        print("Draw")


if __name__ == "__main__":
    main()
