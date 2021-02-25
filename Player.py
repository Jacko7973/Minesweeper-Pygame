import os
import numpy as np

class Player:

    def __init__(self, board_size):
        self.board_size = board_size
        self.solved_positions = []

    def get_choice(self, board):
        odds = {}

        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == -1:
                    if any(board[nei[1]][nei[0]] != -1 for nei in self.get_neighbors((x, y))): odds[(x, y)] = 0

        arrangement = {}
        for key in odds.keys(): arrangement[key] = False
        self.enum_bombs(board, arrangement)


    def enum_bombs(self, board, arrangement, ar_list=[]):
        for (x, y) in arrangement.keys():
            if not arrangement[(x, y)]:
                arrangement[(x, y)] = True
                if self.evaluate_board(board, arrangement):
                    print('evaluated true')
                    if arrangement not in ar_list: ar_list.append(arrangement.copy())
                    self.enum_bombs(board, arrangement, ar_list)
                arrangement[(x, y)] = False

    
    def evaluate_board(self, board, arrangement):
        return False
                    



    def get_neighbors(self, pos):
        (x, y) = pos
        options = [(x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]

        for option in options[:]:
            if any(option[i] < 0 or option[i] >= self.board_size[i] for i in range(len(option))): options.remove(option)

        return options

