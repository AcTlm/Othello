"""
Program: project2.py
Author: Cameron Armstrong
Last modified: 28/5/14

A game of Othello.
"""

import turtle
from random import randint
import math
import os
import time

n = 8 
def initialiseBoard(n):
    board = [[0 for i in range(n)] for j in range(n)]
    half = int(n/2)
    board[half-1][half-1] = 1
    board[half-1][half] = -1
    board[half][half-1] = -1
    board[half][half] = 1
    return board

def drawBoard(boardSize, t):
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.right(90)
    t.forward(350)
    t.left(90)
    t.forward(350)
    t.left(90)
    t.pendown()
    t.forward(700)
    t.left(90)
    for coln in range(boardSize):
        t.forward(700/boardSize)
        t.left(90)
        t.forward(700)
        t.backward(700)
        t.right(90)

    t.left(90)

    for row in range(boardSize):
        t.forward(700/boardSize)
        t.left(90)
        t.forward(700)
        t.backward(700)
        t.right(90)

    t.penup()
    t.goto(0,375)
    t.pencolor("lightblue")
    t.write("OTHELLO",False,align='center',font=("Arial", 16, "bold"))
    
    for row in range(boardSize):
        t.pencolor("orange")
        t.goto(-370,(350-(row)*700/boardSize-700/boardSize/3*2))
        t.write(str(row+1),False,align='center',font=("Arial",12,"normal"))

    for coln in range(boardSize):
        t.pencolor("magenta")
        t.goto((-350+(coln)*700/boardSize+700/boardSize/2),360)
        t.write(chr(coln+65),False,align='center',font=("Arial",12,"normal"))

def updateScreen(b):
    boardSize = len(b)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    t.shapesize(700/boardSize/25)
    t.pencolor("black")
    t.shape("circle")
    t.penup()
    for row in range(boardSize):
        for coln in range(boardSize):
            if (b[row][coln] > 0):
                t.goto(700/boardSize*coln-350+700/boardSize/2,700/boardSize*row-350+700/boardSize/2)
                t.fillcolor("black")
                t.stamp()
            if (b[row][coln] < 0):
                t.goto(700/boardSize*coln-350+700/boardSize/2,700/boardSize*row-350+700/boardSize/2)
                t.fillcolor("white")
                t.stamp()
    return

def move(b, m, p):
    r = m[0]
    c = m[1]
    if (len(m[2]) == 0):
        return
    else:
        for move in m[2]:
            newR = r + move[0]
            newC = c + move[1]
            while (b[newR][newC] != abs(b[newR][newC])*p):
                b[newR][newC] = (abs(b[newR][newC]) + 1) * p
                newR = newR + move[0]
                newC = newC + move[1]
        b[r][c] = p
        placePiece(b, r, c, p)
        updateScreen(b)

def legalDirection(r, c, b, p, u, v):
    foundOpponent = False
    while (r >= 0 and r <= len(b) and c >= 0 and c <= len(b)):
           r = r + u
           c = c + v
           if (r < 0 or r >= len(b) or c < 0 or c >= len(b)):
               return False
           if (b[r][c] == 0):
               return False
           if (b[r][c] == abs(b[r][c])*p):
               if foundOpponent:
                return True
               else:
                   return False
           if (b[r][c] != abs(b[r][c])*p):
                   foundOpponent = True
    return False

def legalMove(r, c, b, p):
    legalDirections = []
    if (b[r][c] != 0):
        return legalDirections
    if (legalDirection(r, c, b, p, -1, -1)):
        legalDirections.append((-1, -1))
    if (legalDirection(r, c, b, p, -1, 0)):
        legalDirections.append((-1, 0))
    if (legalDirection(r, c, b, p, -1, 1)):
        legalDirections.append((-1, 1))
    if (legalDirection(r, c, b, p, 0, -1)):
        legalDirections.append((0, -1))
    if (legalDirection(r, c, b, p, 0, 0)):
        legalDirections.append((0, 0))
    if (legalDirection(r, c, b, p, 0, 1)):
        legalDirections.append((0, 1))
    if (legalDirection(r, c, b, p, 1, -1)):
        legalDirections.append((1, -1))
    if (legalDirection(r, c, b, p, 1, 0)):
        legalDirections.append((1, 0))
    if (legalDirection(r, c, b, p, 1, 1)):
        legalDirections.append((1, 1))
    return legalDirections

