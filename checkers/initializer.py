'''
CS 51
Tic Tac Toe Program
by Vincent Chow, Stephen Albro, Peter Hickman, & Brandon Price
'''
'''
Initializer.py contains our most elementary functionality related to te tic-tac-toe board.
It is responsible for things like making a new boards and games, evaluating wins, ties, and
valid moves, and getting the opponent and the next state given an action.
The file does not require excessive commenting.
'''
from random import randint
from copy import deepcopy

#-----------------------------------------------------------------------------
"""
Returns an empty board
"""

def new():
    return [['wm','_','wm','_','wm','_','wm','_'],\
            ['_','wm','_','wm','_','wm','_','wm'],\
            ['wm','_','wm','_','wm','_','wm','_'],\
            ['_','_','_','_','_','_','_','_'],\
            ['_','_','_','_','_','_','_','_'],\
            ['_','rm','_','rm','_','rm','_','rm'],\
            ['rm','_','rm','_','rm','_','rm','_'],\
            ['_','rm','_','rm','_','rm','_','rm']]


#-----------------------------------------------------------------------------
"""
Takes in the current player and returns the next player
"""

def opponent (player):
    if (player == 'r'):
        return 'w'
    else:
        return 'r'


#-----------------------------------------------------------------------------
"""
Takes in a state and an action and returns the next state
"""

def next_state(state,action):
    board = deepcopy(state['board'])
    statr = deepcopy(state['statr'])
    statw = deepcopy(state['statw'])
    init_i = action['init_pos'][0]
    init_j = action['init_pos'][1]
    final_i = action['final_pos'][0]
    final_j = action['final_pos'][1]
    change_i = final_i - init_i
    change_j = final_j - init_j
    player_type = board[init_i][init_j]
    
    # if its a jump, remove the piece
    if (abs(change_i) == 2 and abs(change_j) == 2):
        opponent_type = board[init_i+change_i/2][init_j+change_j/2]
        type_only = opponent_type[1]
        opponent_player = opponent_type[0]
        board[init_i+change_i/2][init_j+change_j/2] = '_'
        if (type_only == 'm'):
            if (opponent_player == 'r'):
                statr['men_num'] -= 1
            else:
                statw['men_num'] -= 1
        else:
            if (opponent_player == 'r'):
                statr['king_num'] -= 1
            else:
                statw['king_num'] -= 1
                
    # somebody is being kinged
    if (final_i == 0 and player_type == 'rm'):
        statr['men_num'] -= 1
        statr['king_num'] += 1
        board[final_i][final_j] = 'rk'
    elif (final_i == 7 and player_type == 'wm'):
        statw['men_num'] -= 1
        statw['king_num'] += 1
        board[final_i][final_j] = 'wk'
    else:
        board[final_i][final_j] = player_type
    enemy = opponent(state['player'])
    
    # add the blank space
    board[init_i][init_j] = '_'
    nextState = {'player':enemy, 'board':board, 'statr':statr, 'statw':statw}
    return nextState
    
#-----------------------------------------------------------------------------
"""
Checks if either player has won; if not, continue
"""
def eval (state):
    actions = allPosMoves(state['board'],state['player'])
    
    # if no available moves for current player, opponent wins
    if (actions == []):
        return (opponent(state['player']) + '_wins')
    else:
        return 'continue'


