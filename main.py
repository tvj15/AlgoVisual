import pygame
from pygame.locals import *
import os 
from Grid import Grid
from BarsContainer import BarsContainer
from pygame_widgets import Button


class AlgoVisual:
    def __init__(self, display):
        self.DISPLAY = display
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("AlgoVisual")
        self.font = pygame.font.SysFont("Copperplate-Light", 35)
        self.buttons = self.generateButtons()
        self.pathfinder = False
        self.sorter = False
        self.bgImg = pygame.image.load("bg.JPG")
        self.bgImg = pygame.transform.scale(self.bgImg, (self.DISPLAY[0],self.DISPLAY[1]))



        
    def generateButtons(self):
        button = []
        # Create Maze Button
        button.append(Button(
            self.surface, 700, 100, 200, 50, text='VISUALIZE',
            font=self.font,
            inactiveColour=(100,100,100),
            pressedColour=(140, 125, 140),
            textColour=(210,210,210),
            onRelease=self.pathFindingButtonOnClick
        ))

        button.append(Button(
            self.surface, 350, 575, 200, 50, text='VISUALIZE',
            font=self.font,
            inactiveColour=(100,100,100),
            pressedColour=(140, 125, 140),
            textColour=(210,210,210),
            onRelease=self.sortingButtonOnClick

        ))
        return button

    def pathFindingButtonOnClick(self):
        self.grid = Grid(self, 600, 75, 500, 500, 50)
        self.pathfinder = True

    def sortingButtonOnClick(self):
        self.container = BarsContainer(self, 350, 100, 800, 500,50)
        self.sorter = True

    def listen_events(self, events):
        for button in self.buttons:
            button.listen(events)


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

            if self.sorter:
                self.container.listen_events(events)
            if self.pathfinder:
                self.grid.listen_events(events)
            if not self.sorter and not self.pathfinder:
                self.listen_events(events)

            self.surface.fill((180,210,230))
            
            self.draw()
    
            pygame.display.flip()

        pygame.quit()
    
    def draw(self):
        if self.sorter:
            self.container.draw()
        if self.pathfinder:
            self.grid.draw()
        if not self.sorter and not self.pathfinder:
            self.surface.blit(self.bgImg, (0,0))
            for button in self.buttons:
                button.draw()
        


if __name__ == "__main__":
    a = AlgoVisual((1200, 700))
    a.run()