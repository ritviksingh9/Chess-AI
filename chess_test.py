import chess
from itertools import compress

pawn_pos_eval_w = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                    5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
                    1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
                    0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
                    0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,
                    0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
                    0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5,
                    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
pawn_pos_eval_b = [pawn_pos_eval_w[i] for i in range(63, -1, -1)]
knight_pos_eval_w = [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                        -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
                        -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
                        -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
                        -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
                        -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
                        -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
                        -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
                        ]
knight_pos_eval_b = [knight_pos_eval_w[i] for i in range(63, -1, -1)]
bishop_pos_eval_w = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                        -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
                        -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
                        -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
                        -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
                        -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
                        -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
                        ]
bishop_pos_eval_b = [bishop_pos_eval_w[i] for i in range(63, -1, -1)]
rook_pos_eval_w = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                        0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0
                        ]
rook_pos_eval_b = [rook_pos_eval_w[i] for i in range(63, -1, -1)]
queen_pos_eval_w = [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                        -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                        -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                        0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                        -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
                        ]
queen_pos_eval_b = [queen_pos_eval_w[i] for i in range(63, -1, -1)]
king_pos_eval_w = [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                        -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                        2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
                        2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0
                        ]
king_pos_eval_b = [king_pos_eval_w[i] for i in range(63, -1, -1)]

eval_list_w = [pawn_pos_eval_w, knight_pos_eval_w, bishop_pos_eval_w, rook_pos_eval_w, queen_pos_eval_w, king_pos_eval_w]
eval_list_b = [pawn_pos_eval_b, knight_pos_eval_b, bishop_pos_eval_b, rook_pos_eval_b, queen_pos_eval_b, king_pos_eval_b]
piece_worth = [10, 30, 30, 50, 90, 900]

def eval_pos(board, side_color):
    score = 0
    for i in range(6):
        bitboard = board.pieces(i+1, side_color).tolist()
        bitboard.reverse()
        #summing up the positional advantage of the material
        if side_color:
            score += sum(list(compress(eval_list_w[i], bitboard)))
        else:
            score += sum(list(compress(eval_list_b[i], bitboard)))
        #summing up the worth of the material
        score += sum(bitboard) * piece_worth[i]

    if not side_color:
        return -1*score
    return score

def minimax(board, side_color, depth, alpha, beta):
    #must implement game over!!!
    if depth == 0:
        return eval_pos(board, side_color)
    
    if side_color:
        max_eval = -10000000
        for move in board.legal_moves:
            board.push(move)
            curr_eval = minimax(board, 0, depth-1, alpha, beta)
            max_eval = max(max_eval, curr_eval)
            alpha = max(alpha, curr_eval)
            #pop last move to allow for next move
            board.pop()
            if alpha >= beta:
                return max_eval
        return max_eval
    else:
        min_eval = 10000000
        for move in board.legal_moves:
            board.push(move)
            curr_eval = minimax(board, 1, depth-1, alpha, beta)
            min_eval = min(min_eval, curr_eval)
            beta = min(beta, curr_eval)
            board.pop()
            if alpha >= beta:
                return min_eval
        return min_eval

def best_move(board, side_color, depth):
    best_score = -10000000
    best = None

    for move in board.legal_moves:
        board.push(move)
        curr_score = minimax(board, side_color, depth-1, -10000000, 10000000)
        print("Curr Score:{}    Best Score: {}  Move: {}".format(curr_score, best_score, move))
        if abs(curr_score) > best_score:
            best_score = abs(curr_score)
            best = move
        board.pop()

    return best

board = chess.Board()
while 1 == 1:
    print("Your move:")
    x = input()
    board.push(chess.Move.from_uci(""+x))
    print(board)
    print("Opponent move:")
    board.push(best_move(board, 0, 3))
    print(board)

print(board)
print(board.legal_moves)
board.push_san("e4")
print(board)
print(board.pieces(1, 1))
a = board.pieces(1, 0).tolist()
a.reverse()
a = board.legal_moves
for move in a:
    print(type(move))
    break
board.push(move)
print(board)