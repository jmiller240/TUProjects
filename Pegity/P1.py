import random
def emptyBoard(board):
    for row in range(15):
        for col in range(15):
            if board[row][col] != "":
                return False
    return True

def getMovesNextTo(playerSymbol,board):
    movesList=[]
    for row in range(15):
        for col in range(15):
            if board[row][col]==playerSymbol:
                for rowInc in [-1,0,1]:
                    for colInc in [-1,0,1]:
                        if row+rowInc>-1 and row+rowInc<15:
                            if col+colInc>-1 and col+colInc<15:
                                if not(rowInc==0 and colInc==0) and board[row+rowInc][col+colInc]=="":
                                    movesList.append(chr(row+rowInc+65)+str(col+colInc))
    return movesList


def NinARow(N,player,board):
    NinARowList=[]
    playerRun=[player]*N
    #Check for row of N
    for row in range(0,15):
        for col in range(0,15-N+1):
            if board[row][col:col+N]==playerRun:
                #Any empty spaces on either end?
                #Left side?
                leftCol=col-1
                if leftCol>-1:
                    if board[row][leftCol]=='':
                        mvRow=chr(row+65)
                        NinARowList.append(mvRow+str(leftCol))
                #Right side?
                rightCol=col+N
                if rightCol<15:
                    if board[row][rightCol]=='':
                        mvRow=chr(row+65)
                        NinARowList.append(mvRow+str(rightCol))
    return NinARowList

def NinACol(N,player,board):
    NinAColList=[]
    #Check for col of N
    for col in range(0,15):
        for row in range(0,15-N+1):
            countPlayer=0
            for pt in range(0,N):
                if board[row+pt][col]==player:
                    countPlayer=countPlayer+1
            if countPlayer==N:
                #Any empty spaces at upper or lower end?
                #Upper end?
                rowAbove=row-1
                if rowAbove>-1:
                    if board[rowAbove][col]=='':
                        mvRow=chr(rowAbove+65)
                        NinAColList.append(mvRow+str(col))
                #Lower end?
                rowBelow=row+N
                if rowBelow<15:
                    if board[rowBelow][col]=='':
                        mvRow=chr(rowBelow+65)
                        NinAColList.append(mvRow+str(col))
    return NinAColList


def NinLeftToRightDiagonal(N,player,board):
    diagOfN_EndsList=[]
    #Check for diagonal of N
    #Left to Right Top to Bottom
    for row in range(0,15-N+1):
        for col in range(0,15-N+1):
            if board[row][col]==player:
                countPlayer=0
                for pt in range(0,N):
                    #print(row+pt,col+pt)
                    if board[row+pt][col+pt]==player:
                        countPlayer=countPlayer+1
                #print(countPlayer)
                #input()
                if countPlayer==N:
                    #Any empty spaces at upper or lower end?
                    #Upper end?
                    rowAbove=row-1
                    if rowAbove > -1:
                        colAbove=col-1
                        if colAbove > -1:
                            if board[rowAbove][colAbove]=='':
                                mvRow=chr(rowAbove+65)
                                diagOfN_EndsList.append(mvRow+str(colAbove))
                    #Lower end?
                    rowBelow=row+N
                    if rowBelow < 15:
                        colBelow=col+N
                        if colBelow < 15:
                            if board[rowBelow][colBelow]=='':
                                mvRow=chr(rowBelow+65)
                                diagOfN_EndsList.append(mvRow+str(colBelow))
    return diagOfN_EndsList

