"""
Tic Tac Toe Player
"""
import copy
import math
import time

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #Find a count of all X's and O's
    xmoves = board[0].count(X) + board[1].count(X) + board[2].count(X)
    omoves = board[0].count(O) + board[1].count(O) + board[2].count(O)

    #Compare the counts, if they are equal, give the move to X, as X always goes first.
    return O if xmoves > omoves else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    output = []

    #Append the index of any EMPTY square to the output list.
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                output.append([i, j])
    
    return output


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Create deepcopy. We want a copy of board that is not connected to board in anyway.
    cBoard = copy.deepcopy(board)

    #Verify the action can be made and apply the action.
    if (cBoard[action[0]][action[1]] != EMPTY):
        raise TypeError
    else:
        cBoard[action[0]][action[1]] = player(board)

    return cBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check rows and cols for a potential win.
    for i in range(len(board)):
        if(board[i][0] == board[i][1] == board[i][2]):
            return board[i][0]
        
        if(board[0][i] == board[1][i] == board[2][i]):
            return board[0][i]

    #Check diagonals for a potential win.
    if(board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]

    if(board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #If no actions can be made or a winner exists, return the board as terminal.
    return True if (len(actions(board)) == 0) | (winner(board) != None) else False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1

    elif winner(board) == O:
        return -1
        
    else: 
        return 0


def minmaxValues(board, alpha, beta, player):
    #If the board is terminal, grade and return.
    if terminal(board):
        return utility(board)
    
    #If the player is X, look to increase the value.
    if player == X:
        value = -math.inf

        for action in actions(board):
            #For each action possible, gather the largest value possible, factoring in the other players moves.
            value = max(value, minmaxValues(result(board, action), alpha, beta, O))

            #Update alpha on the best move's value.
            alpha = max(alpha, value)

            #If alpha beats all other options, than do not consider the rest of the options.
            if alpha >= beta:
                break

        return value

    #If the player is O, look to decrease the value.
    else:
        value = math.inf

        for action in actions(board):
            #For each action possible, gather the smallest value possible, considering the other players moves.
            value = min(value, minmaxValues(result(board, action), alpha, beta, X))

            #Update beta on the best move's value.
            beta = min(beta, value)

            #If alpha beats all other options, than do not consider the rest of the options.
            if alpha >= beta:
                break
        
        return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    startTime = time.time()

    #Check if a move can even be made.
    if terminal(board):
        return None

    move = None

    #Initialize the boundaries.
    alpha = -math.inf
    beta = math.inf

    #If the player is X, look to maximize 'value'.
    if player(board) == X:
        value = -math.inf

        for action in actions(board):
            #Gather a value for each action possible.
            new_value = minmaxValues(result(board, action), alpha, beta, O)

            #Update the alpha condition with the value of the best move.
            alpha = max(value, new_value)

            #If a better move is found, store it and it's value.
            if new_value > value:
                value = new_value
                move = action

    #Same as above, just altered to minimize 'value'
    else:
        value = math.inf

        for action in actions(board):
            new_value = minmaxValues(result(board, action), alpha, beta, X)

            beta = min(value, new_value)

            if new_value < value:
                value = new_value
                move = action
    
    print("The algorithmn took:", time.time() - startTime)
    return move