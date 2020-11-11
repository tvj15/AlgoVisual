import pygame

class Cell:
    
    def  __init__(self, x, y, cw):
        self.x = x
        self.y = y
        self.CW = cw
        self.walls = [True, True, True, True]
        self.visited = False
        self.start = False
        self.end = False

    def draw(self, surface):
        pygame.draw.rect(surface,(200,200,200),(self.x*self.CW,self.y*self.CW,self.CW, self.CW))

        # TOP
        if self.walls[0]:
            pygame.draw.line(surface, (0,0,0), (self.x * self.CW, (self.y+1) * self.CW,), ((self.x+1) * self.CW, (self.y+1) * self.CW))
        #RIGHT
        if self.walls[1]:
            pygame.draw.line(surface, (0,0,0), ((self.x+1) * self.CW, self.y * self.CW),((self.x+1) * self.CW, (self.y+1) * self.CW))
            
        # BOTTOM
        if self.walls[2]:
            pygame.draw.line(surface, (0,0,0), (self.x * self.CW, self.y * self.CW), ((self.x+1) * self.CW, self.y * self.CW))

        # LEFT
        if self.walls[3]:
            pygame.draw.line(surface, (0,0,0), (self.x * self.CW, self.y * self.CW), (self.x * self.CW, (self.y+1) * self.CW))