import random
pieceScore = {"b": 1, "r": 1}
END = 1000


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = END
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -END
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.GameOver:
                score = -turnMultiplier*END
            else:
                score = -turnMultiplier*scoreM(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove
        gs.undoMove()

    return bestMove


def scoreM(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'b':
                score += pieceScore[square[0]]
            elif square[0] == 'r':
                score -= pieceScore[square[0]]
    return score
