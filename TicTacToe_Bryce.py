import pandas as pd
import numpy as np
import math
import copy

def humanMove(board, humanPlayer):

    print('Your turn!')
    movecellInput = int(input("What cell do you wish to move into? (1 to 9 left to right)"))
    movecell = movecellInput - 1
    row, column = indexToRowCol(movecell)
    board = submitMove(row, column, board, humanPlayer, "HUM")
    return board

def computerMove(board, computerPlayer):

    possibilityTree, move = computerThink(board, computerPlayer)
    row, column = indexToRowCol(move)

    board = submitMove(row, column, board, computerPlayer, "CPU")
    return board

def computerThink(board, computerPlayer):
    possibilityTree = [0] * 9
    startBoard = copy.deepcopy(board)
    if computerPlayer == 1:
        valueTarget = 1
    else:
        valueTarget = -1
    valueReached = False

    for i in range(9):
        board = copy.deepcopy(startBoard)
        row, column = indexToRowCol(i)

        if startBoard[row][column] != 0:
            if computerPlayer == 1:
                possibilityTree[i] = -2
            else:
                possibilityTree[i] = 2
            continue
        board[row][column] = computerPlayer
        winner, winningPlayer = checkWin(board)
        empty = emptySpaces(board)

        if winner:
            possibilityTree[i] = winningPlayer
        elif not empty:
            possibilityTree[i] = 0
        else:
            possibilityTree[i], move = computerThink(board, -computerPlayer)

        for j in range(i):
            if possibilityTree[j] == valueTarget:
                valueReached = True

        if valueReached:
            break


    if computerPlayer == 1:
        optionValue = max(possibilityTree)
    else:
        optionValue = min(possibilityTree)

    for i in range(9):
        if optionValue == possibilityTree[i]:
            move = i
            break

    return optionValue, move

def indexToRowCol(number):

    column = (number) % 3
    row = math.floor(number / 3)
    return row, column

def submitMove(row, column, board, player, playerType):
    cellValue = board[row][column]
    if cellValue == 0: #valid move
        board[row][column] = player
    else: #invalid
        print("invalid Move, try again!")
        if playerType == "CPU":
            board = computerMove(board, player)
        else:
            board = humanMove(board, player)

    return board

def printBoard(board):
    outputBoard = [['', '', ''], ['', '', ''], ['', '', '']]
    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                outputBoard[i][j] = 'X'
            elif board[i][j] == -1:
                outputBoard[i][j] = 'O'


    for i in range(3):
        print(outputBoard[i])

    return

def checkWin(board):
    #check row
    for i in range(3):
        sumRows = board[i][0] + board[i][1] + board[i][2]
        if sumRows == 3 or sumRows == -3:
            break
        else:
            continue

    #check column
    for i in range(3):
        sumCol = board[0][i] + board[1][i] + board[2][i]
        if sumCol == 3 or sumCol == -3:
            break
        else:
            continue

    sumDiag1 = board[0][0] + board[1][1] + board[2][2]
    sumDiag2 = board[2][0] + board[1][1] + board[0][2]

    sumVector = [sumRows, sumCol, sumDiag1, sumDiag2]

    winner = False
    winningPlayer = 0
    for i in range(4):
        if sumVector[i] == 3 or sumVector[i] == -3:
            winner = True
            if sumVector[i] == 3:
                winningPlayer = 1
            else:
                winningPlayer = -1

            break

    return winner, winningPlayer

def emptySpaces(board):
    empty = False
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                empty = True
                break

    return empty



board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
printBoard(board)



humanPlayerInput = input("What do you wish to Play as? [X, O]: ")

if humanPlayerInput == 'X':
    humanPlayer = 1
else:
    humanPlayer = -1

if humanPlayer == 1:
    currentPlayer = "HUM"
    computerPlayer = -1
else:
    currentPlayer = "CPU"
    computerPlayer = 1

## begin game
winner = False
empty = True

while not winner and empty:
    if currentPlayer == "HUM":
        board = humanMove(board, humanPlayer)
        printBoard(board)
        winner, winningPlayer = checkWin(board)
        empty = emptySpaces(board)

        if not winner:
            currentPlayer = "CPU"

    else:
        print("Computer's Turn!!!!")
        print("")
        print("")

        board = computerMove(board, computerPlayer)
        printBoard(board)
        winner, winningPlayer = checkWin(board)

        print("")
        if not winner:
            currentPlayer = "HUM"


if winner:
    print(currentPlayer+' Wins!!!!')
else:
    print("SCRATCH!")




