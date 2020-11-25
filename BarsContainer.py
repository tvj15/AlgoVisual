import pygame
from pygame_widgets import Button
import math
import random
from Bars import Bars
import copy


class BarsContainer:
    def __init__(self, surface, x, y, width, height, bw):
        self.surface = surface
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
        self.bars = self.create_bars()
        self.idx = 0
        self.jdx = 0
        self.bubbleSorting = False
        self.insertionSorting = False
        

    def draw(self):
        pygame.draw.rect(self.surface, (200, 200, 200), (self.x-self.THICKNESS/2, self.y-self.THICKNESS / 2, self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS))
        # Buttons
        for button in self.buttons:
            button.draw()
        # Bars
        for bar in self.bars:
            bar.draw()
        
        if self.bubbleSorting:
            if self.bubbleSort():
                self.bubbleSorting = False

        if self.insertionSorting:
            if self.insertionSort():
                self.insertionSorting = False


        pygame.draw.rect(self.surface, (0, 0, 0), (self.x-self.THICKNESS/2, self.y-self.THICKNESS / 2, self.WIDTH+self.THICKNESS, self.HEIGHT+self.THICKNESS), self.THICKNESS)

    def create_bars(self):
        bars = []
        for i in range(self.numberBars):
            height = random.randint(10, self.HEIGHT - 50)
            x = i * (self.BW + self.space) + (self.WIDTH - (self.numberBars *self.BW + self.numberBars * self.space))/2 + self.x
            b = Bars(self.surface, x, self.HEIGHT + self.y,height, self.BW, self.purple)
            bars.append(b)
        return bars

    def generateButtons(self):
        button = []
        # Create Arrays Button
        button.append(Button(self.surface, self.x+(self.WIDTH)/2-100, self.y+self.HEIGHT+20, 200, 50, text='Generate Arrays',  fontSize=25, inactiveColour=(200, 0, 200), pressedColour=(0, 255, 0), onClick=self.generateBarsButtonOnClick))

        button.append(Button(
            self.surface, 100, self.y, 200, 50, text='Bubble Sort',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.bubbleSortOnClick
        ))

        button.append(Button(
            self.surface, 100, self.y + 100, 200, 50, text='Merge Sort',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.mergeSort, onClickParams=(0, self.numberBars-1)
        ))
        button.append(Button(
            self.surface, 100, self.y + 200, 200, 50, text='Insertion Sort',
            fontSize=25,
            inactiveColour=(200, 0, 200),
            pressedColour=(0, 255, 0),
            onClick=self.insertionSortOnClick
        ))

        return button

    def generateBarsButtonOnClick(self):
        if not self.bubbleSorting and not self.insertionSorting:
            self.bars = self.create_bars()


    def bubbleSortOnClick(self):
        if not self.bubbleSorting and not self.insertionSorting:
            self.init_bubble_sort()
            self.bubbleSorting = True
    
    def insertionSortOnClick(self):
        if not self.bubbleSorting and not self.insertionSorting:
            self.init_insertion_sort()
            self.insertionSorting = True

    def init_bubble_sort(self):
        self.idx = 0
        self.jdx = 0
        self.comparing = False
        self.swapping = False
        self.wait = 0

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
        self.idx = 1
        self.jdx = 0
        self.key = 0
        self.key = self.bars[self.idx].HEIGHT
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

        

    def mergeSort(self, l, u):
        if not self.bubbleSorting and not self.insertionSorting:
            pass
        # if l >= u:
        #     return
        # mid = (l+u)//2
        # self.mergeSort(l, mid)
        # self.mergeSort(mid+1, u)
        # la = []
        # for i in range(l, mid):
        #     la.append(self.bars[i].HEIGHT)
        # ra = []
        # for i in range(mid+1, u+1):
        #     ra.append(self.bars[i].HEIGHT)
        # li = ri = 0
        # si = l
        # while li<len(la) and ri<len(ra):
        #     if la[li] < ra[ri]:
        #         self.bars[si].HEIGHT = la[li]
        #         li += 1
        #     else:
        #         self.bars[si].HEIGHT = ra[ri]
        #         ri += 1
        #     si += 1
        # while li < len(la):
        #     self.bars[si].HEIGHT = la[li]
        #     li += 1
        #     si += 1
        # while ri < len(ra):
        #     self.bars[si].HEIGHT = ra[ri]
        #     ri += 1
        #     si += 1
        

    

    def listen_events(self, events):
        for button in self.buttons:
            button.listen(events)
