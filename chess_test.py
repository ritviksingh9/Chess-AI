import chess
from itertools import compress
import time

MOVE_ORDER_COUNT = 6
PLY = 4
nodes_visited = 0
killers = [[0]*3 for i in range(PLY)]
piece_character_to_num = ["P", "N", "B", "R", "Q", "K"]

mate_score = 1000
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

eval_list_w_temp = [pawn_pos_eval_w, knight_pos_eval_w, bishop_pos_eval_w, rook_pos_eval_w, queen_pos_eval_w, king_pos_eval_w]
eval_list_b_temp = [pawn_pos_eval_b, knight_pos_eval_b, bishop_pos_eval_b, rook_pos_eval_b, queen_pos_eval_b, king_pos_eval_b]

#Reflecting the boards to account for how the bitboard is displayed
eval_list_w = []
eval_list_b = []
for i in range(6):
    board_w = eval_list_w_temp[i]
    board_b = eval_list_b_temp[i]
    w = []
    b = []
    for a in range(7, -1, -1):
        w.extend(board_w[8*a:8*a+8])
        b.extend(board_b[8*a:8*a+8])
    eval_list_w.append(w)
    eval_list_b.append(b)

piece_worth = [10, 32, 33, 50, 90, 900]

#initializing the MVV LVA array
mvv_lva_scores = [[0]*6 for i in range(6)]

for i in range(6):
    for j in range(6):
        mvv_lva_scores[i][j] = (i+1)*100+6 - (j+1)

def eval_pos(board):
    score_w = 0
    score_b = 0
    #adding up pieces from white's and black's side
    for i in range(6):
        bitboard_w = board.pieces(i+1, 1).tolist()
        bitboard_b = board.pieces(i+1, 0).tolist()
        #summing up the positional advantage of the material
        score_w += sum(list(compress(eval_list_w[i], bitboard_w)))
        score_b += sum(list(compress(eval_list_b[i], bitboard_b)))
        #summing up the worth of the material
        score_w += sum(bitboard_w) * piece_worth[i]
        score_b += sum(bitboard_b) * piece_worth[i]

    return score_w-score_b

def sort_captures(board, moves):
    scores = [0]*len(moves)
    i = 0
    for move in moves:
        move_str = board.uci(move)
        attacker = board.piece_type_at(chess.SQUARE_NAMES.index(move_str[:2]))
        victim = board.piece_type_at(chess.SQUARE_NAMES.index(move_str[2:4]))
        #this is in the event of en passant where the target square has no piece
        print(attacker)
        print(victim)
        if victim == None:
            scores[i] += 105
        else:
            scores[i] = mvv_lva_scores[victim-1][attacker-1]
        i += 1

def eval_pos(board): #POV of white
    score_w = 0
    score_b = 0
    #adding up pieces from white's and black's side
    for i in range(6):
        bitboard_w = board.pieces(i+1, 1).tolist()
        bitboard_b = board.pieces(i+1, 0).tolist()
        #summing up the positional advantage of the material
        score_w += sum(list(compress(eval_list_w[i], bitboard_w)))
        score_b += sum(list(compress(eval_list_b[i], bitboard_b)))
        #summing up the worth of the material
        score_w += sum(bitboard_w) * piece_worth[i]
        score_b += sum(bitboard_b) * piece_worth[i]
    return score_w-score_b

def quiescence(board, alpha, beta, player): #player = 1 or -1, as oppose to side color which is = 0 or 1
    stand_pat = player*eval_pos(board)
    if stand_pat >= beta:
        return beta
    if alpha <= stand_pat:
        alpha = stand_pat
    moves = list(board.legal_moves)
    captures = []
    for i in moves:
        if board.is_capture(i):
            captures.append(i)
    for i in captures:
        board.push(i)
        score = -quiescence(board, -beta, -alpha, -player)
        board.pop()
        if score >= beta:
            return score
        if score > alpha:
            alpha = score
    return alpha
 
def minimax(board, side_color, depth, alpha, beta):
    #must implement game over!!!
    if depth == 0:
        return quiescence(board, alpha, beta, -1)
    
