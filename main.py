from tkinter import *
import tkinter.messagebox

gridSize = 16                           # define the dimensions of the grid
noOfSquares = gridSize * gridSize       # overall number of squares in the grid
squareSize = 32                         # define the size of individual squares
borderSize = 30                         # define the border size between canvas and main window
canvasBorder = 3                        # border at the edge of the canvas, to properly align grid lines
lineLength = gridSize * squareSize + canvasBorder
gridLength = lineLength - 2
windowSize = gridLength + (2 * borderSize)
winSizeString = str(windowSize) + "x" + str(windowSize+80)
margin = 1                              # margin between squares and gridlines
green = "#77ff77"
darkGreen = "#00cc44"
darkCyan = "#00aaff"
orange = "#ffaa44"

squareList = []                                         # list to store GUI squares
blockList = [0] * noOfSquares                   # list of blocks: 1 = block, 0 = empty space
pointList = [x for x in range(noOfSquares)]     # pointList with 1-D indexing (defined using a comprehension)

pointInfoList = [[0,0,0,0]] * noOfSquares   # List to store each point's info
# pointInfoList's index and data value:
# 0: f value
# 1: g value
# 2: h value
# 3: point's parent node

solving, solved = False, False
startPoint, endPoint = pointList[0], pointList[noOfSquares - 1]
endPointX, endPointY = endPoint % gridSize, int(endPoint / gridSize)
openList, closedList = [], []

lClick = False
rClick = False
mouseX, mouseY = 0, 0

inputTypes = ["Block", "Start Point", "End Point"]
inputTypeSelection = "Block"

# Functionz....

def leftClick(event):
    global lClick
    lClick = True
def leftClickRelease(event):
    global lClick
    lClick = False
def rightClick(event):
    global rClick
    rClick = True
def rightClickRelease(event):
    global rClick
    rClick = False

def motion(event):
    # keeps track of where the mouse pointer is
    global mouseX, mouseY
    mouseX, mouseY = event.x, event.y

def getSquareCoords(squareX, squareY):
    topLeftX = (squareX * squareSize) + margin + canvasBorder
    topLeftY = (squareY * squareSize) + margin + canvasBorder
    bottomRightX = topLeftX + squareSize - 2 * margin
    bottomRightY = topLeftY + squareSize - 2 * margin
    return topLeftX, topLeftY, bottomRightX, bottomRightY

def solve():
    global solving, solved, startPoint, endPoint, endPointX, endPointY, openList, closedList, pointInfoList
    if not solved:
        solving, solved = True, False
        openList, closedList = [startPoint], []
        pointInfoList[startPoint][3] = startPoint   # sets the startPoint's parent node to itself
        endPointX, endPointY = endPoint % gridSize, int(endPoint / gridSize)    # sets the endPoint's X and Y coords

def reset():
    global solving, solved, openList, closedList
    solving, solved = False, False
    openList, closedList = [], []
    for i in range(noOfSquares):
        if blockList[i] == 0:
            mainGrid.itemconfig(squareList[i], fill="white", outline="white")

def clear():
    global solving, solved, openList, closedList
    solving, solved = False, False
    openList, closedList = [], []
    for i in range(noOfSquares):
        blockList[i] = 0
        mainGrid.itemconfig(squareList[i], fill="white", outline="white")

def changeInputType():
    global inputTypeSelection
    inputTypeSelection = inputTypes[x.get()]

# -----------------------------------------------------------

window = Tk()
window.title("A* Path Finder")
window.geometry(winSizeString)

# Create main grid
mainGrid = Canvas(window, width=gridLength, height=gridLength, bg="white")
mainGrid.pack(pady=20, side=TOP)
mainGrid.bind("<ButtonPress-1>", leftClick)                     # left mouse click
mainGrid.bind("<ButtonRelease-1>", leftClickRelease)            # left mouse release
mainGrid.bind("<ButtonPress-2>", rightClick)                    # right mouse click
mainGrid.bind("<ButtonRelease-2>", rightClickRelease)           # right mouse release
mainGrid.bind("<Motion>", motion)

# Draw grid
for i in range(gridSize + 1):
    lineCo = i * squareSize + canvasBorder
    mainGrid.create_line(lineCo, canvasBorder, lineCo, lineLength)
    mainGrid.create_line(canvasBorder, lineCo, lineLength, lineCo)