#-----------------------------------------------------------------------------
"""
valid takes in a board and action and checks if it is a valid action
"""
def valid (board,action):
    init_i = action['init_pos'][0]
    init_j = action['init_pos'][1]
    final_i = action['final_pos'][0]
    final_j = action['final_pos'][1]
    change_i = final_i - init_i
    change_j = final_j - init_j
    player_type = board[init_i][init_j]
    player = player_type[0]
    opponent_player = opponent(player)
    
    # check if the action is an open space
    space_is_open = (board[final_i][final_j] == '_')
    
    #check if it is the correct pos for a jump
    if (abs(change_i) == 2 and abs(change_j) == 2):
        correct_pos = (board[init_i + change_i/2][init_j + change_j/2] \
                       == (opponent_player + 'm') or \
                       board[init_i + change_i/2][init_j + change_j/2] \
                       == (opponent_player + 'k'))
        
    #checks if it is the correct pos for a non-jump
    else:
        correct_pos =  (abs(change_i) == 1 and abs(change_j) == 1)
    
    # is it up for red-men
    if (player_type == 'rm'):
        correct_direction = (change_i < 0)
        
    # is it down for white-mean
    elif (player_type == 'wm'):
        correct_direction = (change_i > 0)
        
    # direction doesn't matter for kings
    else:
        correct_direction = True
        
    # return all three variables
    return (space_is_open and correct_pos and correct_direction)
    

#-----------------------------------------------------------------------------
"""
pos_actions takes in a board and the current_pos and 
returns a list of all the possible actions
"""
def pos_actions (board, current_pos):
    curr_i = current_pos[0]
    curr_j = current_pos[1]        
    player_type = board[curr_i][curr_j]
    
    if (player_type == '_'):
        return 'no pieces in this position'
    
    player = player_type[0]
    opponent_player = opponent(player)
    
    open_spaces = []
    enemy_spaces = []
    
    # check spaces surrounding the current_pos
    if (curr_i == 7):
        check_i = [-1]
    elif (curr_i == 0):
        check_i = [1]
    else:
        check_i = [-1,1]
        
    if (curr_j == 7):
        check_j = [-1]
    elif (curr_j == 0):
        check_j = [1]
    else:
        check_j = [-1,1]
        
    for i in check_i:
        for j in check_j:
            spotcheck = board[curr_i+i][curr_j+j]
            if (spotcheck == '_'):
                open_spaces.append({'init_pos':current_pos,
                                    'final_pos':(curr_i+i,curr_j+j)})
            elif (spotcheck == opponent_player + 'm' or 
                  spotcheck == opponent_player + 'k'):
                enemy_spaces.append((curr_i+i,curr_j+j))
    
    # check spaces on the other side of the enemies
    for enemy in enemy_spaces:
        enemy_i = enemy[0]
        enemy_j = enemy[1]
        change_i = enemy_i - curr_i
        change_j = enemy_j - curr_j
        next_i = enemy_i + change_i
        next_j = enemy_j + change_j
        if (0 <= next_i <= 7 and 0 <= next_j <= 7):
            if (board[next_i][next_j] == '_'):
                open_spaces.append({'init_pos':current_pos,
                                    'final_pos':(next_i,next_j)})                        
      
    possible_actions = [act for act in open_spaces if valid(board,act)]
    return possible_actions
    

#-----------------------------------------------------------------------------
"""
pos_actions_left return true if there are actions left for that player
"""
def pos_actions_left (board,player):
    pos_act = []
    for i in range(8):
        for j in range(8):
            if (board[i][j] == player+'m' or board[i][j] == player+'k'):
                for act in pos_actions(board,(i,j)):
                    pos_act.append(act)
    return (pos_act != [])

#-----------------------------------------------------------------------------
"""
random_player returns a random player
"""
def random_player ():
    if (randint(0,1) == 0):
        return 'w'
    else:
        return 'r'
   
#-----------------------------------------------------------------------------     
"""
new_state returns an empty board and new stats for each player
"""
def new_state ():
    b = new()
    p = random_player()
    return {'player':p,'board':b,\
    'statr':{'player':'r','men_num':2,'king_num':5},
            'statw':{'player':'w','men_num':5,'king_num':3}}

#-----------------------------------------------------------------------------     
"""
allPosMoves takes in a board and player and returns all of the possible moves
of that player in a list
"""
def allPosMoves(board,player):
    pos_act = []
    for i in range(8):
        for j in range(8):
            if (board[i][j] == player+'m' or board[i][j] == player+'k'):
                for act in pos_actions(board,(i,j)):
                    pos_act.append(act)
    return pos_act