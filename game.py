import os
import sys
import random

SHIPS = [("carrier",    (5, 'C')),  #Carrier
         ("battleship", (4, 'B')),  #Battleship
         ("cruiser",    (3, 'R')),  #Cruiser
         ("submarine",  (2, 'S')),  #Submarine
         ("destroyer",  (2, 'D'))]  #Destroyer

def main():

    # Clear console in terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    gameOver = False
    isPlayer1Turn = True

    BOARD_PLAYER_1 = buildBoard(True, SHIPS)
    BOARD_PLAYER_2 = buildBoard(True, SHIPS)
    hiddenBoardPlayer1 = buildBoard(False, SHIPS)
    hiddenBoardPlayer2 = buildBoard(False, SHIPS)

    while not gameOver:
        if isPlayer1Turn:
            print("Player 1's turn:")
            displayBoard(hiddenBoardPlayer1)
            coordinates = promptCoordinates()
            #DEBUGGING PURPOSES ONLY: PRESET COORDINATES
            #row = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
            #col = ['0', '1', '2', '3', '4', '5', '6', '7']
            #coordinates = (random.choice(row), random.choice(col))
            hiddenBoardPlayer1 = fire(BOARD_PLAYER_1, SHIPS, hiddenBoardPlayer1, coordinates)
            displayBoard(hiddenBoardPlayer1)
            print("")
            isPlayer1Turn = False
        else:
            print("Player 2's turn:")
            displayBoard(hiddenBoardPlayer2)
            coordinates = promptCoordinates()
            hiddenBoardPlayer2 = fire(BOARD_PLAYER_2, SHIPS, hiddenBoardPlayer2, coordinates)
            displayBoard(hiddenBoardPlayer2)
            print("")
            isPlayer1Turn = True

def buildBoard(randomizeShips, SHIPS):
    BOARD_MATRIX = [['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-']]
    
    if randomizeShips:
        return randomizeBoard(BOARD_MATRIX, SHIPS)

    return BOARD_MATRIX

def randomizeBoard(matrix, SHIPS):
    localMatrix = matrix

    for ship in SHIPS:
        localMatrix = placeShip(ship, localMatrix)

    return localMatrix

def placeShip(shipType, matrix):
    localMatrix = matrix
    placed = False
    canPlace = True
    matrixLimit = shipType[1][0]
    horiz = random.choice([True, False])
    row = 0
    col = 0
    #print(f"initiliazed variables for {shipType[0]}")



    while not placed:
        loopCount = 1
        if horiz:
            row = random.randint(0,7)
            col = random.randint(0, 7 - matrixLimit)
        else:
            row = random.randint(0, 7 - matrixLimit)
            col = random.randint(0,7)
        #print("Placing ships...")
        
        canPlace = True
        for i in range(matrixLimit):
            if horiz:
                if localMatrix[row][col + i] != '-':
                    canPlace = False
                    loopCount += 1
                    break
            else:
                if localMatrix[row + i][col] != '-':
                    canPlace = False
                    loopCount += 1
                    break
        if canPlace:
            for i in range(matrixLimit):
                if horiz:
                    localMatrix[row][col + i] = shipType[1][1]
                else:
                    localMatrix[row + i][col] = shipType[1][1]
            placed = True
            #print(f"Ship placed! ({shipType[0]})")
        #print(f"Trying to place ship: {shipType[0]}...")
        #print(f"Loop count: {loopCount}")
    return localMatrix

def displayBoard(board):
    print("  0 1 2 3 4 5 6 7")
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for i in range(len(board)):
        print(f"{columns[i]} {' '.join(board[i])}")

def promptCoordinates():
    validInput = False
    while not validInput:
        coordinates = input("Enter firing coordinates: ")
        if len(coordinates) == 2:
            row = coordinates[0].upper()
            col = coordinates[1]
            if row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] and col in ['0', '1', '2', '3', '4', '5', '6', '7']:
                validInput = True
                return (row, col)
        print("Invalid input. Please enter coordinates in the format 'A0', 'B3', etc.")

def fire(BOARD, SHIPS, hiddenBoard, coordinates):
    convertedRow = ord(coordinates[0]) - ord('A')
    convertedCol = int(coordinates[1])
    row = coordinates[0]
    col = coordinates[1]

    if BOARD[convertedRow][convertedCol] != '-':
        hiddenBoard[convertedRow][convertedCol] = 'X'
        if checkSunkShip(BOARD, SHIPS, hiddenBoard, convertedRow, convertedCol):
            if checkWin(BOARD, hiddenBoard):
                return hiddenBoard, "win", getShipName(SHIPS, BOARD[convertedRow][convertedCol])
            return hiddenBoard, "sunk", getShipName(SHIPS, BOARD[convertedRow][convertedCol])
        return hiddenBoard, "hit", None
    else:
        hiddenBoard[convertedRow][convertedCol] = 'O'
        return hiddenBoard, "miss", None

def checkWin(BOARD, hiddenBoard):
    for i in range(len(BOARD)):
        for j in range(len(BOARD[i])):
            if BOARD[i][j] != '-' and hiddenBoard[i][j] != 'X':
                return False
    return True

def checkSunkShip(BOARD, SHIPS, hiddenBoard, row, col):
    shipType = BOARD[row][col]
    for i in range(len(BOARD)):
        for j in range(len(BOARD[i])):
            if BOARD[i][j] == shipType and hiddenBoard[i][j] != 'X':
                return False
    print(f"You sunk a {getShipName(SHIPS, shipType)}!")
    return True

def getShipName(SHIPS, shipType):
    for ship in SHIPS:
        if ship[1][1] == shipType:
            return ship[0]

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()