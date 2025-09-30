# A* Pathfinder

A simple GUI-based implementation of the famous A* path-finding algorithm written in **Python (Tkinter).**

---

##  About

This project was one of many little projects I wrote while teaching myself Python from scratch.  

Code 100% my own, which I wrote based off an entirely verbal, step-by-step description of the algorithm.

No AI was used.

---

## How to Use

Wall blocks are depicted as black squares. The start point of the path is a green circle, the end point is a blue circle. The main path is represented by red squares, with orange squares representing unexplored possibilities, and yellow squares representing exhausted possibilities.

- The 3 radio buttons in the bottom right corner allow you to add/remove wall blocks on the grid, and move the start and end points of the path
- **Left mouse button**
	- **Block** radio button selected: Drag while holding to add wall blocks to the grid
	- **Start Point** radio button selected: Drag to move the start point of the path
	- **End Point** radio button selected: Drag to move the end point of the path
- **Right mouse button**
	- **Block** radio button selected: Drag while holding to remove wall blocks from the grid
- **'Solve' button on the GUI** — Run the algorithm, finding a path between the start and end points
- **'Reset' button on the GUI** — Reset the grid after having run the algorithm, leaving the walls in place
- **'Clear' button on the GUI** — Clear the entire grid except for the start and end points

---

## 💻 Running the program

- Open the `main.py` file in [PyCharm](https://www.jetbrains.com/pycharm/)  
- Click **Run ▶** to start the game  
- ✅ Uses only Python’s standard library (`tkinter`) — no external installations needed

