import pygame
from Cell import Cell
from pygame_widgets import Button, Slider
import heapq
import math

class Grid:
    def __init__(self,mainObj,x, y, width, height, cw):
        self.mainObj = mainObj
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.CW = cw
        self.ROWS = self.HEIGHT//self.CW
        self.COLS = self.WIDTH//self.CW
        self.THICKNESS = 4
        self.buttons = self.generateButtons()
        self.generateSlider()        
        self.grid = self.create_cells()
        self.drawMaze = False
        self.dijkstraFindPath = False
        self.aStarFindPath = False
        self.drawPath = False
        self.isMaze = False
        
        

    def generateSlider(self):
        self.slider = Slider(self.mainObj.surface, self.x + 5 , self.y+self.HEIGHT+20, 200,10, min=10, max=100, step=5,initial=self.CW, colour=(180, 110, 205))

     # Draw the grid on the screen
    def draw(self):
        # Drawing Border
        pygame.draw.rect(self.mainObj.surface,(0,0,0),(self.x-self.THICKNESS/2,self.y-self.THICKNESS/2,self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS), self.THICKNESS)


        # Drawing Cells
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[i][j].draw()

        # Buttons
        for button in self.buttons:
            button.draw()

        # For Maze Generation
        if self.drawMaze:
            if self.generate_maze():
                self.drawMaze = False
        
        # For dijkstra path finding
        if self.dijkstraFindPath:
            if self.dijkstra_path_finder():
                self.dijkstraFindPath = False
        
        if self.aStarFindPath:
            if self.aStar_path_finder():
                self.aStarFindPath = False
        
        # For  path drawing
        if self.drawPath:
            if self.draw_path():
                self.drawPath = False

        self.slider.draw()
        
    
    def generateButtons(self):
        button = []
        # Create Maze Button
        button.append(Button(
            self.mainObj.surface, self.x+(3*self.WIDTH)/4-100, self.y+self.HEIGHT+50, 200, 50, text='Generate Maze',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.generateMazeButtonOnClick
        ))

        # Clear Maze Button
        button.append(Button(
            self.mainObj.surface, self.x+self.WIDTH/4-100, self.y+self.HEIGHT+50, 200, 50, text='Clear Maze',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.clearMazeButtonOnClick
        ))

        button.append(Button(
            self.mainObj.surface, 100, self.y, 200, 50, text='Find Dijkstra Path',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.findDijkstraPathOnClick
        ))
        button.append(Button(
            self.mainObj.surface, 100, self.y+100, 200, 50, text='Find A* Path',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.findAStarPathOnClick
        ))

        button.append(Button(
            self.mainObj.surface, 100, self.y+400, 200, 50, text='Back',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.backButtonOnClick
        ))

        return button

    # Create all Cell objects
    def create_cells(self):
        self.ROWS = self.HEIGHT//self.CW
        self.COLS = self.WIDTH//self.CW
        self.start = None
        self.end = None
        grid = []
        for j in range(self.ROWS):
            t = []
            for i in range(self.COLS):
                c = Cell(self.mainObj.surface,i,j,i+(self.x/self.CW),j+(self.y/self.CW),self.CW)
                t.append(c)
            grid.append(t)
        self.start = grid[0][0]
        self.end = grid[-1][-1]
        self.start.start = True
        self.end.end = True
        self.isMaze = False
        return grid

    def isClickAllowed(self):
        if not self.drawMaze and not self.dijkstraFindPath and not self.drawPath and not self.aStarFindPath:
            return True
        return False

    # Generate maze button onClick button
    def generateMazeButtonOnClick(self):
        if self.isClickAllowed():
            self.init_maze()
            self.drawMaze = True
    
    def clearMazeButtonOnClick(self):
        if self.isClickAllowed():
            self.grid = self.create_cells()
    
    def findDijkstraPathOnClick(self):
        if self.isClickAllowed():
            self.init_dijkstra()
            self.dijkstraFindPath = True

    def findAStarPathOnClick(self):
        if self.isClickAllowed():
            self.init_aStar()
            self.aStarFindPath = True

    def backButtonOnClick(self):
        if self.isClickAllowed():
            self.mainObj.sorter = False
            self.mainObj.pathfinder = False


    #Init the maze/grid to original
    def init_maze(self):
        self.grid = self.create_cells()
        self.start.start = True
        self.end.end = True
        self.stack = []
        self.current = self.grid[0][0]
        self.current.visited = True
        self.stack.append(self.current)

    # Generate maze using recursive backtracking algorithm
    def generate_maze(self):
        if len(self.stack) > 0:
            self.current = self.stack.pop(-1)
            self.current.highlight()
            nextCell = self.current.getNeighbour(self.grid)
            if nextCell:
                self.stack.append(self.current)
                Cell.removeWall(self.current, nextCell)
                nextCell.visited = True
                self.stack.append(nextCell)
            # pygame.time.wait(20)
            return False
        print("Maze Generated")
        self.isMaze = True
        return True
                       
    #Init the maze/grid for dijkstra
    def init_dijkstra(self):
        self.unVisited = []
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[i][j].dist = math.inf
                self.grid[i][j].dijkstraVisited = False
                self.grid[i][j].path = False
                self.unVisited.append(self.grid[i][j])

        self.start.dist = 0
        self.curr = self.start
        self.unVisited.remove(self.curr)
        heapq.heapify(self.unVisited)
        

    # Dijkstra path finding algorithm
    def dijkstra_path_finder(self):
        if len(self.unVisited) > 0 and not self.curr == self.end:
            neighs = self.curr.neighbours(self.grid, self.isMaze)
            if neighs:
                for n in neighs:
                    if n in self.unVisited:
                        n.highlight()
                        t = self.curr.dist + 1
                        if n.dist > t:
                            n.dist = t
                heapq.heapify(self.unVisited)
                self.curr = heapq.heappop(self.unVisited)
                self.curr.dijkstraVisited = True
            else:
                print('No neighbour found')
                return True

            pygame.time.wait(20)
            return False
        if not self.drawPath:
            self.shortest_path("dijkstra")
            self.drawPath = True
        print("Path found")
        return True

    def init_aStar(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[i][j].g = math.inf
                self.grid[i][j].dist = math.inf
                self.dijkstraVisited = False
        self.open_list = [self.start]
        self.start.came_from = None
        self.start.g = 0
        self.start.dist=self.compute_score(self.start, self.end)
        self.curr = self.start

    def aStar_path_finder(self):
        if len(self.open_list) > 0 and not self.curr == self.end:
            self.curr = heapq.heappop(self.open_list)
            self.curr.close = True
            neighs = self.curr.neighbours(self.grid, self.isMaze)
            if neighs:
                for n in neighs:
                    temp_score = self.curr.g + self.compute_score(self.curr,n)
                    if temp_score < n.g:
                        n.came_from = self.curr
                        n.g = temp_score
                        n.dist = n.g + self.compute_score(n, self.end)
                        if n not in self.open_list:
                            n.highlight()
                            heapq.heappush(self.open_list,n)
                            n.open = True
            else:
                print('No neighbour found')
                return True
            pygame.time.wait(20)
            return False
        if not self.drawPath:
            self.shortest_path("astar")
            self.drawPath = True
        print("Path found")
        return True


    def compute_score(self, cell,other):
        return (abs(cell.idx - other.idx) + abs(cell.idy - other.idy))

    def shortest_path(self,algo):
        if algo == "dijkstra":
            self.path = []
            curr = self.end
            while not curr.dist == 0:
                neighs = curr.neighbours(self.grid, self.isMaze)
                for n in neighs:
                    if n.dist == curr.dist - 1:
                        self.path.append(n)
                        curr = n
                        break
        elif algo == "astar":
            self.path = [self.curr]
            while self.curr.came_from:
                self.curr = self.curr.came_from
                self.path.append(self.curr)
    
    def draw_path(self):
        if len(self.path) > 0:
            self.path.pop(-1).path = True
            pygame.time.wait(20)
            return False
        print("Path drawn")
        return True

    #Grid event Handling
    def listen_events(self, events):
        if self.isClickAllowed():
            self.slider.listen(events)
            temp = self.slider.getValue()
            if temp != self.CW and temp in [10,20,25,50,100]:
                self.CW = temp
                self.grid = self.create_cells()
        for button in self.buttons:
            button.listen(events)
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[i][j].listen_events(events, self)
