import pygame
import random
import math

class Cell:
    drag = False
    currDrag = None
    currDraging = None

    def  __init__(self, surface,idx,idy, x, y, cw):
        self.surface = surface
        self.x = x
        self.y = y
        self.idx = idx
        self.idy = idy
        self.CW = cw
        self.walls = [True, True, True, True]
        self.visited = False
        self.start = False
        self.end = False
        self.dijkstraVisited = False
        self.path = False
        self.open = False
        self.close = False

    def __lt__(self, other):
        return self.dist < other.dist
        

    #Drawing Cells
    def draw(self):
        if self.start:
            pygame.draw.rect(self.surface,(255,0,0),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.end:
            pygame.draw.rect(self.surface,(0,0,255),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.path:
            pygame.draw.rect(self.surface,(255,255,0),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.dijkstraVisited:
            pygame.draw.rect(self.surface,(100,(255-self.dist-2)%255,200),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.close:
            pygame.draw.rect(self.surface,(255,165,0),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.open:
            pygame.draw.rect(self.surface,(0,255,0),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))
        elif self.visited:
            pygame.draw.rect(self.surface,(200,200,200),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))


        # TOP
        if self.walls[0]:
            pygame.draw.line(self.surface, (0,0,0), (self.x * self.CW, (self.y+1) * self.CW,), ((self.x+1) * self.CW, (self.y+1) * self.CW))
        #RIGHT
        if self.walls[1]:
            pygame.draw.line(self.surface, (0,0,0), ((self.x+1) * self.CW, self.y * self.CW),((self.x+1) * self.CW, (self.y+1) * self.CW))
            
        # BOTTOM
        if self.walls[2]:
            pygame.draw.line(self.surface, (0,0,0), (self.x * self.CW, self.y * self.CW), ((self.x+1) * self.CW, self.y * self.CW))

        # LEFT
        if self.walls[3]:
            pygame.draw.line(self.surface, (0,0,0), (self.x * self.CW, self.y * self.CW), (self.x * self.CW, (self.y+1) * self.CW))
        
    
    #Highlighting cells
    def highlight(self):
        pygame.draw.rect(self.surface, (255,255,0), (self.x*self.CW, self.y*self.CW, self.CW, self.CW))
    
    # Getting cell neighbours for maze
    def getNeighbour(self, grid):
        n = []     
        top = Cell.checkNeighbour(self.idx, self.idy+1, grid)
        right = Cell.checkNeighbour(self.idx+1, self.idy, grid)
        bottom = Cell.checkNeighbour(self.idx, self.idy-1, grid)
        left = Cell.checkNeighbour(self.idx-1, self.idy, grid)

        if top and not top.visited:
            n.append(top)
        if right and not right.visited:
            n.append(right)
        if bottom and not bottom.visited:
            n.append(bottom)
        if left and not left.visited:
            n.append(left)

        if len(n) > 0:
            t = random.choice(n)
            return t
        else:
            return None
    
    # Checking neighbours validity
    @staticmethod
    def checkNeighbour(x,y, grid):
        rows = len(grid)
        cols = len(grid[0])
        if (x < 0 or y < 0 or x > cols-1 or y > rows-1):
            return None
        return grid[y][x]

    #Neighbours function for dijkstra
    def neighbours(self, grid, isMaze):
        n = []     
        top = Cell.checkNeighbour(self.idx, self.idy+1, grid)
        right = Cell.checkNeighbour(self.idx+1, self.idy, grid)
        bottom = Cell.checkNeighbour(self.idx, self.idy-1, grid)
        left = Cell.checkNeighbour(self.idx-1, self.idy, grid)
        if top and not (isMaze and self.walls[0]):
            n.append(top)
        if right and not (isMaze and self.walls[1]):
            n.append(right)
        if bottom and not (isMaze and self.walls[2]):
            n.append(bottom)
        if left and not (isMaze and self.walls[3]):
            n.append(left)

        if len(n) > 0:
            n.sort()
            return n
        else:
            return None
    
    #Remove wall
    def removeWall(self, other):
        dx = self.idx - other.idx
        dy = self.idy - other.idy
        if dx == -1:
            self.walls[1] = False
            other.walls[3] = False
        elif dx == 1:
            self.walls[3] = False
            other.walls[1] = False
        if dy == -1:
            self.walls[0] = False
            other.walls[2] = False
        elif dy == 1:
            self.walls[2] = False
            other.walls[0] = False
    
    #Cell event handler
    def listen_events(self,events, gridObj):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if self.x * self.CW < event.pos[0] < (self.x+1) * self.CW and self.y * self.CW < event.pos[1] < (self.y + 1) * self.CW:
                    if self.start == True:
                        Cell.currDraging = "start"
                        Cell.drag = True
                        Cell.currDrag = self
                    elif self.end == True:
                        Cell.currDraging = "end"
                        Cell.drag = True
                        Cell.currDrag = self
                    
            if event.type == pygame.MOUSEMOTION:
                if self.x * self.CW < event.pos[0] < (self.x+1) * self.CW and self.y * self.CW < event.pos[1] < (self.y + 1) * self.CW:
                    if Cell.drag and gridObj.isClickAllowed():
                        if not self == Cell.currDrag:
                            if Cell.currDraging == "start":
                                if not self.end:
                                    self.start = True
                                    Cell.currDrag.start = False
                                    Cell.currDrag = self
                                    gridObj.start = self

                            elif Cell.currDraging == "end":
                                if not self.start:
                                    self.end = True
                                    Cell.currDrag.end = False
                                    Cell.currDrag = self
                                    gridObj.end = self


            if event.type == pygame.MOUSEBUTTONUP:
                if self.x * self.CW < event.pos[0] < (self.x+1) * self.CW and self.y * self.CW < event.pos[1] < (self.y + 1) * self.CW:
                    Cell.drag = False
                    Cell.currDrag = None
                    currDraging = None
