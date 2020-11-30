<<<<<<< HEAD
import pygame


class Bars:
    def __init__(self, surface, x,y, height, bw, color):
        self.surface = surface
        self.x = x
        self.y = y
        self.HEIGHT = height
        self.BW = bw
        self.color = color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y - self.HEIGHT, self.BW, self.HEIGHT))
=======
import pygame


class Bars:
    def __init__(self, surface, x,y, height, bw, color):
        self.surface = surface
        self.x = x
        self.y = y
        self.HEIGHT = height
        self.BW = bw
        self.color = color

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y - self.HEIGHT, self.BW, self.HEIGHT))
>>>>>>> c1ed4a1235ddc8c2b9c710d75a8b811af5079aa2
