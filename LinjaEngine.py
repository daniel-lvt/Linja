import LinjaBoard

class GameState():
    def __init__(self):
        self.board = LinjaBoard.board_m1r
        self.whiteToMove = True
        self.moveLog = []
        self.stackB = 0
        self.stackR = 0
        self.turnB = True
        self.turnR = True
        self.stackColum = []


    #recibe el movimiento de inicio y final de columna 
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  

        if self.stackR==1 or self.stackB==1:
            print('-------------cambio estado -------------------------------------')
            if (len(self.stackColum)>1):
                self.stackColum.pop(0)

        if((self.stackB == 1) or (self.stackR == 1)):
            self.whiteToMove = not self.whiteToMove
            self.stackB = 0
            self.stackR = 0
        elif (self.whiteToMove):
            if (len(self.stackColum)>0):
                self.stackColum.clear()
            self.stackB += 1
            self.stackColum.append(([move.endRow], [move.endCol]))
        else:
            if (len(self.stackColum)>0):
                self.stackColum.clear()
            self.stackR += 1
            self.stackColum.append(([move.endRow], [move.endCol]))

    # deshase el movimiento 
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    # retorna todos los movimientos validos
    def getValidMoves(self):
        return self.getAllPossibleMoves()

    # retorna todos los posibles movimientos
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'r' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    self.getMoves(r, c, moves, turn)
        #valida el turno del movimiento 
        if self.turnB:
            self.turnB = False
        elif not self.whiteToMove:
            if not self.turnB:
                self.turnR = False
        return moves


    # definicion de turno
    # ---- cudrar movimiento extra solo valido para segundo movimiento 
    def getMoves(self, r, c, moves, turn):

        if self.turnB:
            print('primer movimiento P1')
            self.turn(r, c, moves)
        elif not self.turnB and self.whiteToMove:
            print('segundo movimiento P1')
            self.turn(r, c, moves)
        elif self.turnR and not self.turnB:
            print('primer movimiento P2')
            self.turn(r, c, moves)
        else:
            print('segundo movimiento P2')
            self.turn(r, c, moves)

    # cantidad de movimientos de las columnas 
    def getMovementColum(self):
        cont = 0
        #rint(self.stackColum[0][1][0])
        print(self.stackColum)
        valCol = self.stackColum[0][1][0]
        for r in range(len(self.board)):
            if self.board[r][valCol] != "--":
                cont += 1
        return cont-1

    def turn(self, r, c, moves):
        print("lugar de entrada turno")
        print(r,c)
        if ( not self.stackR==0 or not self.stackB ==0 ):
            jumps = self.getMovementColum()
        if self.whiteToMove:
            if self.stackB==0:
                for i in range(len(self.board)):
                    print("-value-"+str(i))
                    print((r+i),(c+1))
                    if self.board[i][c+1] == "--":
                        moves.append(Move((r, c), (i, c+1), self.board))
                    
                    #if self.board[r-1][c+1] == "--":
                    #    moves.append(Move((r, c), (r-1, c+1), self.board))
            else:
                for i in range(jumps):
                    if c+(i+1) > 7:
                        break
                    else:
                        if self.board[r][c+(i+1)] == "--":
                            moves.append(Move((r, c), (r, (c+i+1)), self.board))
                        if self.board[r-i-1][c-1] == "--":
                            moves.append(Move((r,c),(((r-i-1),c-1)),self.board))
        else:
            print("entro")
            if (self.stackR==0):
                if self.board[r][c-1] == "--":
                    moves.append(Move((r, c), (r, c-1), self.board))
                if r == 0 and self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
            else:
                for i in range(jumps,0,-1):
                    if c-r<0:
                        break
                    else:
                        if self.board[r][c-i] == "--":
                            moves.append(Move((r,c),(r,(c-i)),self.board))
                        ##if self.board[][]=="--"      
        ## por que carajos tengo esta monda aca 

        ##if self.whiteToMove:
        ##    print("entra")
        ##    if self.board[r][c+1] == "--":
        ##        moves.append(Move((r, c), (r, c+1), self.board))
        ##    if r == 7 and self.board[r-1][c+1] == "--":
        ##        moves.append(Move((r, c), (r-1, c+1), self.board))
        ##else:
        ##    if self.board[r][c-1] == "--":
        ##        moves.append(Move((r, c), (r, c-1), self.board))
        ##    if r == 0 and self.board[r+1][c] == "--":
        ##        moves.append(Move((r, c), (r+1, c), self.board))

class Move():

    def __init__(self, startSq, endSq, board):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow=endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveID=self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
