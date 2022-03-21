# Diogo Ramalho 86407 & Manuel Manso 86471 Project 1 IA

import exp
import copy
from search import *

import time


# TAI content 
def c_peg ():
    return "O"
def c_empty ():
    return "_"
def c_blocked ():
    return "X"
def is_empty (e):
    return e == c_empty()
def is_peg (e):
    return e == c_peg()
def is_blocked (e):
    return e == c_blocked() 

# TAI pos
# Tuplo (l, c) 
def make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1] 


# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1]

def remove_peg(board, l_initial, c_initial, l_removed, c_removed, l_final, c_final):
    board[l_initial][c_initial] = c_empty()
    board[l_removed][c_removed] = c_empty()
    board[l_final][c_final] = c_peg()
    return board


def board_moves(board):
    moves = []

    number_lines = len(board)
    number_columns=len(board[0])

    for l in range(number_lines):
        for c in range(number_columns):
            if is_peg(board[l][c]):
                if c > 1 and is_peg(board[l][c-1]) and is_empty(board[l][c-2]):
                    moves.append(make_move(make_pos(l,c,), make_pos(l,c-2)))
                if c < number_columns - 2 and is_peg(board[l][c+1]) and is_empty(board[l][c+2]):
                    moves.append(make_move(make_pos(l,c,), make_pos(l,c+2)))
                if l > 1 and is_peg(board[l-1][c]) and is_empty(board[l-2][c]):
                    moves.append(make_move(make_pos(l,c,), make_pos(l-2,c)))
                if l < number_lines - 2 and is_peg(board[l+1][c]) and is_empty(board[l+2][c]):
                    moves.append(make_move(make_pos(l,c,), make_pos(l+2,c)))

    return moves


def board_perform_move(board, move):
    
    board_temp = copy.deepcopy(board)

    l_initial = pos_l(move_initial(move))
    c_initial = pos_c(move_initial(move))
    l_final = pos_l(move_final(move))
    c_final = pos_c(move_final(move))


    if l_initial != l_final:
        if l_initial > l_final:
            board_temp = remove_peg(board_temp, l_initial, c_initial, l_initial-1, c_final, l_final, c_final)
        else:
            board_temp = remove_peg(board_temp, l_initial, c_initial, l_initial+1, c_final, l_final, c_final)
    else:
        if c_initial > c_final:
            board_temp = remove_peg(board_temp, l_initial, c_initial, l_initial, c_initial-1, l_final, c_final)
        else:
            board_temp = remove_peg(board_temp, l_initial, c_initial, l_initial, c_initial+1, l_final, c_final)

    return board_temp


def is_board_solved(board):
    return number_of_pegs(board)==1

def number_of_pegs(board):
    n_pegs = 0
    number_lines = len(board)
    number_columns=len(board[0])


    for l in range(number_lines):
        for c in range(number_columns):
            if(is_peg(board[l][c])):
                n_pegs+=1
    return n_pegs


class sol_state:

    def __init__(self, board):

        global n
        global last_n
        n+=1
        last_n+=1
        if last_n==print_every_n:
            print(n)
            last_n=0


        self.board = board
        self.n_pegs = number_of_pegs(self.get_board())

    def get_board(self):
        return self.board

    def get_number_of_pegs(self):
        return self.n_pegs

    def dec_number_of_pegs(self):
        self.n_pegs-=1;

    def get_number_of_lines(self):
        return len(self.board)

    def get_number_of_columns(self):
        return len(self.board[0])

    def __lt__(self, other_sol_state):
        return other_sol_state.get_number_of_pegs()<self.get_number_of_pegs()

class solitaire(Problem):
    """Models a solitaire problem as a satisfaction problem.
       A solution cannot have more than 1 peg left on the board"""

    def __init__(self, board):
        self.initial = sol_state(board)

    def actions(self, state):
        return board_moves(state.get_board())

    def result(self, state, action):
        return sol_state(board_perform_move(state.get_board(), action))

    def goal_test(self, state):
        return is_board_solved(state.get_board())

    def path_cost(self, c, state1, action, state2):
        return c+1

    def h(self, node):
        """Needed for informed search"""

        board = node.state.get_board()
        lines = node.state.get_number_of_lines()
        columns = node.state.get_number_of_columns()

        #Base h
        h = number_of_pegs(board)*100
        
        #Maximise possible moves
        h-= len(board_moves(board))
        
        for c in range(columns):
            if is_empty(board[0][c]):
                h-=1
            if is_empty(board[lines-1][c]):
                h-=1

        for l in range(lines-2):
            if is_empty(board[l+1][0]):
                h-=1
            if is_empty(board[l+1][columns-1]):
                h-=1

        return h;

    def h1(self, node):
        """Needed for informed search"""
        return number_of_pegs(node.state.get_board())

    def h2(self, node):
        """Needed for informed search"""

        board = node.state.get_board()

        h = number_of_pegs(board)*100
        
        h-= len(board_moves(board))

        return h;

if __name__ == '__main__':

    n=0
    last_n=0
    print_every_n=500000

    sol_1 = solitaire([["_","O","O","O","_"],["O","_","O","_","O"],["_","O","_","O","_"],["O","_","O","_","_"],["_","O","_","_","_"]])
    sol_2 = solitaire([["O","O","O","X"],["O","O","O","O"],["O","_","O","O"],["O","O","O","O"]])
    sol_3 = solitaire([["O","O","O","X","X"],["O","O","O","O","O"],["O","_","O","_","O"],["O","O","O","O","O"]])
    sol_4 = solitaire([["O","O","O","X","X","X"],["O","_","O","O","O","O"],["O","O","O","O","O","O"],["O","O","O","O","O","O"]])

    for j in range(4):
        print("\n\n-----------------------NOVO TABULEIRO---------------------------------\n\n")
        if j==0:
            sol = sol_1
        if j==1:
            sol = sol_2
        if j==2:
            sol = sol_3
        if j==3:
            sol = sol_4

        for i in range(3):

            n=0
            last_n=0
            exp.exp=0

            start_time = time.time()

            print("--- %s seconds ---" % (time.time() - start_time))


            if i==0 and j!=3:
                print(depth_first_tree_search(sol).state.board)
            if i==1:
                print(greedy_search(sol).state.board)
            if i==2:
                print(astar_search(sol).state.board)

            print("--- %s seconds ---" % (time.time() - start_time))
            print("Gerados: "+ str(n))
            print("Expandidos: "+ str(exp.exp))


            