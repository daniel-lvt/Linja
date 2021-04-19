import pygame as p
import LinjaEngine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = WIDTH//DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ['b', 'r']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "images/"+piece+".png"), (60, 60))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("blue"))
    gs = LinjaEngine.GameState()
    p.display.set_caption("Linja - Inteligencia Computacional")

    #########

    validMoves=gs.getValidMoves()
    moveMade=False

    ###########
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    background=p.image.load("images/background.png").convert()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # x,y lugar
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):  
                    sqSelected = ()  
                    playerClicks = []  
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: 
                    move = LinjaEngine.Move(
                        playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade=True
                    sqSelected = ()  
                    playerClicks = []  
            elif e.type == p.KEYDOWN:
                if e.key == p.K_x:
                    gs.undoMove()
                    moveMade=True
        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False
        screen.blit(background,[0,0])
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)  
    drawPieces(screen, gs.board)  


def drawBoard(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, p.Color("white"), p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE),1,5)


def drawPieces(screen, board):
    
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
if __name__ == "__main__":
    main()