def moves(b, p):
    availableMoves = []
    for r in range(len(b)):
        for c in range(len(b)):
            legal = legalMove(r, c, b, p)
            if legal != []:
                availableMoves.append((r, c, legal))
    return availableMoves

def scoreBoard(b):
    blackScore = 0
    whiteScore = 0
    for r in range(len(b)):
        for c in range(len(b)):
            if (b[r][c] > 0):
                if b[r][c] > 0:
                    blackScore = blackScore + b[r][c]
            if (b[r][c] < 0):
                if b[r][c] < 0:
                    whiteScore = whiteScore - b[r][c]
    return (blackScore, whiteScore)

def checkMoveScore(b, m, p): # Goes through all possible moves and finds the one with the highest score. The computer will choose this one.
    moveScore = 1
    r = m[0]
    c = m[1]
    if (len(m[2]) == 0):
        return 0
    else:
        for move in m[2]:
            newR = r + move[0]
            newC = c + move[1]
            while (b[newR][newC] != abs(b[newR][newC])*p):
                moveScore = moveScore + abs(b[newR][newC])
                newR = newR + move[0]
                newC = newC + move[1]
    return moveScore

def selectMove(b, availableMoves, p):
    bestMoveScore = 0
    bestMoveIndex = -1
    currentMoveIndex = 0
    for availableMove in availableMoves:
        currentMoveScore = checkMoveScore(b, availableMove, p)
        if (bestMoveScore < currentMoveScore):
            bestMoveIndex = currentMoveIndex
            bestMoveScore = currentMoveScore
        currentMoveIndex = currentMoveIndex + 1
    return availableMoves[bestMoveIndex]

def placePiece(b, r, c, p): # Animates the placement of a piece.
    boardSize = len(b)
    t = turtle.Turtle()
    t.penup()
    t.hideturtle()
    t.shapesize(8)
    t.pencolor("black")
    if p == 1:
        t.fillcolor("black")
        t.goto(0, -400)
    else:
        t.goto(0, 400)
        t.fillcolor("white")
    t.speed(4)
    t.shape("circle")
    t.showturtle()
    t.goto(700/boardSize*c-350+700/boardSize/2,700/boardSize*r-350+700/boardSize/2)
    for x in range(1,50):
        t.shapesize(8 - (8 - 700/boardSize/25)/50*x)
    t.shapesize(700/boardSize/25)
    t.stamp()
    return

def getPreviousScores(f): # Reads previous scores saved in file.
	scores = []
	currentDirectoryPath = os.getcwd()
	listOfFileNames = os.listdir(currentDirectoryPath)
	for name in listOfFileNames:
		if name == f:
			scoresFile = open(f, 'r')
			for line in scoresFile:
				line = line.strip()
				if (line == ""):
					continue
				scores.append(line)
	return scores

def saveScore(scores,f,players,size): # Saves the current set of scores to disk.
    file = open(f, "a")
    localtime = time.asctime( time.localtime(time.time()))
    line = localtime + " " + "Black: " + str(scores[0]) + " White: " + str(scores[1]) + " Players: " + str(players) + " Size: " + str(size) + "\n"
    file.write(line)
    file.close()
    return

