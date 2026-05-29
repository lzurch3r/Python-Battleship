import random

def main():
    board = buildBoard()
    displayBoard(board)

def buildBoard():
    boardMatrix = [['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-'],
                   ['-', '-', '-', '-', '-', '-', '-', '-']]
    
    board1 = randomizeBoard(boardMatrix)

    return board1

def randomizeBoard(matrix):
    localMatrix = matrix
    ships = [("carrier",    (5, 'C')),  #Carrier
             ("battleship", (4, 'B')),  #Battleship
             ("cruiser",    (3, 'R')),  #Cruiser
             ("submarine",  (2, 'S')),  #Submarine
             ("destroyer",  (2, 'D'))]  #Destroyer


    for ship in ships:
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

main()