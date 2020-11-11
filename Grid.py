import pygame
from Cell import Cell

class Grid:
    def __init__(self,x,y, width, height, cw):
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.CW = cw
        self.ROWS = self.HEIGHT//self.CW
        self.COLS = self.WIDTH//self.CW
        self.grid = self.create_cells()
        self.THICKNESS = 4

    def create_cells(self):
        grid = []
        for i in range(self.ROWS):
            t = []
            for j in range(self.COLS):
                c = Cell(j+(self.x/self.CW),i+(self.y/self.CW),self.CW)
                t.append(c)
            grid.append(t)
        return grid

    def draw(self, surface):
        pygame.draw.rect(surface,(0,0,0),(self.x-self.THICKNESS/2,self.y-self.THICKNESS/2,self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS), self.THICKNESS)

        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.grid[j][i].draw(surface)

    # def generate_maze(self, )

    


