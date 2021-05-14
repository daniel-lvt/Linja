import LinjaBoard
import MoveFinder
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

        #MoveFinder.scoreM(self.board)

        if self.endGame():
            self.score()
            self.GameOver=True
        elif self.stackB == 1 or self.stackR == 1:
            if len(self.stackColum) > 0:
                self.stackColum.pop(0)
            self.stackColum.append(([move.endRow], [move.endCol]))
            if (self.conf and not self.extraB and self.whiteToMove and (self.stackColum[0][1][0] == 7)) or (self.conf and (self.stackColum[0][1][0] == 0 and not self.whiteToMove and not self.extraR)):
                self.conf = False
                if not self.extraB and self.whiteToMove:
                    self.extraB = True
                elif not self.extraR:
                    self.extraR = True
            else:
                #print('-----------------')
                #print('cambio de jugador')
                #print('---------------')
                self.reset_turn()

        elif (self.whiteToMove):
            if (len(self.stackColum) > 0):
                self.stackColum.clear()
            self.stackB += 1
            self.stackColum.append(([move.endRow], [move.endCol]))
        else:
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
        ## arreglar
        if not self.whiteToMove:
            self.whiteToMove=not self.whiteToMove
        if len(self.moveLog) != 0 :

            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            #print(self.board[move.startRow][move.startCol])
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if self.board[move.startRow][move.startCol]=='r':
                self.whiteToMove=True
            elif self.board[move.startRow][move.startCol]=='b':
                self.whiteToMove=False
            if len(self.stackColum)>0:
                self.stackColum.pop(0)
            if self.whiteToMove:
                if self.stackB>=0:
                    self.extraB=False if self.extraB==True else False
                    self.turnB=True
                    if self.stackB!=0:
                        self.stackB-=1

                self.conf=True
            else:
                if self.stackR>=0:
                    self.extraR=False if self.extraR==True else False
                    self.turnR=True
                    if self.stackR!=0:
                        self.stackR-=0

                self.conf=True
            self.conf=True#print('*********')
            #print(self.stackColum)
            #print(self.stackB)
            #print(self.stackR)
            #print(self.conf)
            #print(self.whiteToMove)
            #print('*********')
            #revisar falta probarlo mas
            #revisar en que csos estalla
            #if (self.whiteToMove and self.stackB>0) or (self.stackR>0 and not self.whiteToMove):
            #    self.whiteToMove = not self.whiteToMove

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
            #print('1')
            self.turn(r, c, moves)
        elif not self.turnB and self.whiteToMove:
            #print('2')
            self.turn(r, c, moves)
        elif self.turnR and not self.turnB:
            #print('3')
            self.turn(r, c, moves)
        else:
            #print('4')
            self.turn(r, c, moves)

    # cantidad de movimientos de las columnas
    def getMovementColum(self):
        cont = 0
        if len(self.stackColum)>0:
            valCol = self.stackColum[0][1][0]
            for r in range(len(self.board)):
                if self.board[r][valCol] != "--":
                    cont += 1
            return cont-1
        return 1

    def turn(self, r, c, moves):
        
        if (not self.stackR == 0 or not self.stackB == 0):
            jumps = self.getMovementColum()
            self.reset_turn() if jumps == 0 else False
        if self.extraB:
            #print('entrada extra en rojas')
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
            if self.extraR and not self.whiteToMove:
                #print('entrada etra en negras')
                self.turn_r('R', r, c, moves)
            elif self.stackR == 0:
                self.turn_r('R', r, c, moves)
            else:
                for i in range(jumps,0,-1):
                    if c-1<0 and c-i<0:
                        break
                    else:
                        for j in range(len(self.board)):
                            if self.board[j][c-i]=="--":
                                moves.append(Move((r,c),(j,(c-i)),self.board))


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
    def endGame(self):
        cont=0
        state=False
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if(turn == 'r' and self.whiteToMove):
                    if c<4:
                        cont+=1
                elif (turn == 'b' and not self.whiteToMove):
                    if c>3:
                        cont+=1
        return state if cont>0 else True

    def score(self):

        scoreBlack={'b1':0,'b2':0,'b3':0,'b4':0}
        scoreRed={'r1':0,'r2':0,'r3':0,'r4':0}

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if turn=='b' and c==0:
                    scoreBlack['b4']+=5
                elif turn=='b' and c==1:
                    scoreBlack['b3']+=3
                elif turn=='b' and c==2:
                    scoreBlack['b2']+=2
                elif turn=='b' and c==3:
                    scoreBlack['b1']+=1
                elif turn=='r' and c==4:
                    scoreRed['r1']+=1
                elif turn=='r' and c==5:
                    scoreRed['r2']+=2                                      
                elif turn=='r' and c==6:
                    scoreRed['r3']+=3
                elif turn=='r' and c==7:
                    scoreRed['r4']+=5
        
        out=self.strScore(scoreRed,scoreBlack)
        return out  
    
    def strScore(self,r,b):
        total=0
        index=1
        text="Red :"
        for i in r:
            valor=r[i]
            text+="[("+str(index)+"):"+str(valor)+"]"
            total+=valor
            if index==3:
                index+=2
            else:
                index+=1
        text+=" Total: "+str(total)+"\n"
        total=0
        index=1
        text+="Black :"
        for i in b:
            valor=b[i]
            text+="[("+str(index)+"): "+str(valor)+"]"
            total+=valor
            if index==3:
                index+=2
            else:
                index+=1
        text+=" Total: "+str(total)+" \n"
        return text
                                 

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
