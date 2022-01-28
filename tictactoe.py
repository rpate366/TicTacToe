"""
Tic Tac Toe Player
"""
import copy
import math

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
    xmoves = board[0].count(X) + board[1].count(X) + board[2].count(X)
    omoves = board[0].count(O) + board[1].count(O) + board[2].count(O)

    return O if xmoves > omoves else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    output = []

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                output.append([i, j])
    
    return output


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    cBoard = copy.deepcopy(board)
    if (cBoard[action[0]][action[1]] != EMPTY):
        raise TypeError
    else:
        cBoard[action[0]][action[1]] = player(board)

    return cBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if(board[i][0] == board[i][1] == board[i][2]):
            return board[i][0]
        
        if(board[0][i] == board[1][i] == board[2][i]):
            return board[0][i]

    if(board[0][0] == board[1][1] == board[2][2]):
        return board[0][0]

    if(board[0][2] == board[1][1] == board[2][0]):
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
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
    if terminal(board):
        return utility(board)
    
    if player == X:
        value = -math.inf

        for action in actions(board):
            value = max(value, minmaxValues(result(board, action), alpha, beta, O))

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    else:
        value = math.inf

        for action in actions(board):
            value = min(value, minmaxValues(result(board, action), alpha, beta, X))

            beta = min(beta, value)

            if alpha >= beta:
                break
        
        return value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    move = None

    alpha = -math.inf
    beta = math.inf

    if player(board) == X:
        value = -math.inf

        for action in actions(board):
            new_value = minmaxValues(result(board, action), alpha, beta, O)

            alpha = max(value, new_value)

            if new_value > value:
                value = new_value
                move = action

    else:
        value = math.inf

        for action in actions(board):
            new_value = minmaxValues(result(board, action), alpha, beta, X)

            beta = min(value, new_value)

            if new_value < value:
                value = new_value
                move = action
    
    return move