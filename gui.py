import pygame as p
import chess

WIDTH = HEIGHT = 512
DIMENSION = 8 #8 by 8
SQ_SIZE = HEIGHT // 8
MAX_FPS = 15
IMAGES = {}

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

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    loadImages() #do once only
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, chess.Board())
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()