def main():
    playing  = True
    while playing:
        board = []
        inGame = False
        numPlayers = 0
        option = 0
        while (not inGame):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("********************************")
            print("*          OTHELLO             *")
            print("******************************** (c) Cameron Armstrong")
            print("")
            print("1. 1 Player Mode")
            print("2. 2 Player Mode")
            print("3. Observer Mode (Computer vs Computer)")
            print("4. Previous Scores")
            while (option < 1 or option > 4):
                try:
                    option = int(input("Enter option: "))
                    if option < 4:
                        inGame = True
                except:
                  pass
            if option == 4:
                 os.system('cls' if os.name == 'nt' else 'clear')
                 option = 0
                 previousScores = getPreviousScores("scores.txt")
                 if previousScores == []:
                     print("No previous scores saved. \nPlay some games and your scores will get saved to disk.")
                 else:
                   for line in previousScores:
                      print(line)
                 input("Press enter to continue.")

        numPlayers = option
        if numPlayers == 3:
            numPlayers = 0
        while (board == []):
            try:
                boardSize = int(input("Enter the board size (4-26): "))
                screen = turtle.Screen()
                screen.clear()
                board = initialiseBoard(boardSize)
            except:
                   print("Enter a valid number.")
                   pass

        t = turtle.Turtle()
        t.hideturtle()
        turtleText = turtle.Turtle()
        turtleText.hideturtle()
        turtleText.penup()
        turtleText.speed(0)
        turtle.title("Othello")
        turtle.setup(800, 800)
        screen.bgcolor("darkgreen")
        drawBoard(boardSize, t)
        updateScreen(board)
        playerTurn = 1
        gameOver = False
        blackCanMove = True
        whiteCanMove = True
        while (not gameOver):
            if playerTurn == -1:
                print("Player white's turn.")
            else:
                print("Player black's turn.")
            scores = scoreBoard(board)
            turtleText.clear()
            turtleText.pencolor("black")
            turtleText.goto(-300, -380)
            turtleText.write("Black: " + str(scores[0]),False,align='center',font=("Arial",12,"bold"))
            turtleText.pencolor("white")
            turtleText.goto(300, -380)
            turtleText.write("White: " + str(scores[1]),False,align='center',font=("Arial",12,"bold"))
            validMove = False
            if ((playerTurn == -1 and numPlayers < 2) or numPlayers == 0):
                availableMoves = moves(board, playerTurn)
                if availableMoves != []:
                    if playerTurn == -1:
                        whiteCanMove = True
                    else:
                        blackCanMove = True
                    validMove = True
                    bestMove = selectMove(board, availableMoves, playerTurn)
                    move(board, bestMove, playerTurn)
                else:
                    validMove = True
                    if playerTurn == -1:
                        whiteCanMove = False
                    else:
                        blackCanMove = False
                    print("No available moves. Skipping turn.")

            if (numPlayers > 0):
                availableMoves = moves(board, playerTurn)
                if availableMoves == []:
                    if playerTurn == 1:
                        blackCanMove = False
                    else:
                        whiteCanMove = False
                    validMove = True
                    print("No available moves. Skipping turn.")
                else:
                    if playerTurn == -1:
                        whiteCanMove = True
                    else:
                        blackCanMove = True

            if (not blackCanMove and not whiteCanMove):
                print("GAME OVER!")
                saveScore(scores, "scores.txt", numPlayers, boardSize)
                if scores[0] > scores[1]:
                    turtleText.goto(0, 0)
                    turtleText.pendown()
                    turtleText.pencolor("black")
                    for degrees in range(0,360,4):
                        angle = math.radians(degrees)
                        length = randint(1,400)
                        turtleText.goto(length*math.cos(angle),length*math.sin(angle))
                        turtleText.goto(0,0)
                    turtleText.pencolor("red")
                    turtleText.write("Black Wins!",False,align='center',font=("Arial",72,"bold"))
                    print("Black wins!")
                else:
                    turtleText.goto(0, 0)
                    turtleText.pendown()
                    turtleText.pencolor("white")
                    for degrees in range(0,360,4):
                        angle = math.radians(degrees)
                        length = randint(1,400)
                        turtleText.goto(length*math.cos(angle),length*math.sin(angle))
                        turtleText.goto(0,0)
                    turtleText.pencolor("red")
                    turtleText.write("White Wins!",False,align='center',font=("Arial",72,"bold"))
                    print("White wins!")
                gameOver = True

            while (not validMove):
                inRange = False
                while (not inRange):
                    r = -1
                    try: 
                        r = boardSize - int(input("Row of new piece: "))
                    except:
                        print("Enter a valid number in range.")
                        pass
                    if (r >= 0 and r < boardSize):
                        inRange = True
                    else:
                        print("Enter a valid number in range.")
                inRange = False
                while (not inRange):
                    c = input("Column of new piece: ")
                    c = c.upper()
                    try:
                        c = ord(c) - ord('A')
                        if (c >= 0 and c < boardSize):
                            inRange = True
                        else:
                            print("Enter a valid letter in range.")
                    except:
                           print("Enter a valid letter in range.")
                           pass
                availableMoves = [r, c, legalMove(r, c, board, playerTurn)]
                if (availableMoves[2] != []):
                    validMove = True
                    move(board, availableMoves, playerTurn)
                else:
                    print("Invalid move.")
            if playerTurn == -1:
                playerTurn = 1
            else:
                playerTurn = -1
        playAgain = -1
        while (playAgain < 1 or playAgain > 2):
            try:
                print("Play again?")
                print("1. yes")
                print("2. no")
                playAgain = int(input(""))
                if playAgain == 2:
                    playing = False
            except:
                pass
    return

main()