def NinRightToLeftDiagonal(N,player,board):
    diagOfN_EndsList=[]
    #Check for diagonal of N
    #Left to Right Top to Bottom
    for row in range(0,15-N+1):
        for col in range(N-1,15):
            if board[row][col]==player:
                #print("Found player at",row,col)
                countPlayer=0
                for pt in range(0,N):
                    #print(pt,row+pt,col+pt)
                    if board[row+pt][col-pt]==player:
                        countPlayer=countPlayer+1
                #print(countPlayer)
                #input()
                if countPlayer==N:
                    #Any empty spaces at upper or lower end?
                    #Upper end?
                    rowAbove=row-1
                    if rowAbove > -1:
                        colAbove=col+1
                        if colAbove < 15:
                            if board[rowAbove][colAbove]=='':
                                mvRow=chr(rowAbove+65)
                                diagOfN_EndsList.append(mvRow+str(colAbove))
                    #Lower end?
                    rowBelow=row+N
                    if rowBelow < 15:
                        colBelow=col-N
                        if colBelow > -1:
                            if board[rowBelow][colBelow]=='':
                                mvRow=chr(rowBelow+65)
                                diagOfN_EndsList.append(mvRow+str(colBelow))
    return diagOfN_EndsList

#Heuristic H - Check for and play if there's a run of length N+1 with N markers and no opponent markers
def NinNPlusOne(N,player,board):
    for row in range(15):
        for col in range(11):
            runlist=[]
            for i in range(N+1):
                runlist.append(board[row][col+i])
            if runlist.count(player) == N and runlist.count("") == 1:
                index=runlist.index("")
                return chr(row+65)+str(col+index)

    for col in range(15):
        for row in range(11):
            #runlist=[board[row][col],board[row+1][col],board[row+2][col],board[row+3][col],board[row+4][col]]
            runlist=[]
            for i in range(N+1):
                runlist.append(board[row+i][col])
            if runlist.count(player) == 4 and runlist.count("") == 1:
                index=runlist.index("")
                return chr(row+index+65)+str(col)

    for row in range(11):
        for col in range(11):
            #runlist=[board[row][col],board[row+1][col+1],board[row+2][col+2],board[row+3][col+3],board[row+4][col+4]]
            runlist=[]
            for i in range(N+1):
                runlist.append(board[row+i][col+i])
            if runlist.count(player) == 4 and runlist.count("") == 1:
                index=runlist.index("")
                return chr(row+index+65)+str(col+index)
            
    for row in range(11):
        for col in range(4,15):
            #runlist=[board[row][col],board[row+1][col-1],board[row+2][col-2],board[row+3][col-3],board[row+4][col-4]]
            runlist=[]
            for i in range(N+1):
                runlist.append(board[row+i][col-i])
            if runlist.count(player) == 4 and runlist.count("") == 1:
                index=runlist.index("")
                return chr(row+index+65)+str(col-index)


def getNConsectiveEndMoves(N,player,board):
    lstPossibleMoves=[]
    lstPossibleMoves+=NinARow(N,player,board)
    lstPossibleMoves+=NinACol(N,player,board)
    lstPossibleMoves+=NinLeftToRightDiagonal(N,player,board)
    lstPossibleMoves+=NinRightToLeftDiagonal(N,player,board)
    return lstPossibleMoves

