import random
import copy

class RandomAI:
    '''AI class playing random moves'''
    def __init__(self):
        pass

    def move(self, board):
        return random.choice(board.possible_moves())

class MiniMaxAI:
    '''AI class playing best possible moves'''
    def __init__(self, player):
        self.player = player
        self.human = "X" if player == "O" else "O"

    def minimax(self, board, maximizing=False):
        '''Implementation of MiniMax algorithm'''
        if board.check_board() == self.human:
            return 1, None
        elif board.check_board() == self.player:
            return -1, None
        elif board.check_board() == 'D':
            return 0, None

        if maximizing:
            bestval = -10
            best_move = None
            for (i, j) in board.possible_moves():
                board_copy = copy.deepcopy(board)
                board_copy.mark_space(i, j, self.human)
                value = self.minimax(board_copy, False)[0]
                if value > bestval:
                    bestval = value
                    best_move = (i, j)
            return bestval, best_move

        else:
            bestval = 10
            best_move = None
            for (i, j) in board.possible_moves():
                board_copy = copy.deepcopy(board)
                board_copy.mark_space(i, j, self.player)
                value = self.minimax(board_copy, True)[0]
                if value < bestval:
                    bestval = value
                    best_move = (i, j)
            return bestval, best_move

    def move(self, board):
        if board.isempty():
            return random.choice(board.possible_moves())
        return self.minimax(board)[1]

class Board:
    
    def __init__(self):
        self.board = [ # 3x3 tic-tac-toe board
            ['-','-','-'],
            ['-','-','-'],
            ['-','-','-']
            ]

    def print(self):
        for row in self.board:
            print('|'.join(row))

    def possible_moves(self):
        empty = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    empty.append((i,j))
        return empty
    
    def isfull(self):
        if len(self.possible_moves()) == 0:
            return True
        return False

    def isempty(self):
        if len(self.possible_moves()) == 9:
            return True
        return False

    def mark_space(self, i, j, player):
        self.board[i][j] = player

    def check_board(self):
        Xs_placed = [[self.board[i][j] == 'X' for j in range(3)] for i in range(3)] + \
                    [[self.board[j][i] == 'X' for j in range(3)] for i in range(3)] + \
                    [[self.board[i][i] == 'X' for i in range(3)]] + \
                    [[self.board[i][2-i] == 'X' for i in range(3)]]
        Os_placed = [[self.board[i][j] == 'O' for j in range(3)] for i in range(3)] + \
                    [[self.board[j][i] == 'O' for j in range(3)] for i in range(3)] + \
                    [[self.board[i][i] == 'O' for i in range(3)]] + \
                    [[self.board[i][2-i] == 'O' for i in range(3)]]

        for triple in Xs_placed:
            if triple == [True] * 3:
                return 'X' # returns 'X' if there are 3 Xs in any row/column/slant 
        for triple in Os_placed:
            if triple == [True] * 3:
                return 'O' # returns 'O' if there are 3 Os in any row/column/slant 
        if self.isfull():
            return 'D' # returns 'D' if there is a draw
        return

class Game:
    
    def __init__(self, ai_type, player):
        self.board = Board()
        if ai_type=='random': self.ai = RandomAI() 
        else: self.ai = MiniMaxAI(player)
        self.player = 'X'

    def next_turn(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
    
    def move(self, i, j):
        if self.board.board[i][j] == '-':
            self.board.board[i][j] = self.player
        else:
            print('Space is not empty!')
            self.next_turn()

def main():

    ai_type = input('Choose AI type ("random" or "minimax")')
    if ai_type not in ["random","minimax"]:
        raise Exception('Wrong input! Choose "random" or "minimax" AI')
    human_player = input('Choose "X" or "O"')
    if human_player not in ["X","O"]:
        raise Exception('Wrong input! Choose "X" or "O"')
    if human_player == "X": ai_player = "O" 
    else: ai_player = "X"
    
    game = Game(ai_type, ai_player)
    board = game.board
    ai = game.ai

    board.print()

    while True:

        if game.player == human_player:
            while True:
                i = int(input(f'Choose row to place {human_player}: (0-2)'))
                j = int(input(f'Choose column to place {human_player}: (0-2)'))
                if i in [0, 1, 2] and j in [0, 1, 2]:
                    break
                else:
                    print("Choose row and column from 0, 1, 2")
        elif game.player == ai_player:
            i, j = ai.move(board)
            print(f'AI plays {ai_player} in row {i} column {j}')
        game.move(i, j)
        board.print()

        state = board.check_board()
        if state in ['X','O']:
            print(f"{state} wins!")
            break
        elif state == 'D':
            print("It's a draw!")
            break
        game.next_turn()


if __name__ == '__main__':
    main()
