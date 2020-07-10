import pygame as p
import chess

WIDTH = HEIGHT = 512
DIMENSION = 8 #8 by 8
SQ_SIZE = HEIGHT // 8
MAX_FPS = 15
IMAGES = {}
rowtorank = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
coltofile = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

'''
Initialize a global dictionary of images. Called once
'''

def loadImages():
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("/home/dsl7/Documents/Summer/Side Projects/Chess-AI/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # we can now access images by doing, say, IMAGES['wp']

def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board.piece_at(chess.square(c, 7-r))
            if piece is not None:
                screen.blit(IMAGES[piece.symbol()], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getmovefromclick(playerclick):
    startrow = playerclick[0][0]
    startcol = playerclick[0][1]
    endrow = playerclick[1][0]
    endcol = playerclick[1][1]
    return coltofile[startcol] + rowtorank[startrow] + coltofile[endcol] + rowtorank[endrow]

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    loadImages() #do once only
    running = True
    sqSelected = () #tuple
    playerClick = [] #keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y)
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #click same square twice
                    sqSelected = () # unselect
                    playerClicks = [] # clear plyer clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if (len(playerClicks) == 2): #after 2nd click
                    #make move
                    sqSelected = ()
                    playerClick = []
        drawGameState(screen, chess.Board())
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()

