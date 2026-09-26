import typing
import time



from enum import Enum

from NeoTrellisGame import NeoTrellisGame, AbstractNeoTrellisGame, Action
from adafruit_neotrellis.multitrellis import MultiTrellis
from adafruit_neotrellis.neotrellis import NeoTrellis

WIDTH = 8
HEIGHT = 8

ROWS = 6
COLS = 8

CONTROL_ROW = 0
RESET_COL = 7
BOARD_START_ROW = 2

OFF = (0, 0, 0)
PLAYER1 = (255, 40 , 40)
PLAYER2 = (40, 40, 255)
RESET = (40, 255, 40)

class ConnectFour:
    def __init__(self, board: typing.Optional[AbstractNeoTrellisGame] = None):
        self.board = board if board is not None else NeoTrellisGame()
        super().__init__()
        self.game_state = [[OFF] * COLS for _ in range(ROWS)] #TODO: Choose a structure to represent what pieces are currently in the game board
        self.current_player = PLAYER1
        self.game_over = False
        self.register_callbacks()
        self.reset_game()
        self.board.play_sound("clack.mp3")

    def reset_game(self):
        self.game_state = [[OFF] * COLS for _ in range(ROWS)]
        self.current_player = PLAYER1
        self.update_board_colors()

    def register_callbacks(self):
        #TODO: Register callbacks that will be run when buttons are pressed and released
        for i in range(8):
            self.board.set_callback(i, 0, self.handle_button_event) # Example of how to register a callback (function) for button 0, 0. Must be done for every button that runs a function
            self.board.activate_key(i, 0, Action.BUTTON_PRESSED) # Even though the callback is set, if the key is not enabled it will not be run. This is how you enable
    def handle_button_event(self, x:int, y: int, action: Action):
        if self.game_over:
            self.reset_game()

        if y != CONTROL_ROW or self.is_column_full(x):
            print("Not top row or column full")
            return

        print("in handle button")
        color = self.get_player_color(self.current_player)
        placed_row = self.place_piece(x)
        self.game_state[placed_row][x] = self.current_player

        cells = []

        if self.is_board_full() and self.game_over == False:
            self.show_tie_game
        elif self.game_over and cells is not None:
            pass
        else:
            self.switch_player()
            self.update_board_colors()


    def find_lowest_empty_row(self, col: int):
        for row in range(ROWS -1, -1, -1):
            if self.game_state[row][col] == OFF:
                return row
        return None

    def place_piece(self, col: int):
        target_row = self.find_lowest_empty_row(col)
        print("IN PLACE PIECE")

        if target_row is None:
            return None

        player = self.current_player
        self.game_state[target_row][col] = player
        self.board.set_cell_color(col, target_row + BOARD_START_ROW, player)
        self.board.update_display()

        return target_row

    def update_board_colors(self):
        #TODO: Take the current game state and update the board colors accordingly. Hint: look at NeoTrellisGame.py for functions to update the colors and display the colors
        for col in range(COLS):
            if self.game_over:
                if col == RESET_COL:
                    self.board.set_cell_color(col, CONTROL_ROW, RESET)
                else:
                    self.board.set_cell_color(col, CONTROL_ROW, OFF)
            elif self.is_column_full(col):
                self.board.set_cell_color(col, CONTROL_ROW, OFF)
            elif self.current_player == PLAYER1:
                self.board.set_cell_color(col, CONTROL_ROW, PLAYER1)
            elif self.current_player == PLAYER2:
                self.board.set_cell_color(col, CONTROL_ROW, PLAYER2)
        self.board.play_sound("clack.mp3")
        self.board.update_display()
        return

    def switch_player(self):
        print("In switchPlayer")
        if self.current_player == PLAYER1:
            self.current_player = PLAYER2
        else:
            self.current_player = PLAYER1
        
        print("Current Player: ", self.current_player)

    def is_board_full(self):
        for col in range(COLS):
            if self.is_column_full(col) == False:
                print("NOT FULL")
                return False
        return True

    def get_player_color(self, player) -> tuple[int, int, int]:
        if player == PLAYER1:
            return PLAYER1
        elif player == PLAYER2:
            return PLAYER2
        else:
            return OFF

    def is_column_full(self, col: int):
        for row in range(ROWS - 1):
            if self.game_state[row][col] == OFF:
                print(row)
                return False
        print("FULL")
        return True

    def check_win(self):
        pass

    def show_winner(self):
        #TODO: Display on the board who won
        pass

    def show_tie_game(self):
        #TODO: Display on the board that there was a draw
        pass


