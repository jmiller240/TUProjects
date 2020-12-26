import turtle
import random
import P1
import P2

def drawSquare(t):
    for i in range(4):
        t.forward(1)
        t.left(90)
        
def drawBoard(numSquares):
    wn=turtle.Screen()
    bob=turtle.Turtle()
    bob.up()
    wn.setworldcoordinates(-2,numSquares+1,numSquares+1,-2)
    wn.tracer(False)
    #drawing rows and columns of squares
    for row in range(numSquares):
        for col in range(numSquares):
            drawSquare(bob)
            bob.forward(1)
        bob.backward(numSquares)
        bob.left(90)
        bob.forward(1)
        bob.right(90)
    #labelling the board
    bob.speed(0)
    bob.goto(0,0)
    bob.up()
    bob.forward(.5)
    for col in range(numSquares):
        bob.write(col,align='center',font=('Arial',16,'bold'))
        bob.forward(1)
    bob.goto(-.3,0)
    bob.left(90)
    bob.forward(.8)
    for row in range(numSquares):
        bob.write(chr(row+65),align='center',font=('Arial',16,'bold'))
        bob.forward(1)
    bob.hideturtle()
    wn.tracer(True)
    bob.goto(numSquares//2,-1)
    bob.write("PEGITY",align='center',font=('Lucida Calligraphy',20,'bold'))
    bob.ht()
    return bob,wn

def displayLogicalBoard(board):
    for row in board:
        print(row)

def drawMark(t,col,row,board):
    t.up()
    t.goto(col+.75,row+.5)
    t.color("yellow")
    t.down()
    t.begin_fill()
    t.circle(.25,360,360)
    t.end_fill()
    t.up()
    
def win(t,wn,board):
    for row in range(15):
        for col in range(15):
            if board[row][col]!='':
                #horizontal
                if col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row][col+offset]:
                            count+=1
                    if count==5:
                        wn.tracer(False)
                        for c in range(5):
                            drawMark(t,col+c,row,board)
                        wn.tracer(True)
                        return [True, board[row][col]]
                #vertical
                if row<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col]:
                            count+=1
                    if count==5:
                        wn.tracer(False)
                        for r in range(5):
                            drawMark(t,col,row+r,board)
                        wn.tracer(True)
                        return [True, board[row][col]]
                #CHECK DIAGONALS
                #left to right
                if row<11 and col<11:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col+offset]:
                            count+=1
                    if count==5:
                        wn.tracer(False)
                        for i in range(5):
                            drawMark(t,col+i,row+i,board)
                        wn.tracer(True)
                        return [True, board[row][col]]
                #right to left
                if row<11 and col>3:
                    count=1
                    for offset in range(1,5,1):
                        if board[row][col]==board[row+offset][col-offset]:
                            count+=1
                    if count==5:
                        wn.tracer(False)
                        for i in range(5):
                            drawMark(t,col-i,row+i,board)
                        wn.tracer(True)
                        return [True, board[row][col]]
    return [False,""]

def drawPlayer(t,col,row,player):
    t.up()
    t.color('white')
    t.goto(col+1,row+.5)
    t.color(player)
    t.down()
    t.begin_fill()
    t.circle(.5,360,360)
    t.end_fill()

def main(numSquares, oldGameFileName):
    #Set up graphical and logical game boards
    t,scrn=drawBoard(numSquares)
    row=['','','','','','','','','','','','','','','']
    board=[]
    for i in range(15):
        board.append(row[:])
    #If old game specified, read and set it
    if oldGameFileName!="":
        inFile=open(oldGameFileName,"r")
        fileNextPlayer=inFile.readline() #Read next player
        fileNextPlayer=fileNextPlayer.strip() #Remove \n
        row=0
        for line in inFile:
            line=line[:-1]
            for col in range(len(line)):
                if line[col]!='e':
                    board[row][col]=line[col]
                    drawPlayer(t,col,row,{'b':'blue','g':'green'}[line[col]])
                else:
                    board[row][col]=''
            row+=1
        inFile.close()
    #Pick the starting player
    if oldGameFileName!="":
        player=fileNextPlayer
    else:
        player=["blue","green"][random.randint(0,1)]

    #Play game
    move=""
    while move not in ["QUIT","Quit","quit"] and not win(t,scrn,board)[0]:
        if player=="blue":
            move=P1.getValidMove(t,scrn,board,player)
            print(player,move)
        else:
            move=P2.getValidMove(t,scrn,board,player)
            print(player,move)
        if move not in ["QUIT","Quit","quit"]:
            row=(ord(move[0]))-65
            col=int(move[1:])
            drawPlayer(t,col,row,player)
            board[row][col]=player[0]
            if player=="blue":
                player="green"
            else:
                player="blue"
                
    #Display the winner or save the partial game
    d={"g":"green","b":"blue"}
    if win(t,scrn,board)[0]:
        print("Winner is",d[win(t,scrn,board)[1]])
    elif move in ["QUIT","Quit","quit"]:
        saveFileName=input("Enter a name for the game file, or just hit enter for no save => ")
        if saveFileName !="":
            print("Saving game")
            outFile=open(saveFileName,"w")
            outFile.write(player+'\n')
            for row in board:
                outString=""
                for col in row:
                    if col=="":
                        outString=outString+'e'
                    else:
                        outString=outString+col
                outFile.write(outString+'\n')
            outFile.close()
            print("Game saved")
        else:
            print("Game abandoned")
    scrn.clearscreen()
    return win(t,scrn,board)[1]

greencount=0
bluecount=0            
for i in range(100):
    if main(15,"")=="b":
        bluecount+=1
    else:
        greencount+=1
print("Blue:", bluecount,"Green:",greencount)
