import pygame as p
import LinjaEngine
import MoveFinder
import sys

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

def mainGame(pyOne,pyTwo):
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("blue"))
    gs = LinjaEngine.GameState()
    p.display.set_caption('Linja - Computational Intelligence')

    #########

    validMoves = gs.getValidMoves()
    moveMade = False

    ###########
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver=False
    playerOne=pyOne
    playerTwo=pyTwo
    background = p.image.load("images/background.png").convert()
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                sys.exit(1)
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                            moveMade = True
                        sqSelected = ()
                        playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_x:
                    gs.undoMove()
                    moveMade = True  
        #IA
        if not gameOver and not humanTurn:
            IAMove=MoveFinder.findRandomMove(validMoves)
            gs.makeMove(IAMove)
            moveMade=True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        screen.blit(background, [0, 0])
        drawGameState(screen, gs,validMoves,sqSelected)

        if gs.GameOver:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,"Reds win the game")
            else:
                drawText(screen,"Blacks win the game")
    
        clock.tick(MAX_FPS)
        p.display.flip()


def stateGame(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('r' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(50)  
            s.fill(p.Color('red'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*SQ_SIZE,move.endRow*SQ_SIZE))


def drawGameState(screen, gs,validMoves, sqSelected):
    drawBoard(screen)
    stateGame(screen,gs,validMoves, sqSelected)
    drawPieces(screen, gs.board)


def drawBoard(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, p.Color("white"), p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE), 1, 5)


def drawPieces(screen, board):

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textObject=font.render(text,0,p.Color('Gray'))
    textLocation= p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-textObject.get_width()/2,HEIGHT/2-textObject.get_height()/2)
    screen.blit(textObject,textLocation)
    textObject=font.render(text,0,p.Color("Black")) 
    screen.blit(textObject,textLocation.move(2,2))