# Create squares and start/end circles
for i in range(noOfSquares):
    squareX = i % gridSize
    squareY = int(i / gridSize)
    index = (squareY * gridSize) + squareX
    topLeftX, topLeftY, bottomRightX, bottomRightY = getSquareCoords(squareX, squareY)
    newSquare = mainGrid.create_rectangle(topLeftX,topLeftY,bottomRightX,bottomRightY, fill="white", outline="white")
    squareList.append(newSquare)
startX, startY = startPoint % gridSize, int(startPoint / gridSize)
topLeftX, topLeftY, bottomRightX, bottomRightY = getSquareCoords(startX, startY)
startCircle = mainGrid.create_oval(topLeftX,topLeftY,bottomRightX,bottomRightY, fill=green, outline="black")
endX, endY = endPoint % gridSize, int(endPoint / gridSize)
topLeftX, topLeftY, bottomRightX, bottomRightY = getSquareCoords(endX, endY)
endCircle = mainGrid.create_oval(topLeftX,topLeftY,bottomRightX,bottomRightY, fill="cyan", outline="black")

# Create GUI buttons
buttonFrame = Frame(window)
buttonFrame.pack(side=LEFT, padx=30)
solveButton = Button(buttonFrame, text="Solve", command=solve)
solveButton.grid(row=0, column=0)
resetButton = Button(buttonFrame, text="Reset", command=reset)
resetButton.grid(row=0, column=1)
clearButton = Button(buttonFrame, text="Clear", command=clear)
clearButton.grid(row=0, column=2)
# Create GUI radio buttons
rButtonFrame = Frame(window)
rButtonFrame.pack(side=LEFT, padx=10)
x = IntVar()
for i in range(len(inputTypes)):
    inputSelect = Radiobutton(rButtonFrame, text=inputTypes[i], variable=x,
                              justify=LEFT, value=i, command=changeInputType)
    inputSelect.pack(side=LEFT)


