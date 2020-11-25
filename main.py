import pygame
from pygame.locals import *
import os 
from Grid import Grid
from BarsContainer import BarsContainer

class AlgoVisual:
    def __init__(self, display):
        self.DISPLAY = display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("AlgoVisual")
        # self.grid = Grid(self.screen, 600, 100, 500, 500, 20)
        self.container = BarsContainer(self.screen, 400, 100, 700, 500, 20)
        

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                        break
                    if event.key == K_RETURN:
                        for bar in self.container.bars:
                            print("(",bar.x, bar.HEIGHT,")", end="" )
                        print()
                        print("-------------------------------------------")

            self.container.listen_events(events)

            self.screen.fill((180,210,230))
            
            self.draw()
    
            pygame.display.flip()

        pygame.quit()
    
    def draw(self):
        self.container.draw()
        


if __name__ == "__main__":
    a = AlgoVisual((1200, 700))
    a.run()