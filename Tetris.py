from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 55
    app.boardTop = 50
    app.boardWidth = 300
    app.boardHeight = 400
    app.cellBorderWidth = 2
    restart(app)
    app.stepsPerSecond=3
    
    
def restart(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    loadPiece(app,0)
    app.piece = app.tetrisPieces[0]
    app.pieceColor = app.tetrisPieceColors[0]
    app.pieceTopRow = 0
    app.pieceLeftCol = app.cols//2-len(app.piece)//2
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    loadNextPiece(app)
    app.score = 0
    app.isGameOver = False
    app.isPaused =False
def redrawAll(app):
    drawLabel('Tetris', 65, 30, size=16)
    drawLabel('Your current score is: '+str(app.score),280,30,size=16)
    drawBoard(app)
    drawPiece(app)
    drawBoardBorder(app)
    if app.isGameOver:
        drawLabel('Game Over',200,150,size=30,fill='red',bold=True)
        drawLabel('Your Score is '+str(app.score),200,200,size=30,fill='red',bold=True)
        drawLabel('Press r to restart the game!',200,250,size=30,fill='red',bold=True)
        

    

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col,app.board[row][col])

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col,color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def resizeBoard(app, numRows, numCols, boardSize):
    app.rows = numRows
    app.cols = numCols
    app.boardLeft, app.boardWidth, app.boardHeight = boardSize
    app.board = [([None] * app.cols) for row in range(app.rows)]
    
def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

def onKeyPress(app,key):
    if '0'<=key<='6':
        loadPiece(app,int(key))
    if key == 'left':
        movePiece(app,0,-1)
    elif key == 'right':
        movePiece(app,0,1)
    elif key == 'down':
        movePiece(app,1,0)
    elif key == 'up':
        rotatePieceClockwise(app)
    elif key == 'space':
        hardDropPiece(app)
    elif key == 's':
        takeStep(app)
    elif key in ['a','b','c','d','e','f','g','h']:
        loadTestBoard(app, key)
    elif key == 'p':
        app.isPaused = not app.isPaused
    elif key == 'r':
        restart(app)
        
        
def loadTestBoard(app, key):
    # DO NOT EDIT THIS FUNCTION
    # We are providing you with this function to set up the board
    # with some test cases for clearing the rows.
    # To use this: press 'a', 'b', through 'h' to select a test board.
    # Then press 'space' for a hard drop of the red I,
    # and then press 's' to step, which in most cases will result
    # in some full rows being cleared.

    # 1. Clear the board and load the red I piece 
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.nextPieceIndex = 0
    loadNextPiece(app)
    # 2. Move and rotate the I piece so it is vertical, in the
    #    top-left corner
    for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
        onKeyPress(app, keyName)
    # 3. Add a column of alternating plum and lavender cells down
    #    the rightmost column
    for row in range(app.rows):
        app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
    # 4. Now almost fill some of the bottom rows, leaving just the
    #    leftmost column empty
    indexesFromBottom = [ [ ], [0], [0,1], [0,1,2], [0,2],
                          [1,2,3], [1,2,4], [0,2,3,5] ]
    colors = ['moccasin', 'aqua', 'khaki', 'aquamarine',
              'darkKhaki', 'peachPuff']
    for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
        row = app.rows - 1 - indexFromBottom
        color = colors[indexFromBottom]
        for col in range(1, app.cols):
            app.board[row][col] = color

def loadPiece(app,pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceTopRow = 0
    app.pieceLeftCol = math.floor(app.cols/2-len(app.piece[0])/2)
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    
def drawPiece(app):
    limitedCol = app.pieceLeftCol+len(app.piece[0])
    limitedRow = app.pieceTopRow+len(app.piece)
    for i in range(app.pieceTopRow,limitedRow):
        for j in range(app.pieceLeftCol,limitedCol):
            if app.piece[i-app.pieceTopRow][j-app.pieceLeftCol]:
                drawCell(app,i,j,app.pieceColor)

def movePiece(app,drow,dcol):
    app.pieceLeftCol+=dcol
    app.pieceTopRow+=drow
    if ((app.pieceLeftCol < 0) or ((app.pieceLeftCol+len(app.piece[0]))>app.cols)):
        app.pieceLeftCol-=dcol
        return False
    elif ((app.pieceTopRow<0) or ((app.pieceTopRow+len(app.piece))>app.rows)):
        app.pieceTopRow-=drow
        return False
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j]:
                boardRow = app.pieceTopRow+i
                boardCol = app.pieceLeftCol+j
                if app.board[boardRow][boardCol] is not None:
                    app.pieceTopRow-=drow
                    app.pieceLeftCol-=dcol
                    return False
    return True

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
    
def rotatePieceClockwise(app):
    oldRows, oldCols = len(app.piece), len(app.piece[0])
    newRows, newCols = oldCols, oldRows
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    centerRow = oldTopRow + oldRows//2
    app.pieceTopRow = centerRow - newRows//2
    centerCol = oldLeftCol + oldCols//2
    app.pieceLeftCol = centerCol - newCols//2
    app.piece = rotate2dListClockwise(app.piece)
    if ((app.pieceLeftCol < 0) or ((app.pieceLeftCol+len(app.piece[0]))>app.cols)):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
    elif ((app.pieceTopRow<0) or ((app.pieceTopRow+len(app.piece))>app.rows)):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol
    centerRow = oldTopRow + oldRows//2
    
def rotate2dListClockwise(L):
    oldRows, oldCols = len(L), len(L[0])
    newRows, newCols = oldCols, oldRows
    res = [['']*newCols for _ in range(newRows)]
    for oldRow in range(oldRows):
        for oldCol in range(oldCols):
            newRow=oldCol
            newCol=oldRows-1-oldRow
            res[newRow][newCol]=L[oldRow][oldCol]
    return res



def takeStep(app):
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        if isGameOver(app):
            app.isGameOver = True
        else:
            loadNextPiece(app)
        removeFullRows(app)
        
        
   
def loadNextPiece(app):
    loadPiece(app, app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))
    
    
def placePieceOnBoard(app):
    for i in range(len(app.piece)):
        for j in range(len(app.piece[0])):
            if app.piece[i][j]:
                boardRow = app.pieceTopRow+i
                boardCol = app.pieceLeftCol+j
                if (0<=boardRow < app.rows)and (0<=boardCol<app.cols):
                    app.board[boardRow][boardCol] = app.pieceColor
                    
def removeFullRows(app):
    score = 0
    numOfPoped = 0
    numOfTrue=0
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col]!=None:
                numOfTrue+=1
                if numOfTrue == app.cols:
                    app.board.pop(row)
                    app.board.insert(0,[None]*app.cols)
                    numOfPoped +=1
        numOfTrue=0
    score = numOfPoped**2 
    app.score+=score
def onStep(app):
    if not app.isPaused:
        takeStep(app)

def isGameOver(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if (app.board[row][col] is not None) and row<1:
                return True
    return False
def main():
    # app = runApp()
    runApp()
    
main()
