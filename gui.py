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
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # we can now access images by doing, say, IMAGES['wp']

def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [p.Colors("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    pass

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
                running = True
        drawGameState(screen, chess.board())
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()

