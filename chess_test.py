import chess
from itertools import compress
import time
import gui
import pygame as p
import random

PLY = 5
nodes_visited = 0
killers = [[0]*2 for i in range(PLY)]
history = [[0]*64 for i in range(64)]
file_to_num = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h':7}
mate_score = 100000


pawn_pos_eval_w = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                    5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
                    1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
                    0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
                    0.0,  0.0,  0.0,  2.0,  3.0,  0.0,  0.0,  0.0,
                    0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
                    0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5,
                    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]#e4 shud be 2
knight_pos_eval_w = [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
                        -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
                        -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
                        -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
                        -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
                        -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
                        -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
                        -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
                        ]
bishop_pos_eval_w = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                        -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
                        -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
                        -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
                        -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
                        -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
                        -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
                        ]
rook_pos_eval_w = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
                        0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
                        0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0
                        ]
queen_pos_eval_w = [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
                        -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                        -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
                        0.0,  0.0,  -0.5,  -0.5,  -0.5,  -0.5,  0.0, -0.5,
                        -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
                        -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
                        -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
                        ]#d4.e4,c4,f4 were 0.5 
king_pos_eval_w = [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
                        -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                        -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                        2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
                        2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0
                        ]
king_pos_eval_w_endgame = [-50,-40,-30,-20,-20,-30,-40,-50,
                            -30,-20,-10,  0,  0,-10,-20,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-10, 30, 40, 40, 30,-10,-30,
                            -30,-10, 30, 40, 40, 30,-10,-30,
                            -30,-10, 20, 30, 30, 20,-10,-30,
                            -30,-30,  0,  0,  0,  0,-30,-30,
                            -50,-30,-30,-30,-30,-30,-30,-50]

#king_pos_eval_b = [king_pos_eval_w[i] for i in range(63, -1, -1)]
pawn_pos_eval_b, knight_pos_eval_b, bishop_pos_eval_b, rook_pos_eval_b, queen_pos_eval_b, king_pos_eval_b, king_pos_eval_b_endgame = [], [], [], [], [], [], []

for i in range(8):
    pawn_pos_eval_b[8*i:8*i+8] = pawn_pos_eval_w[8*(7-i):8*(8-i)]
    knight_pos_eval_b[8*i:8*i+8] = knight_pos_eval_w[8*(7-i):8*(8-i)]
    bishop_pos_eval_b[8*i:8*i+8] = bishop_pos_eval_w[8*(7-i):8*(8-i)]
    rook_pos_eval_b[8*i:8*i+8] = rook_pos_eval_w[8*(7-i):8*(8-i)]
    queen_pos_eval_b[8*i:8*i+8] = queen_pos_eval_w[8*(7-i):8*(8-i)]
    king_pos_eval_b[8*i:8*i+8] = king_pos_eval_w[8*(7-i):8*(8-i)]
    king_pos_eval_b_endgame[8*i:8*i+8] = king_pos_eval_w_endgame[8*(7-i):8*(8-i)]

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

piece_worth = [10, 32, 33, 50, 90, 900] # hmmmm, used to be *10 but this worked better i think

#initializing the MVV LVA array
mvv_lva_scores = [[0]*6 for i in range(6)]

for i in range(6):
    for j in range(6):
        mvv_lva_scores[i][j] = (i+1)*100+6 - (j+1)

def eval_pos(board): 
    side_color = 0
    if (len(board.move_stack)%2 == 0):
        side_color = 1
   
    if side_color == 1 and not any(board.legal_moves):
        return -100000000000
    elif side_color == 0 and not any(board.legal_moves):
        return 100000000000

    score_w = 0
    score_b = 0
    #adding up pieces from white's and black's side
    for i in range(6):
        bitboard_w = board.pieces(i+1, 1).tolist() 
        bitboard_b = board.pieces(i+1, 0).tolist()
        #encouraging bishop pairs
        if i == 2:
            if sum(bitboard_w) == 2:
                score_w += 5
            if sum(bitboard_b) == 2:
                score_b += 5
        #summing up the positional advantage of the material
        score_w += sum(list(compress(eval_list_w[i], bitboard_w)))
        score_b += sum(list(compress(eval_list_b[i], bitboard_b)))
        #summing up the worth of the material
        score_w += sum(bitboard_w) * piece_worth[i]
        score_b += sum(bitboard_b) * piece_worth[i]
    return score_w-score_b

def rank_file_to_num(str_move):
    return file_to_num[str_move[0]]+(int(str_move[1]) - 1)*8

