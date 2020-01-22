#############################################################
# FILE : game.py
# WRITERS :  Nadav_Meidan, nadav.meidan, 200990240
#            Mattan Yeroushalmi, mattan, 312292584
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : A program that processes the moves in the game and updates
# the board. It handles the logic of the game and is used to determine if
# there has been a win.
#############################################################

import time
from tkinter import messagebox
# Directions to go over when checking for a winner.
DIRECTIONS = {'r': (0, 1), 'd': (1, 0), 'w': (1, -1), 'z': (1, 1)}


class Game:
    """
    The game class is in charge of executing all of the functions pertaining to
    the board: Checking for a win after every turn, making sure that
    there is room in the column, placing the discs in the right location, etc.
    """
    MIN_X, MIN_Y = 0, 0 # Top left coordinate.
    HEIGHT, WIDTH = 6, 7 # The board size.
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2 # Not Used

    def __init__(self):
        #  Initializes the board as a dictionary of keys: Tuples of coordinates.
        #                       values: 1 or 0 depending on the current player.
        self.__board = self.create_board()
        # The winner will be set to 0 if player 1 is the winner and 1 if
        # player 2 is the winner.
        self.__winner = None
        # The default starting player is player one.
        self.__current_player = self.PLAYER_ONE
        # The last move that was made as a tuple.
        self.__last_move = None

    def is_tie(self):
        """
        Determines whether there is a tie by going over the board dictionary.
        :return: False or True depending on Tie state.
        """
        for value in self.__board.values():
            if value == None:
                return False
        return True

    def is_win(self):
        """
        Determines if there is a win state by checking for four discs in a
        row.
        :return: In case of a winL The winning tuples in the board dictionary
        and the winner. Otherwise: False.
        """
        curr_player = self.__current_player
        last_x, last_y = self.__last_move
        board = self.__board

        for direction in DIRECTIONS.values():
            tuple_list = list()
            # The search for a winning series of discs is made by scanning
            # the board in the directions supplied. This is done by
            # multiplication of the direction tuple.
            x_dir = direction[0]
            y_dir = direction[1]

            for i in range(-3, 4):
                current_coordinate = last_x + i * x_dir, last_y + i * y_dir
                # make sure that the tuple is in the range.
                if current_coordinate in board.keys():
                    if board[current_coordinate] == curr_player:
                        streak_coordinates = current_coordinate
                        tuple_list.append(streak_coordinates)
                    else: # empty the list
                        tuple_list = list()
                if len(tuple_list) == 4: # this means that a player has won.
                    return tuple_list, curr_player
        return False

    def make_move(self, column):
        """
        Places a disc in the next available spot. If full, raises an exception.
        :param column: Column to place the disc in
        """
        for row in range(self.HEIGHT - 1, self.MIN_X -1, -1):
            if self.__board[row, column] == None:
                self.__board[row, column] = self.__current_player
                self.__last_move = row, column
                return
        raise Exception("Illegal Move!")

    def create_board(self):
        """
        Initialize the board dictionary.
        :return: The board dictionary.
        """

        board = dict()
        for i in range(Game.HEIGHT):
            for j in range(Game.WIDTH):
                board[i, j] = None
        return board

    def get_last_move(self):
        """
        :return: The last move that was made.
        """
        return self.__last_move

    def get_winner(self):
        """
        :return: The winner of the game.
        """
        return self.__winner

    def get_board(self):
        """
        :return: The board dictionary.
        """
        return self.__board

    def get_player_at(self, row, col):
        # Not used.
        return self.__board[row, col]

    def set_winner(self, winner):
        """
        :param winner: Set the winner to player one or player two.
        """
        self.__winner = winner

    def get_current_player(self):
        """
        :return: The current player.
        """
        return self.__current_player

    def set_current_player(self, cur_player):
        """
        :param cur_player: player one or player two.
        """
        self.__current_player = cur_player
