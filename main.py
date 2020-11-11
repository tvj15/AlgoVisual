import pygame
from pygame.locals import *
import os 
from Grid import Grid
from pygame_widgets import Button

class AlgoVisual:
    def __init__(self, display):
        self.DISPLAY = display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("AlgoVisual")
        self.grid = Grid(600, 100, 500, 500, 50)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        break

            self.screen.fill((180,210,230))

            self.draw()

            pygame.display.flip()

        pygame.quit()
    
    def draw(self):
        
        self.grid.draw(self.screen)

if __name__ == "__main__":
    a = AlgoVisual((1200, 700))
    a.run()