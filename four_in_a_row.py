#############################################################
# FILE : four_in_a_row.py
# WRITERS :  Nadav_Meidan, nadav.meidan, 200990240
#            Mattan Yeroushalmi, mattan, 312292584
# EXERCISE : intro2cs ex12 2017-2018
# DESCRIPTION : A program that runs the game and the GUI.
#############################################################

import socket
import sys
import tkinter as t
from tkinter import messagebox
from communicator import Communicator

MIN_PORT, MAX_PORT = 0, 65535 # Minimum and maximum legal ports.


class GUI:
    """
    Designed to handle the GUI aspects (creating a window, buttons and
    pop-ups. Also initializes the communicator object, the game object and
    the AI object.
    """

    SCALAR = 99  # Determines the screen size and the sizes of objects
    # within it. Any int or float will work.
    # **The dimensions of the screen must be kept at a 6 to 7 ratio for the
    # game to work correctly.**
    WIDTH = 7*SCALAR  # Width of the screen in pixels
    HEIGHT = 6*SCALAR  # Height of the screen in pixels

    def __init__(self, game, master, port, player=None,
                 ip=None):
        """
        Initializes the GUI and connects the communicator and the AI.
        :param game: The game class which includes the logic of the game.
        :param master: The tkinter root.
        :param port: The port to connect to.
        :param player: The player to start as. If server then player one,
        if client then player two.
        :param ip: The ip address of the server. to be left None if the
        instance is server.
        """
        self._master = master  # The tkinter root.

        self._canvas = t.Canvas(self._master, width=self.WIDTH,
            height=self.HEIGHT, highlightthickness=0)  # The tkinter canvas.
        # The AI class which is to be activated only when the game is not
        # human vs. human.
        self._AI = AI()
        self._game = game
        # The communicator class which is in charge of communication between
        # server and client.
        self.__communicator = Communicator(root, port, ip)
        # Connects between instances of the game.
        self.__communicator.connect()
        # Binds the message handler to incoming messages.
        self.__communicator.bind_action_to_message(self.__handle_message)
        # __columns: A dictionary of keys: Column numbers.
        #                            values: The columns' item IDs.
        # __discs: A dictionary of keys: Coordinates on the board.
        #                          values: The Discs' item IDs.
        self.__columns, self.__discs = self.shapes()
        # if the instance is AI, is_human changes to False.
        self.__is_human = True
        self.__player = player

    def set_is_human(self, is_human):
        """
        Sets the __is_human attribute to true if the player is human and
        false if the player is 'AI'.
        :param is_human: True if human or False if AI
        """
        self.__is_human = is_human

    def event_handler(self, column, msg=False):
        """
        The function to be activated when a move is made by one of the players.
        Calls all the necessary functions to be executed when a
        turn has been made.
        :param column: The column which was clicked by a player.
        :param msg: Determines whether the move was made by the current
        player or by the other player.
        :return: None.
        """
        if msg:
            self._game.make_move(column)
            self.add_disc()
            self.win()
            self.tie()

        elif self.__player == self._game.get_current_player() and \
                self._game.get_winner() == None:
            self._game.make_move(column)
            self.add_disc()
            self.__communicator.send_message(str(column))
            self.win()
            self.tie()

    def add_disc(self):
        """
        Adds a disc to the screen according to the coordinates supplied by
        the "make move" function. Add a green or red disc depending on who
        the current player is.
        :return: None.
        """
        game = self._game
        y, x = game.get_last_move()
        item_id = self.__discs[x, y]
        if game.get_current_player() == game.PLAYER_ONE:
            self._canvas.itemconfig(item_id, fill="#af0707", outline=
            '#751810')
        else:
            self._canvas.itemconfig(item_id, fill="#096300", outline=
            '#203d11')

    def shapes(self):
        """
        The function that draws the initial board. Generates all of the
        necessary shapes by using the helper functions.
        :return: A dictionary of columns and a dictionary of discs.
        """
        self._canvas.pack()
        column_dict = {k: None for k in range(int(self.WIDTH / self.SCALAR))}
        disc_dict = self._game.create_board()
        for i in range(int(self.WIDTH / self.SCALAR)): # Creates columns.
            color = self.color_generator \
                (index=i, RGB=(0, 0, 0, 0, 3, 0), oval=False)
            rectangle = self.draw_column(i, color)
            column_dict[i] = rectangle  # adds to column dictionary.
            for j in range(int(self.HEIGHT / self.SCALAR)): # Creates discs.
                color = self.color_generator(index=(i, j),
                                    RGB=(1, 0, 0, 0, 2, 1), oval=True)
                oval = self.draw_oval(i, j, color)
                disc_dict[i, j] = oval  # adds to disc dictionary.
        return column_dict, disc_dict

    def key_bind(self, object, index):
        """
        Binds Left mouse
        button to event handler, as well as 'enter' and 'leave' to the current
        player signal (changing the column color).
        :param object: Type of object to bind.
        :index: Column index of the object.
        """
        self._canvas.tag_bind(object, '<Button-1>',
                              lambda event: self.event_handler(index, False))
        self._canvas.tag_bind(object, '<Enter>',
                              lambda event: self.column_config(index, True))
        self._canvas.tag_bind(object, '<Leave>',
                              lambda event: self.column_config(index, False))

    def draw_oval(self, i, j, color):
        """
        Creates The oval objects to be displayed on screen.
        :param i: Current column index.
        :param j: Current row index.
        :param color: The shade to fill the oval with.
        :return: Creates an oval object
        """
        scaled_i, scaled_j = i * self.SCALAR, j * self.SCALAR
        tlo = self.SCALAR*0.2  # top left offset
        bro = self.SCALAR*0.8  # bottom right offset
        oval = self._canvas.create_oval(scaled_i + tlo, scaled_j + tlo,
                                        scaled_i + bro, scaled_j + bro,
                                        fill=color, outline='', width=2)
        self.key_bind(oval, i)
        return oval

    def draw_column(self, i, color):
        """
        Used for the initial drawing of columns to the screen. Binds Left mouse
        button to event handler, as well as 'enter' and 'leave' to the current
        player signal (changing the column color).
        :param canvas: Canvas to draw on.
        :param i: Current column index.
        :param color: Fill color of the column.
        :return: Creates a column (rectangle object) on the screen.
        """
        scaled_i = self.SCALAR * i
        tlo = 0  # top left offset
        rectangle = self._canvas.create_rectangle(scaled_i, tlo, scaled_i +
                            self.SCALAR,self.HEIGHT, fill=color, outline='')
        self.key_bind(rectangle, i)
        return rectangle

    def column_config(self, i, enter):
        """
        Changes the color of the column on mouse over depending on the
        current player. If it is not the instance's turn, the column will be
        grayed out to avoid confusion and still let the player know that the
        game is not stuck.
        :param i: Column index.
        :param enter: True if 'enter' event, False if 'leave' event.
        """
        current_player = self._game.get_current_player()
        item_id = self.__columns[i]
        if enter and self.__player == current_player:
            if self.__player == self._game.PLAYER_ONE:
                self._canvas.itemconfig(item_id, fill='#720d0d')
            else:
                self._canvas.itemconfig(item_id, fill='#16720d')
        elif enter and self.__player != current_player:
            self._canvas.itemconfig(item_id, fill='#555555')
        elif not enter:
            color = self.color_generator(index=i, RGB=(0, 0, 0, 0, 3, 0),
                                         oval=False)
            self._canvas.itemconfig(item_id, fill=color)

    def color_generator(self, index, RGB, oval):
        """
        A function that is used to generate the various shades that are
        utilized in the initial creation of the board. The formula for the
        coloring of the ovals was found solely through rigorous trial and
        error. This gives the illusion of a gradient background.
        :param index: When sent from oval, this is a tuple of the row and
        column. This enables the illusion of a gradient background. When
        sent from a rectangle, it is the column index.
        :param RGB: The amount of Red, Green and Blue. Every two items in
        the list represent the amount of each color in hex - 00 being the
        minimum and FF being the maximum.
        :param oval: True if the object being colored is an oval, False if
        it is a rectangle.
        :return: A hexadecimal color code.
        """
        color_hex_string = '#'
        if oval == True:
            shade = int((index[0] + index[1]))
        else:
            shade = int(index)
        for ind in RGB:
            color_hex_string += hex(shade + ind)[2:]
        return color_hex_string

    def __handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Upon reception of a message, sends the column number to
        the event handler.
        :param text: the number of the column to place a disc in.
        """
        if text:
            column = int(text)
            self.event_handler(column, True)

        if not self.__is_human:
            self._AI.find_legal_move(self.event_handler)

    def win(self):
        """
        Sets the winning four animation if there is a win and calls the
        message box function, otherwise changes the current player.
        """
        game = self._game
        if game.is_win():
            tuple_list, curr_player = game.is_win()
            if curr_player == game.PLAYER_ONE:
                outline = '#ff851c'
                game.set_winner(game.PLAYER_ONE)
            else:
                outline = '#00ff00'
                game.set_winner(game.PLAYER_TWO)
            for tuple in tuple_list:
                x, y = tuple
                item_id = self.__discs[y, x]
                self._canvas.itemconfig(item_id, outline=outline, dash=5,
                                        width=3)
            self.win_message()
        if game.get_current_player() == game.PLAYER_ONE:
            game.set_current_player(game.PLAYER_TWO)
        else:
            game.set_current_player(game.PLAYER_ONE)

    def tie(self):
        """
        The Tie message box.
        """
        if self._game.is_tie():
            if messagebox.showinfo('Game Over', 'It\'s a Tie!'):
                self._master.destroy()


    def win_message(self):
        """
        The Win Message boxes.
        """
        if self._game.get_current_player() == self._game.PLAYER_ONE:
            if t.messagebox.showinfo('Game Over!', 'Red Wins'):
                self._master.destroy()
        if self._game.get_current_player() == self._game.PLAYER_TWO:
            if t.messagebox.showinfo('Game Over!', 'Green Wins'):
                self._master.destroy()

def check_arguments():
    """
    Check to see that the arguments are legal.
    :return: True or False according to the number of arguments and port.
    """
    arguments = sys.argv
    server = True
    if len(arguments) not in (3, 4) or int(sys.argv[2]) > MAX_PORT or \
                    int(sys.argv[2]) < MIN_PORT:
        print('‪Illegal‬‬ ‫‪program‬‬ ‫‪arguments.‬‬')
    if len(arguments) == 4:
        server = False
    return server # False if client.

if __name__ == '__main__':
    # For some reason these imports failed on the computers in the lab when
    # they were placed up top.
    from game import Game
    from ai import AI
    server = check_arguments()
    root = t.Tk()
    root.resizable(False, False)
    game_object = Game()
    if server:
        player = game_object.PLAYER_ONE
        gui = GUI(game_object, root, int(sys.argv[2]), player, None)
        if sys.argv[1] == 'ai':
            gui.set_is_human(False)
            #if the ai has to make the first move, call the make move function.
            AI.find_legal_move(gui._AI, gui.event_handler)
        root.title("Server")
    else:
        player = game_object.PLAYER_TWO
        gui = GUI(game_object, root, int(sys.argv[2]), player, sys.argv[3])
        if sys.argv[1] == 'ai':
            gui.set_is_human(False)
        root.title("Client")
    root.mainloop()