def sort_captures(board, moves):
    scores = [0]*len(moves)
    i = 0
    for move in moves:
        move_str = board.uci(move)
        attacker = board.piece_type_at(chess.SQUARE_NAMES.index(move_str[:2]))
        victim = board.piece_type_at(chess.SQUARE_NAMES.index(move_str[2:4]))
        #this is in the event of en passant where the target square has no piece
        if victim == None:
            scores[i] += 105
        else:
            scores[i] = mvv_lva_scores[victim-1][attacker-1]
        i += 1
    moves = [x for _, x in sorted(zip(scores, moves), key=lambda pair: pair[0], reverse=True)]

def sort_moves(board, moves, depth, side):
    moves_sorted = []

    #sorting captures first using MVV-LVA
    for i in moves:
        if board.is_capture(i):
            moves_sorted.append(i)
    for i in moves_sorted:
        moves.remove(i)
    sort_captures(board, moves_sorted)
    #sorting killer moves second
    i = 0    
    for j in range(len(moves)):
        if moves[j] in killers[depth]:
            moves[j], moves[i] = moves[i], moves[j]
            moves_sorted.append(moves[i])
            i += 1
    for j in range(i):
        moves.pop(0)
    #sorting history heuristic third
    scores = []
    for j in range(len(moves)):
        move_str = board.uci(moves[j])
        from_square = move_str[:2]
        to_square = move_str[2:4]
        scores.append(history[rank_file_to_num(from_square)][rank_file_to_num(to_square)])
    moves = [x for _, x in sorted(zip(scores, moves), key=lambda pair: pair[0], reverse=True)]
    
    moves_sorted.extend(moves)
    return moves_sorted

def quiescence(board, alpha, beta, player, depth): #player = 1 or -1, as oppose to side color which is = 0 or 1
    global nodes_visited 
    nodes_visited += 1
    stand_pat = player*eval_pos(board)
    if stand_pat >= beta:
        return beta
    if depth == 0:
        return stand_pat
    if alpha <= stand_pat:
        alpha = stand_pat
    moves = list(board.legal_moves)
    captures = []
    for i in moves:
        if board.is_capture(i):
            captures.append(i)

    for i in captures:
        board.push(i)
        score = -quiescence(board, -beta, -alpha, -player, depth-1)
        board.pop()
        if score >= beta:
            return score
        if score > alpha:
            alpha = score
    return alpha 
 
pvtable = {} # whenever a move beats alpha we add it here, noting by definition any move such that alpha<score<beta is a pv node
zobrist_keys = []

def fill_zobrist_keys():
    pass

def zobrist_hash(board):
    fill_zobrist_keys()

def storepvmove (board, move):
    index = zobrist_hash(board)
    pvtable[index] = move

def minimax(board, side_color, depth, alpha, beta):
    #must implement game over!!!
    if depth == 0:
        if side_color:
            return quiescence(board, alpha, beta, 1, 3)
        return -quiescence(board, -beta, -alpha, -1, 3)
        
    #Move ordering by simply moving all possible captures to the front
    moves = list(board.legal_moves)
    moves_sorted = sort_moves(board, moves, depth, 1-side_color)
        
    if side_color:
        max_eval = -10000000
        #for move in board.legal_moves: 
        for move in moves_sorted:
            board.push(move)
            curr_eval = minimax(board, 0, depth-1, alpha, beta)
            max_eval = max(max_eval, curr_eval)
            #print(move, curr_eval, max_eval)
            alpha = max(alpha, max_eval)
            #pop last move to allow for next move
            board.pop()
            if alpha >= beta:
                if not board.is_capture(move):
                    for i in range(len(killers[0])-1, 0, -1):
                        killers[depth][i] = killers[depth][i-1]
                    killers[depth][0] = move
                #print ("Movehuh:{}   Evalution:{}".format(move, curr_eval))
                return max_eval
        #print ("Movehuh1:{}   Evalution:{}".format(move, curr_eval))
        return max_eval
    else:
        min_eval = 10000000
        #for move in board.legal_moves:
        for move in moves_sorted:
            board.push(move)
            curr_eval = minimax(board, 1, depth-1, alpha, beta)
            #print ("{}  {}".format(curr_eval, move))
            min_eval = min(min_eval, curr_eval)
            beta = min(beta, min_eval)
            board.pop()
            if alpha >= beta:
                if not board.is_capture(move):
                    for i in range(len(killers[0])-1, 0, -1):
                        killers[depth][i] = killers[depth][i-1]
                    killers[depth][0] = move
                #print ("MOve:{}   Evalutionnnn:{}".format(move, curr_eval))
                return min_eval
        #print ("MOve:{}   Evalution:{}".format(move, curr_eval))
        return min_eval


