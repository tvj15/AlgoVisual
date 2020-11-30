import pygame
from pygame_widgets import Button, Slider
import math
import random
from Bars import Bars


class BarsContainer:
    def __init__(self, mainObj, x, y, width, height, bw):
        self.mainObj = mainObj
        self.x = x
        self.y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.BW = bw
        self.space = (self.BW//5) + 1
        self.numberBars = (self.WIDTH // (self.BW + self.space))-1
        self.THICKNESS = 4
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.yellow = (255,255,0)
        self.purple = (80, 40, 130)
        self.blue = (0,0,255)
        self.buttons = self.generateButtons()
        self.generateSlider()        
        self.bars = self.create_bars()
        self.idx = 0
        self.jdx = 0
        self.bubbleSorting = False
        self.insertionSorting = False
        self.pancakeSorting = False
        self.font = pygame.font.SysFont("Copperplate-Light", 25)
        self.noSwaps = 0

    def drawText(self, algo,worst,best,average,space):
        text = self.font.render(f"Algortihm: {algo}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+10,self.y-75))
        text = self.font.render(f"Worst Case Time Complexity: {worst}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+10,self.y-25))
        text = self.font.render(f"Best Case Time Complexity: {best}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+10,self.y-50))
        text = self.font.render(f"Average Case Time Complexity: {average}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+335,self.y-25))
        text = self.font.render(f"Space Complexity: {space}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+335,self.y-50))
        

        
    def generateSlider(self):
        self.slider = Slider(self.mainObj.surface, self.x + 20 , self.y+self.HEIGHT+35, self.WIDTH - 500, 20, min=2, max=100, step=2,initial=self.BW, colour=(180, 110, 205))


    def draw(self):
        pygame.draw.rect(self.mainObj.surface, (200, 200, 200), (self.x-self.THICKNESS/2, self.y-self.THICKNESS / 2, self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS))
        # Buttons
        for button in self.buttons:
            button.draw()
        # Bars
        for bar in self.bars:
            bar.draw()
        
        self.slider.draw()
        
        text = self.font.render(f"Number Of Swaps: {self.noSwaps}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+10,self.y+10))
        text = self.font.render(f"Number Of Bars: {self.numberBars}",True,(0,0,0))
        self.mainObj.surface.blit(text, (self.x+225,self.y+10))
        
        if self.bubbleSorting:
            self.drawText("Bubble Sort","O(n*n)", "O(n)", "O(n*n)", "O(1)")
            if self.bubbleSort():
                self.bubbleSorting = False

        if self.insertionSorting:
            self.drawText("Insertion Sort","O(n*n)", "O(n)", "O(n*n)", "O(1)")
            if self.insertionSort():
                self.insertionSorting = False

        if self.pancakeSorting:
            self.drawText("Pancake Sort","O(n)", "O(n)", "O(n)", "O(n)")
            if self.pancakeSort():
                self.pancakeSorting = False
        



        pygame.draw.rect(self.mainObj.surface, (0, 0, 0), (self.x-self.THICKNESS/2, self.y-self.THICKNESS / 2, self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS), self.THICKNESS)

    def create_bars(self):
        self.noSwaps = 0
        self.space = (self.BW//5) + 1
        self.numberBars = (self.WIDTH // (self.BW + self.space))-1
        bars = []
        for i in range(self.numberBars):
            height = random.randint(10, self.HEIGHT - 50)
            x = i * (self.BW + self.space) + (self.WIDTH - (self.numberBars *self.BW + self.numberBars * self.space))/2 + self.x
            b = Bars(self.mainObj.surface, x, self.HEIGHT + self.y,height, self.BW, self.purple)
            bars.append(b)
        return bars

    def generateButtons(self):
        button = []
        # Create Arrays Button
        button.append(Button(self.mainObj.surface, self.x+(self.WIDTH)/2 , self.y+self.HEIGHT+20, 200, 50, text='Generate Arrays',  fontSize=25, inactiveColour=(180, 110, 205), pressedColour=(130, 110, 205), onRelease=self.generateBarsButtonOnClick))

        button.append(Button(
            self.mainObj.surface, 100, self.y, 200, 50, text='Bubble Sort',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.bubbleSortOnClick
        ))

        button.append(Button(
            self.mainObj.surface, 100, self.y + 100, 200, 50, text='Insertion Sort',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.insertionSortOnClick
        ))

        button.append(Button(
            self.mainObj.surface, 100, self.y + 200, 200, 50, text='Pancake Sort',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.pancakeSortOnClick
        ))

        button.append(Button(
            self.mainObj.surface, 100, self.y+400, 200, 50, text='Back',
            fontSize=25,
            inactiveColour=(180, 110, 205),
            pressedColour=(130, 110, 205),
            onRelease=self.backButtonOnClick
        ))

        return button

    def isClickAllowed(self):
        if not self.bubbleSorting and not self.insertionSorting and not self.pancakeSorting:
            return True
        return False


    def generateBarsButtonOnClick(self):
        if self.isClickAllowed():
            self.bars = self.create_bars()


    def bubbleSortOnClick(self):
        if self.isClickAllowed():
            self.init_bubble_sort()
            self.bubbleSorting = True
    
    def insertionSortOnClick(self):
        if self.isClickAllowed():
            self.init_insertion_sort()
            self.insertionSorting = True

    def pancakeSortOnClick(self):
        if self.isClickAllowed():
            self.init_pancake_sort()
            self.pancakeSorting = True

    def backButtonOnClick(self):
        if self.isClickAllowed():
            self.mainObj.sorter = False
            self.mainObj.pathfinder = False

    def init_bubble_sort(self):
        self.noSwaps = 0
        self.idx = 0
        self.jdx = 0
        self.comparing = False
        self.swapping = False
        if self.BW > 70:
            self.wait = 300
        elif self.BW > 50:
            self.wait = 100
        else:
            self.wait = self.BW 

    def bubbleSort(self):
        if 0 <= self.idx < self.numberBars - 1:
            if 0 <= self.jdx < self.numberBars - self.idx - 1:
                if not self.comparing:
                    self.bars[self.jdx].color=self.green
                    self.bars[self.jdx + 1].color=self.green
                    self.comparing = True
                    pygame.time.wait(self.wait)
                    return False
                if self.bars[self.jdx].HEIGHT > self.bars[self.jdx+1].HEIGHT:
                    if not self.swapping:
                        self.bars[self.jdx].color=self.red
                        self.bars[self.jdx + 1].color=self.red
                        self.swapping = True
                        pygame.time.wait(self.wait)
                        return False
                    self.bars[self.jdx].x, self.bars[self.jdx+1].x = self.bars[self.jdx+1].x, self.bars[self.jdx].x
                    self.bars[self.jdx], self.bars[self.jdx+1] = self.bars[self.jdx+1], self.bars[self.jdx]
                    self.noSwaps += 1
                    self.comparing = False
                    pygame.time.wait(self.wait)
                    return False
                self.bars[self.jdx + 1].color=self.purple
                self.bars[self.jdx].color=self.purple
                self.comparing = False
                self.swapping = False
                self.jdx += 1
                pygame.time.wait(self.wait)
                return False
            else:
                self.bars[self.jdx].color = self.blue
                self.idx += 1
                self.jdx = 0
                return False
        else:
            print('bubble sort done')
            for bar in self.bars:
                bar.color = self.yellow
            return True

    def init_insertion_sort(self):
        self.noSwaps = 0
        self.idx = 1
        self.jdx = 0
        self.key = 0
        self.key = self.bars[self.idx].HEIGHT
        if self.BW > 70:
            self.wait = 300
        elif self.BW > 50:
            self.wait = 100
        else:
            self.wait = self.BW 
        self.inserting = False

    
    def insertionSort(self):
        if 1 <= self.idx < self.numberBars:
            if not self.inserting:
                self.bars[self.idx].color = self.red
                self.bars[self.jdx].color = self.blue
                self.inserting = True
                pygame.time.wait(self.wait)
                return False
            if self.jdx >= 0 and self.key < self.bars[self.jdx].HEIGHT:
                self.bars[self.jdx].x, self.bars[self.jdx+1].x = self.bars[self.jdx+1].x, self.bars[self.jdx].x
                self.bars[self.jdx], self.bars[self.jdx+1] = self.bars[self.jdx+1], self.bars[self.jdx]
                self.noSwaps += 1
                self.jdx -= 1
                pygame.time.wait(self.wait)
                return False
            self.bars[self.jdx+1].color = self.blue
            self.inserting = False
            self.idx += 1
            if not self.idx == self.numberBars:
                self.key = self.bars[self.idx].HEIGHT
                self.jdx = self.idx - 1
            pygame.time.wait(self.wait)
            return False
        else:
            print("insertion sort done")
            for bar in self.bars:
                bar.color = self.yellow
            return True

    def init_pancake_sort(self):
        self.noSwaps = 0
        self.current = self.numberBars-1
        self.maxIndex = None
        self.start = 0
        self.maxFlipped = False
        self.currentFlipped = True
        self.changeMax = True
        self.i = 0
        self.maxFlipping = False
        self.currentFlipping = False
        if self.BW > 70:
            self.wait = 300
        elif self.BW > 50:
            self.wait = 100
        else:
            self.wait = self.BW 
        self.decrementCurr = False

    
    def pancakeSort(self):
        if self.current > 0:
            
            if self.changeMax:
                self.maxIndex = self.bars.index(max(self.bars[0:self.current+1], key=lambda bar: bar.HEIGHT))
                self.changeMax = False
            if self.maxIndex != self.current:
                if not self.maxFlipping and self.currentFlipped :
                    self.start = 0
                    self.i = self.maxIndex
                    self.maxFlipping = True
                if self.maxFlipping:
                    if self.start < self.i:
                        if self.start-1 >= 0 and self.i+1 <= self.maxIndex:
                            self.bars[self.start-1].color = self.purple
                            self.bars[self.i+1].color = self.purple
                        self.bars[self.start].color = self.red
                        self.bars[self.i].color = self.red
                        self.bars[self.start].x, self.bars[self.i].x = self.bars[self.i].x, self.bars[self.start].x
                        self.bars[self.start], self.bars[self.i] = self.bars[self.i], self.bars[self.start]
                        self.noSwaps += 1
                        self.start += 1
                        self.i -= 1
                        pygame.time.wait(self.wait)
                        return False
                    else:
                        if self.start-1 >= 0 and self.i+1 <= self.maxIndex:
                            self.bars[self.start-1].color = self.purple
                            self.bars[self.i+1].color = self.purple
                        self.maxFlipping = False
                        self.maxFlipped = True
                        self.currentFlipped = False
                        self.currentFlipping = False
                if not self.currentFlipping and self.maxFlipped:
                    self.start = 0
                    self.i = self.current
                    self.currentFlipping = True
                if self.currentFlipping:
                    if self.start < self.i:
                        if self.start-1 >= 0 and self.i+1 <= self.current:
                            self.bars[self.start-1].color = self.purple
                            self.bars[self.i+1].color = self.purple
                        self.bars[self.start].color = self.red
                        self.bars[self.i].color = self.red
                        self.bars[self.start].x, self.bars[self.i].x = self.bars[self.i].x, self.bars[self.start].x
                        self.bars[self.start], self.bars[self.i] = self.bars[self.i], self.bars[self.start]
                        self.noSwaps += 1
                        self.start += 1
                        self.i -= 1
                        pygame.time.wait(self.wait)
                        return False
                    else:
                        if self.start-1 >= 0 and self.i+1 <= self.current:
                            self.bars[self.start-1].color = self.purple
                            self.bars[self.i+1].color = self.purple
                        self.currentFlipping = False
                        self.currentFlipped = True
                        self.maxFlipping = False
                        self.maxFlipped = False
                        self.decrementCurr = True
            else:
                self.decrementCurr = True

            self.bars[self.current].color = self.blue
            self.current -= 1
            self.changeMax = True
        else:
            print("pancake sort done")
            for bar in self.bars:
                bar.color = self.yellow
            return True


    def listen_events(self, events):
        if self.isClickAllowed():
            self.slider.listen(events)
            temp = self.slider.getValue()
            if temp != self.BW:
                self.BW = temp
                self.bars = self.create_bars()
        for button in self.buttons:
            button.listen(events)
