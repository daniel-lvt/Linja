import random
#pieceScore = {"b": 1, "r": 1}
pieceScoreB = {'0':1,'1':2,'2':4,'3':8,'4':16,'5':32,'6':64,'7':128}
pieceScoreR = {'0':128,'1':64,'2':32,'3':16,'4':8,'5':4,'6':2,'7':1}
END = 1000
a=0
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove (gs,validMoves):
    global a
    state=False
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore=-END*turnMultiplier
    bestMove=None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        moves=gs.getValidMoves()
        playerMax=END
        for game in moves:
            gs.makeMove(game)
            if gs.GameOver:
                score = END*turnMultiplier
            else: 
                score = turnMultiplier*scoreM(gs.board)
            if score>playerMax:
                playerMax=score
            gs.undoMove()
        if playerMax<maxScore:
            maxScore=playerMax
            bestMove=playerMove
        gs.undoMove()

    if a>0:
        #print(a)
        if not gs.whiteToMove and not state:
            state=True    
        gs.whiteToMove=not gs.whiteToMove
        a=0
    a+=1
    return bestMove
#def findBestMove(gs, validMoves):
    #turnMultiplier = 1 if gs.whiteToMove else -1
    #opponentMinMaxScore = END
    #bestMove = None
    #random.shuffle(validMoves)
    #for playerMove in validMoves:
        #gs.makeMove(playerMove)
        #opponentsMoves = gs.getValidMoves()
        #opponentMaxScore = -END
        #for opponentsMove in opponentsMoves:
            #gs.makeMove(opponentsMove)
            #if gs.GameOver:
            #    score = -turnMultiplier*END
            #else:
            #    score = -turnMultiplier*scoreM(gs.board)
           # if score > opponentMaxScore:
          #      opponentMaxScore = score
         #   gs.undoMove()
        #if opponentMaxScore < opponentMinMaxScore:
          #  opponentMinMaxScore = opponentMaxScore
         #   bestMove = playerMove
        #gs.undoMove()

#    return bestMove


def scoreM(board):
    #print(board)
    score = 0
    #print(board[1][0])
    #print('entra')

    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c]=='b':
                for i in pieceScoreR:
                    if i==str(c):
                        score+=pieceScoreR[i]
            elif board[r][c]=='r':
                for i in pieceScoreB:
                    if i==str(c):
                        score-=pieceScoreB[i]
                        
    return score
    #for row in board:
    #    for square in row:

    #        if square[0] == 'b':
    #            print('-b-')
    #            score += pieceScore[square[0]]
    #            print('--')
    #        elif square[0] == 'r':
    #            print('-r-')
    #            print(pieceScore[square[0]])
    #            print(pieceScore)
    #            print(square)
    #            print('-*-')
    #            print(pieceScoreR)
    #            print(pieceScoreR['0'])
    #            print('-*-')
    #            score -= pieceScore[square[0]]
    #            print('--')
    #print('sale')
    #print(score)
    #print('wwwwwwww')
    #print(score)
    return score
