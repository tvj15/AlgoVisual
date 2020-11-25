import pygame
from Cell import Cell
from pygame_widgets import Button
import heapq
import math

class Grid:
    def __init__(self,surface,x, y, width, height, cw):
        self.surface = surface
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.CW = cw
        self.ROWS = self.HEIGHT//self.CW
        self.COLS = self.WIDTH//self.CW
        self.THICKNESS = 4
        self.buttons = self.generateButtons()
        self.grid = self.create_cells()
        self.drawMaze = False
        self.findPath = False
        self.drawPath = False
        self.isMaze = False
        self.start.start = True
        self.end.end = True

    def generateButtons(self):
        button = []
        # Create Maze Button
        button.append(Button(
            self.surface, self.x+(3*self.WIDTH)/4-100, self.y+self.HEIGHT+20, 200, 50, text='Generate Maze',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.generateMazeButtonOnClick
        ))

        # Clear Maze Button
        button.append(Button(
            self.surface, self.x+self.WIDTH/4-100, self.y+self.HEIGHT+20, 200, 50, text='Clear Maze',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.clearMazeButtonOnClick
        ))

        button.append(Button(
            self.surface, 100, self.y, 200, 50, text='Find Path',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.findPathOnClick
        ))
        return button

    # Create all Cell objects
    def create_cells(self):
        grid = []
        for j in range(self.ROWS):
            t = []
            for i in range(self.COLS):
                c = Cell(self.surface,i,j,i+(self.x/self.CW),j+(self.y/self.CW),self.CW)
                t.append(c)
            grid.append(t)
        self.start = grid[0][0]
        self.end = grid[-1][-1]
        self.isMaze = False
        return grid

    # Generate maze button onClick button
    def generateMazeButtonOnClick(self):
        if not self.drawMaze and not self.findPath and not self.drawPath:
            self.init_maze()
            self.drawMaze = True
    
    def clearMazeButtonOnClick(self):
        if not self.drawMaze and not self.findPath and not self.drawPath:
            self.grid = self.create_cells()
            self.start.start = True
            self.end.end = True
    
    def findPathOnClick(self):
        if not self.findPath and not self.drawMaze and not self.drawPath:
            self.init_dijkstra()
            self.findPath = True


    # Draw the grid on the screen
    def draw(self):
        # Drawing Border
        pygame.draw.rect(self.surface,(0,0,0),(self.x-self.THICKNESS/2,self.y-self.THICKNESS/2,self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS), self.THICKNESS)

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
        if self.findPath:
            if self.dijkstra_path_finder():
                self.findPath = False
        
        # For dijkstra path drawing
        if self.drawPath:
            if self.draw_path():
                self.drawPath = False


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
                heapq.heappush(self.unVisited, self.grid[i][j])

        self.start.dist = 0
        self.curr = self.start
        self.unVisited.remove(self.curr)

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
            self.shortest_path()
            self.drawPath = True
        print("Path found")
        return True

    def shortest_path(self):
        self.path = []
        curr = self.end
        while not curr.dist == 0:
            neighs = curr.neighbours(self.grid, self.isMaze)
            for n in neighs:
                if n.dist == curr.dist - 1:
                    self.path.append(n)
                    curr = n
                    break
    
    def draw_path(self):
        if len(self.path) > 0:
            self.path.pop(-1).path = True
            pygame.time.wait(20)
            return False
        print("Path drawn")
        return True

    #Grid event Handling
    def listen_events(self, events):
        for button in self.buttons:
            button.listen(events)
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[i][j].listen_events(events, self)