def getValidMove(t,scrn,board,player):
    if player=="blue":
        playerSymbol="b"
        opposingPlayerSymbol="g"
    else:
        playerSymbol="g"
        opposingPlayerSymbol="b"
        
    #Heuristic 1 - if empty board, take a center square
    if emptyBoard(board):
        return "G7"

    #Heuristic H - If I have a run of four in five spaces with no opponent presence, take the win
    if NinNPlusOne(4,playerSymbol,board)!=None:
        return NinNPlusOne(4,playerSymbol,board)
        
    #Heuristic A - 4 for me
    allMovesFor4List=getNConsectiveEndMoves(4,playerSymbol,board)
    repeatsList=[]
    for move in allMovesFor4List:
        if allMovesFor4List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesFor4List!=[]:
            return allMovesFor4List[random.randrange(0,len(allMovesFor4List))]

    #Heuristic H - If the opponent has a run of four in five spaces with none of my pegs, block the win
    if NinNPlusOne(4,opposingPlayerSymbol,board)!=None:
        return NinNPlusOne(4,opposingPlayerSymbol,board)    
        
    #Heuristic B - 4 for opponent
    allMovesForOpp4List=getNConsectiveEndMoves(4,opposingPlayerSymbol,board)
    repeatsList=[]
    for move in allMovesForOpp4List:
        if allMovesForOpp4List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesForOpp4List!=[]:
            return allMovesForOpp4List[random.randrange(0,len(allMovesForOpp4List))]
        
    #Heuristic G - Prioritize playing on pegs of length two that can be joined together this turn
    allMovesFor2List=getNConsectiveEndMoves(2,playerSymbol,board)
    repeatsList=[]
    for move in allMovesFor2List:
        if allMovesFor2List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]

    #Heuristic H - Prioritize joining two pegs to make a peg of length four     
    if NinNPlusOne(3,playerSymbol,board)!=None:
        return NinNPlusOne(3,playerSymbol,board)
        
    #Heuristic C - 3 for me
    allMovesFor3List=getNConsectiveEndMoves(3,playerSymbol,board)
    repeatsList=[]
    for move in allMovesFor3List:
        if allMovesFor3List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesFor3List!=[]:
            return allMovesFor3List[random.randrange(0,len(allMovesFor3List))]

    #Heuristic G - Prioritize blocking pegs of length two that can be joined together this turn
    allMovesForOpp2List=getNConsectiveEndMoves(2,opposingPlayerSymbol,board)
    repeatsList=[]
    for move in allMovesForOpp2List:
        if allMovesForOpp2List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]

    #Heuristic H - Prioritize blocking two pegs that could make a peg of length four     
    if NinNPlusOne(3,opposingPlayerSymbol,board)!=None:
        return NinNPlusOne(3,opposingPlayerSymbol,board)
        
    #Heuristic D - 3 for opponent
    allMovesForOpp3List=getNConsectiveEndMoves(3,opposingPlayerSymbol,board)
    repeatsList=[]
    for move in allMovesForOpp3List:
        if allMovesForOpp3List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesForOpp3List!=[] and len(allMovesForOpp3List) > 1:
            return allMovesForOpp3List[random.randrange(0,len(allMovesForOpp3List))]
    
    #Heuristic E - 2 for me
    #The getNConsecutiveEndMoves  will provide the information for implementing
    #lots of additional heuristics
    allMovesFor2List=getNConsectiveEndMoves(2,playerSymbol,board)
    repeatsList=[]
    for move in allMovesFor2List:
        if allMovesFor2List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesFor2List!=[]:
            return allMovesFor2List[random.randrange(0,len(allMovesFor2List))]

    #Heuristic F - 2 for opponent
    allMovesForOpp2List=getNConsectiveEndMoves(2,opposingPlayerSymbol,board)
    repeatsList=[]
    for move in allMovesForOpp2List:
        if allMovesForOpp2List.count(move)>1 and move not in repeatsList:
            repeatsList.append(move)
    if repeatsList!=[]:
        return repeatsList[random.randrange(0,len(repeatsList))]
    else:
        if allMovesForOpp2List!=[]:
            return allMovesForOpp2List[random.randrange(0,len(allMovesForOpp2List))]

    #Heuristic 2 - move next to an existing peg for this player
    moveNextToMeList=getMovesNextTo(playerSymbol,board)
    if moveNextToMeList != []:
        return moveNextToMeList[random.randrange(0,len(moveNextToMeList))]
    
    #Heuristic 3 - move next to an existing peg for the other player
    moveNextToOpposingList=getMovesNextTo(opposingPlayerSymbol,board)
    if moveNextToOpposingList != []:
        return moveNextToOpposingList[random.randrange(0,len(moveNextToOpposingList))]


    #Otherwise, make a random move (not a possible strategy given the earlier heuristics)
    row = random.randint(0,14)
    col = random.randint(0,14)
    while board[row][col] != '':
        row = random.randint(0,14)
        col = random.randint(0,14)
    return chr(row+65)+str(col)
