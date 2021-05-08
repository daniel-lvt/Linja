import LinjaBoard
# B= Rojos
# R= negros


class GameState():
    def __init__(self):
        self.board = LinjaBoard.board_principal
        self.whiteToMove = True
        self.moveLog = []
        self.stackB = 0
        self.stackR = 0
        self.turnB = True
        self.turnR = True
        self.stackColum = []
        self.extraB = False
        self.extraR = False
        self.conf = True
        self.GameOver=False

    # recibe el movimiento de inicio y final de columna
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)

        if self.stackB == 1 or self.stackR == 1:
            if len(self.stackColum) > 0:
                self.stackColum.pop(0)
            self.stackColum.append(([move.endRow], [move.endCol]))
            if (self.conf and not self.extraB and self.whiteToMove and (self.stackColum[0][1][0] == 7)) or (self.conf and (self.stackColum[0][1][0] == 0 and not self.whiteToMove and not self.extraR)):
                self.conf = False
                if not self.extraB:
                    self.extraB = True
                elif not self.extraR:
                    self.extraR = True
            else:
                print('-----------------')
                print('cambio de jugador')
                print('---------------')
                self.reset_turn()

        elif (self.whiteToMove):
            print("--2--")
            if (len(self.stackColum) > 0):
                self.stackColum.clear()
            self.stackB += 1
            #print("ye tenemos cambio en el valor del primer cambio "+str(self.stackB))
            self.stackColum.append(([move.endRow], [move.endCol]))
        else:
            print("--3--")
            if (len(self.stackColum) > 0):
                self.stackColum.clear()
            self.stackR += 1
            self.stackColum.append(([move.endRow], [move.endCol]))

    def reset_turn(self):
        self.whiteToMove = not self.whiteToMove
        self.stackB = 0
        self.stackR = 0
        self.conf = True
        self.extraB = False
        self.extraR = False

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
        # valida el turno del movimiento
        if self.turnB:
            self.turnB = False
        elif not self.whiteToMove:
            if not self.turnB:
                self.turnR = False
        return moves

    # definicion de turno

    def getMoves(self, r, c, moves, turn):

        if self.turnB:
            print('movimiento P1')
            self.turn(r, c, moves)
        elif not self.turnB and self.whiteToMove:
            print('movimiento P1')
            self.turn(r, c, moves)
        elif self.turnR and not self.turnB:
            print(' movimiento P2')
            self.turn(r, c, moves)
        else:
            print('movimiento P2')
            self.turn(r, c, moves)

    # cantidad de movimientos de las columnas
    def getMovementColum(self):
        cont = 0
        valCol = self.stackColum[0][1][0]
        for r in range(len(self.board)):
            if self.board[r][valCol] != "--":
                cont += 1
        return cont-1

    def turn(self, r, c, moves):
        print(self.board[r][c])
        print(r,c)
        if (not self.stackR == 0 or not self.stackB == 0):
            jumps = self.getMovementColum()
            self.reset_turn() if jumps == 0 else False
        if self.extraB:
            self.turn_r('B', r, c, moves)
        elif self.whiteToMove:
            if self.stackB == 0:
                self.turn_r('B', r, c, moves)
            else:
                for i in range(jumps):
                    if c+(i+1) > 7:
                        break
                    else:
                        for j in range(len(self.board)):
                            if self.board[j][c+(i+1)] == "--":
                                moves.append(
                                    Move((r, c), (j, (c+i+1)), self.board))
        else:
            # movimiento extra para fichas negras revisar puesta en escena para verificar posicion en la que se va a colocar
            if self.extraR:
                self.turn_r('R', r, c, moves)
            elif self.stackR == 0:
                self.turn_r('R', r, c, moves)
            else:
                for i in range(jumps, 0, -1):
                    for j in range(len(self.board)):
                        if c-j < 0:
                            break
                        else:
                            if self.board[j][c-i] == "--":
                                moves.append(
                                    Move((r, c), (j, (c-i)), self.board))
        

    def turn_r(self, type, r, c, moves):
        if type == 'B':
            for i in range(len(self.board)):
                if c+1 > 7:
                    break
                else:
                    if self.board[i][c+1] == "--":
                        moves.append(Move((r, c), (i, c+1), self.board))
        elif type == 'R':
            for i in range(len(self.board)):
                if c-1 < 0:
                    break
                else:
                    if self.board[i][c-1] == "--":
                        moves.append(Move((r, c), (i, c-1), self.board))
        else:
            print('---ERROR EN LA MATRIX---')

    ##fijar final de juego 
    def endGame(self,r,c):
        print(r,c)
        print(self.board[r][c])


class Move():

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000+self.startCol*100+self.endRow*10+self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