# Main loop
while True:
    # Highlight startPoint or endPoint if they're selected in the radio buttons menu
    if inputTypeSelection == "Start Point":
        mainGrid.itemconfig(startCircle, fill=green)
        mainGrid.itemconfig(endCircle, fill=darkCyan)
    elif inputTypeSelection == "End Point":
        mainGrid.itemconfig(endCircle, fill="cyan")
        mainGrid.itemconfig(startCircle, fill=darkGreen)
    else:
        mainGrid.itemconfig(endCircle, fill=darkCyan)
        mainGrid.itemconfig(startCircle, fill=darkGreen)
    # Draw blocks
    if (lClick or rClick) and not solving and not solved and inputTypeSelection == "Block":
        # Get the square's X and Y coordinates and clip them within the bounds
        squareX = int(mouseX / squareSize)
        squareX = min(squareX, gridSize - 1)
        squareX = max(squareX, 0)
        squareY = int(mouseY / squareSize)
        squareY = min(squareY, gridSize - 1)
        squareY = max(squareY, 0)
        index = (squareY * gridSize) + squareX
        if index not in (startPoint, endPoint):         # prevent blocks being drawn on the start or end points
            if lClick:
                blockList[index] = 1
                colour = "black"
            if rClick:
                blockList[index] = 0
                colour = "white"
            index = min((squareY * gridSize) + squareX, len(squareList) - 1)       # min function prevents index going out of range
            mainGrid.itemconfig(squareList[index], fill=colour, outline=colour)
    # Move startPoint
    elif lClick and not solving and not solved and inputTypeSelection == "Start Point":
        squareX = int(mouseX / squareSize)
        squareX = min(squareX, gridSize-1)
        squareX = max(squareX, 0)
        squareY = int(mouseY / squareSize)
        squareY = min(squareY, gridSize - 1)
        squareY = max(squareY, 0)
        index = (squareY * gridSize) + squareX
        if blockList[index] == 0 and index != endPoint:     # prevent startPoint being moved to a block or the endPoint
            startPoint = pointList[index]
            topLeftX, topLeftY, bottomRightX, bottomRightY = getSquareCoords(squareX, squareY)
            mainGrid.coords(startCircle, topLeftX, topLeftY, bottomRightX, bottomRightY)
    # Move endPoint
    elif lClick and not solving and not solved and inputTypeSelection == "End Point":
        squareX = int(mouseX / squareSize)
        squareX = min(squareX, gridSize-1)
        squareX = max(squareX, 0)
        squareY = int(mouseY / squareSize)
        squareY = min(squareY, gridSize - 1)
        squareY = max(squareY, 0)
        index = (squareY * gridSize) + squareX
        if blockList[index] == 0 and index != startPoint:   # prevent endPoint being moved to a block or the startPoint
            endPoint = pointList[index]
            topLeftX, topLeftY, bottomRightX, bottomRightY = getSquareCoords(squareX, squareY)
            mainGrid.coords(endCircle, topLeftX, topLeftY, bottomRightX, bottomRightY)

    # Solve algorithm
    if solving and not solved:
        # If all possible paths have been exhausted:
        if len(openList) == 0:
            tkinter.messagebox.showinfo("", "No possible path could be found.")
            solved = True
        # A* algorithm starts here:
        while len(openList) > 0:
            # Draw openList squares in orange and closedList ones in yellow
            for node in openList:
                mainGrid.itemconfig(squareList[node], fill=orange, outline=orange)
            for node in closedList:
                mainGrid.itemconfig(squareList[node], fill="yellow", outline="yellow")
            # Get minimum f value from openList nodes
            popIdx = 0                                  # sets the pop index to the start of the openList
            minF = pointInfoList[openList[0]][0]        # sets the minimum f value to that of the first node in the openList
            for i in range(len(openList)):
                currentF = pointInfoList[openList[i]][0]
                if currentF < minF:
                    minF = currentF
                    popIdx = i
            currentNode = openList.pop(popIdx)
            closedList.append(currentNode)
            # Draw main path in red
            drawingPath = True
            path = [currentNode]
            i = 0
            while drawingPath:
                nextSquare = pointInfoList[path[i]][3]
                path.append(nextSquare)
                if nextSquare == startPoint:
                    drawingPath = False
                i += 1
            for square in path:
                mainGrid.itemconfig(squareList[square], fill="red", outline="red")
            # If the current node is the end node, then the algorithm has been solved
            if currentNode == endPoint:
                solving, solved = False, True
                mainGrid.itemconfig(squareList[endPoint], fill="red", outline="red")
                window.update()         # colour the final square red before the pop-up message appears
                tkinter.messagebox.showinfo("", "A path has been found!")
                break
            # Get the children of the current node
            xCo = currentNode % gridSize
            yCo = int(currentNode / gridSize)
            children = []
            if yCo > 0:
                children.append(currentNode - gridSize)
                # if xCo > 0:                                           # greyed-out code allows diagonal movement
                #     children.append(currentNode - gridSize - 1)
                # if xCo < gridSize:
                #     children.append(currentNode - gridSize + 1)
            if yCo < gridSize - 1:
                children.append(currentNode + gridSize)
                # if xCo > 0:
                #     children.append(currentNode + gridSize - 1)
                # if xCo < gridSize:
                #     children.append(currentNode + gridSize + 1)
            if xCo > 0:
                children.append(currentNode - 1)
            if xCo < gridSize - 1:
                children.append(currentNode + 1)
            print("children = " + str(children))
            # Process each child in children list
            for child in children:
                if child in closedList:                 # skip the rest of the loop if child is already in closedList
                    continue
                if blockList[child] == 1:               # skip the rest of the loop if child is a solid block
                    continue
                childX = child % gridSize
                childY = int(child / gridSize)
                childG = 1                  # distance from child to parent node (same value for all four directions)
                xDist, yDist = (endPointX - childX) ** 2, (endPointY - childY) ** 2
                childH = (xDist + yDist) ** 0.5     # distance from child to destination node
                childF = childG + childH
                if child in openList:
                    if childG > pointInfoList[child][1]:
                        continue
                    else:
                        openList.remove(child)
                openList.append(child)
                pointInfoList[child] = [childF, childG, childH, currentNode]

            for i in range(1000000):    # screen refresh timer
                pass
            window.update()

    while solved:
        window.update()
        pass

    window.update()

window.mainloop()