def negamax(board, depth, alpha, beta, side_color):
    if depth == 0:
        return 2*(side_color-0.5)*eval_pos(board)
    
    moves = list(board.legal_moves)
    moves_sorted = sort_moves(board, moves, depth)

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
    global nodes_visited
    nodes_visited += 1
    if depth == 0:
        #return 2*(side_color-0.5)*eval_pos(board)
        return quiescence(board, alpha, beta, 2*(side_color-0.5), 2)
    
    moves = list(board.legal_moves)
    moves_sorted = sort_moves(board, moves, depth)

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
            #killer moves
            if not board.is_capture(move):
                for i in range(len(killers[0])-1, 0, -1):
                    killers[depth][i] = killers[depth][i-1]
                killers[depth][0] = move
            #history heuristic
            move_str = board.uci(move)
            from_square = move_str[:2]
            to_square = move_str[2:4]
            history[rank_file_to_num(from_square)][rank_file_to_num(to_square)] += 1
            return beta
        if (score > alpha):
            #killer moves
            if not board.is_capture(move):
                for i in range(len(killers[0])-1, 0, -1):
                    killers[depth][i] = killers[depth][i-1]
                killers[depth][0] = move
            #history heuristic
            move_str = board.uci(move)
            from_square = move_str[:2]
            to_square = move_str[2:4]
            history[rank_file_to_num(from_square)][rank_file_to_num(to_square)] += 1
            
            alpha = score
            bSearchPv = False
    return alpha

#def iterativedeepening(board, depth, alpha, beta, side_color):
def best_move_minimax(board, side_color, depth):
    best_score = 10000000
    best = None

    for move in board.legal_moves:
        board.push(move)
        #print (move)
        curr_score = minimax(board, 1-side_color, depth-1, -10000000, 10000000)
        print("Curr Score:{}    Best Score: {}  Move: {}".format(curr_score, best_score, move))
        if curr_score <= best_score:
            best_score = curr_score
            best = move
        board.pop()
    return best

def best_move(board, side_color, depth):
    best_score = -10000000    
    best = None

    for move in board.legal_moves:
        #print (move)
        board.push(move)
        curr_score = minimax(board, 1-side_color, depth-1, -10000000, 10000000)
        #curr_score = -negamax(board, depth-1, -10000000, 10000000, 1-side_color) # played around with miinmax and negamax a bit
        #curr_score = -pvSearch(board, depth-1, -10000000, 10000000, 1-side_color)
        print("Curr Score:{}    Best Score: {}  Move: {}".format(curr_score, best_score, move))
        if curr_score >= best_score:
            best_score = curr_score
            best = move
        board.pop()

    return best

'''def state (board):
    # this will identify whether we are in the opening, middlegame, or endgame'''

if __name__ == "__main__":
    '''
    p.init()
    screen = p.display.set_mode((gui.WIDTH, gui.HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gui.loadImages() #do once only
    running = True

    board = chess.Board()
    gui.drawGameState(screen, board)
    p.display.flip()
    sqSelected = () #tuple
    playerClicks = [] #keep track of player clicks

    while running:
        while (len(playerClicks) < 2 and running):
            for e in p.event.get():
                if e.type == p.QUIT: 
                    running = False
                    break
                elif e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos() #(x,y)
                    col = location[0]//gui.SQ_SIZE
                    row = location[1]//gui.SQ_SIZE
                    if sqSelected == (row, col): #click same square twice
                        sqSelected = () # unselect
                        playerClicks = [] # clear plyer clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
        if (gui.getmovefromclick(playerClicks, board) == "Illegal"):
            sqSelected = () 
            playerClicks = [] 
            continue                
        board.push(chess.Move.from_uci(gui.getmovefromclick(playerClicks, board)))
        sqSelected = ()
        playerClicks = []
        #print(board)
        gui.drawGameState(screen, board)
        p.display.flip()
        nodes_visited = 0
        print("Opponent move:")
        start = time.time()
        board.push(best_move_minimax(board, 0, 4))
        end = time.time()
        gui.drawGameState(screen, board)
        p.display.flip()
        print("ELAPSED TIME: ", end-start)
        print("NODES VISITED: ", nodes_visited)
        print(board)
    '''
    num1 = random.getrandbits(64)
    num2 = random.getrandbits(64)
    num3 = random.getrandbits(64)
    print(num1)
    print(num2)
    print(num1 ^ num2)
    print(num1 ^ num2 ^ num3)