#Move ordering by simply moving all possible captures to the front
    moves = list(board.legal_moves)
    moves_sorted = []
    
    for i in moves:
        if board.is_capture(i):
            moves_sorted.append(i)
    for i in moves_sorted:
        moves.remove(i)
    sort_captures(board, moves_sorted)

    scores = [0]*len(moves_sorted)
    for i in range(len(moves_sorted)):
        board.push(moves_sorted[i])
        scores[i] = eval_pos(board)
        board.pop()
    moves_sorted_temp = [x for _, x in sorted(zip(scores, moves_sorted), key=lambda pair: pair[0], reverse=True)]
    moves_sorted = moves_sorted_temp
    i = 0
    
    for j in range(len(moves)):
        if moves[j] in killers[depth]:
            moves[j], moves[i] = moves[i], moves[j]
            i += 1
    moves_sorted.extend(moves)
    
    if side_color:
        max_eval = -10000000
        #for move in board.legal_moves:
        for move in moves_sorted:
            board.push(move)
            curr_eval = minimax(board, 0, depth-1, alpha, beta)
            max_eval = max(max_eval, curr_eval)
            alpha = max(alpha, max_eval)
            #pop last move to allow for next move
            board.pop()
            if alpha >= beta:
                if not board.is_capture(move):
                    for i in range(len(killers[0])-1, 0, -1):
                        killers[depth][i] = killers[depth][i-1]
                    killers[depth][0] = move
                return max_eval
        return max_eval
    else:
        min_eval = 10000000
        #for move in board.legal_moves:
        for move in moves_sorted:
            board.push(move)
            curr_eval = minimax(board, 1, depth-1, alpha, beta)
            min_eval = min(min_eval, curr_eval)
            beta = min(beta, min_eval)
            board.pop()
            if alpha >= beta:
                if not board.is_capture(move):
                    for i in range(len(killers[0])-1, 0, -1):
                        killers[depth][i] = killers[depth][i-1]
                    killers[depth][0] = move
                return min_eval
        return min_eval

def negamax(board, depth, alpha, beta, side_color):
    if depth == 0:
        return 2*(side_color-0.5)*eval_pos(board)
    
    moves = list(board.legal_moves)
    moves_sorted = []
    for i in moves:
        if board.is_capture(i):
            moves_sorted.append(i)
    for i in moves_sorted:
        moves.remove(i)
    moves_sorted.extend(moves)

    max_eval = -10000000
    for move in moves_sorted:
        board.push(move)
        curr_eval = -negamax(board, depth-1, -beta, -alpha, 1-side_color)
        max_eval = max(max_eval, curr_eval)
        alpha = max(alpha, max_eval)
        board.pop()
        if alpha >= beta:
            return max_eval
    return max_eval

def pvSearch (board, depth, alpha, beta, side_color):
    if depth == 0:
        return 2*(side_color-0.5)*eval_pos(board)
        #return quiescence(board, alpha, beta, 2*(side_color-0.5))
    
    moves = list(board.legal_moves)
    moves_sorted = []
    for i in moves:
        if board.is_capture(i):
            moves_sorted.append(i)
    for i in moves_sorted:
        moves.remove(i)
    moves_sorted.extend(moves)

    bSearchPv = True
    for move in moves_sorted:
        board.push(move)
        if (bSearchPv):
            score = -pvSearch(board, depth-1, -beta, -alpha, 1-side_color)
        else:
            score = -pvSearch(board, depth-1, -alpha-1, -alpha, 1-side_color)
            if (score > alpha):
                score = -pvSearch(board, depth-1, -beta, -alpha, 1-side_color)
        board.pop()
        if (score >= beta):
            return beta
        if (score > alpha):
            alpha = score
            bSearchPv = False
    return alpha

def best_move(board, side_color, depth):
    best_score = -10000000
    # the next portion is commented out in negamax implementation
    '''
    if side_color:
        best_score *= -1
    '''
    best = None

    for move in board.legal_moves:
        board.push(move)
        #curr_score = minimax(board, side_color, depth-1, -10000000, 10000000)
        #curr_score = -negamax(board, depth-1, -10000000, 10000000, 1-side_color) # played around with miinmax and negamax a bit
        curr_score = -pvSearch(board, depth-1, -10000000, 10000000, 1-side_color)
        print("Curr Score:{}    Best Score: {}  Move: {}".format(curr_score, best_score, move))
        if curr_score >= best_score:
            best_score = curr_score
            best = move
        board.pop()

    return best

if __name__ == "__main__":
    board = chess.Board()
    
    while 1 == 1:
        print("Your move:")
        x = input()
        board.push(chess.Move.from_uci(x))
        print(board)
        print("Opponent move:")
        start = time.time()
        board.push(best_move(board, 0, 5))
        end = time.time()
        print("ELAPSED TIME: ", end-start)
        print(board)
    '''
    a = list(board.legal_moves)
    print(a)
    print(board)
    board.push(a[0])
    print(board)
    '''