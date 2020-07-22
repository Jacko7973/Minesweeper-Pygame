import sys
import os
import numpy as np
import time
import random
import pygame
from pygame.locals import *

size = (30, 40)
bombs = 200

class Minesweeper(object):

    def __init__(self):
        global size, bombs
        pygame.init()
        pygame.font.init() 

        self.size = size
        self.totalBombs = bombs
        self.width, self.height = self.size[0]*15+150, self.size[1]*15+150

        self.clock = pygame.time.Clock()
        self.canvas = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Minesweeper')
        
        self.textFont = pygame.font.SysFont('Arial', 15, 1)
        self.infoTextFont = pygame.font.SysFont('Arial', 40, 1)
        self.tileImage = pygame.image.load(os.path.join('Images', 'tileImage.png'))
        self.flagImage = pygame.image.load(os.path.join('Images', 'flagImage.png'))
        self.setupGame()

        while True:
            self.update()

    def setupGame(self):
        self.frame = 0
        self.board = self.setupBoard((self.size[1], self.size[0]), self.totalBombs)
        self.clickedPosArray = np.zeros((self.size[1], self.size[0]), int)
        self.flaggedPosArray = np.zeros((self.size[1], self.size[0]), int)

    
    def update(self):
        self.clock.tick(10)
        won = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                self.mouseClicked(event.pos, event.button)

        self.canvas.fill((255, 255, 255))

        boarder = pygame.Surface((self.size[0]*15+20, self.size[1]*15+20))
        boarder.fill((100, 100, 100))
        innerRect = pygame.Surface((self.size[0]*15, self.size[1]*15))
        innerRect.fill((230, 230, 230))
        for i in range(1, self.size[0]):
            pygame.draw.line(innerRect, (0, 0, 0), (i * 15, 0), (i * 15, 650))
        for i in range(1, self.size[1]):
            pygame.draw.line(innerRect, (0, 0, 0), (0, i * 15), (650, i * 15))

        self.canvas.blit(boarder, (65, 65))

        totalUnclicked = 0
        for y in range(len(self.clickedPosArray)):
            for x in range(len(self.clickedPosArray[0])):
                if self.clickedPosArray[y][x] == 0:
                    totalUnclicked += 1
                    if self.flaggedPosArray[y][x] == 0:
                        innerRect.blit(self.tileImage, (x*15, y*15))
                    else:
                        innerRect.blit(self.flagImage, (x*15, y*15))
                else:
                    if self.board[y][x] != 0:
                        num = self.board[y][x]
                        if num == 1:
                            clr = (0, 0, 240)
                        elif num == 2:
                            clr = (0, 158, 8)
                        elif num == 3:
                            clr = (240, 0, 0)
                        elif num == 4:
                            clr = (141, 50, 168)
                        elif num == 5:
                            clr = (163, 60, 39)
                        elif num == 6:
                            clr = (42, 212, 200)
                        elif num == 7:
                            clr = (0, 0, 0)
                        elif num == 8:
                            clr = (150, 150, 150)
                        text = self.textFont.render(str(num), False, clr)
                        innerRect.blit(text, ((x*15)+5, (y*15)))

        if totalUnclicked == self.totalBombs:
            won = True

        self.canvas.blit(innerRect, (75, 75))

        timerText = self.infoTextFont.render(createTime(self.frame // 10), False, (240, 0, 0))
        timerX = self.width // 2 - timerText.get_width() // 2

        self.canvas.blit(timerText, (timerX, 5))

        if won:
            infoText = self.infoTextFont.render('You Win', False, (0, 240, 0))
            txtX = self.width // 2 - infoText.get_width() // 2
            txtY = self.height // 2 - infoText.get_height() // 2
            self.canvas.blit(infoText, (txtX, txtY))
            pygame.display.update()
            time.sleep(2)
            self.setupGame()

        self.frame += 1
        pygame.display.update()

    def setupBoard(self, size, bombs):
        board = np.zeros(size, int)
        availableList = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                availableList.append((x, y))

        i = 0
        while i < bombs:
            (x, y) = random.choice(availableList)
            board[y][x] = -1
            for pos in self.findNeighborList((x, y)):
                if board[pos[1]][pos[0]] != -1:
                    board[pos[1]][pos[0]] += 1
            availableList.remove((x, y))
            i += 1

        return board

    def findNeighborList(self, pos):
        x, y = pos[0], pos[1]
        posList = [(x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]
        for item in posList[:]:
            if item[0] < 0 or item[0] >= self.size[0]:
                posList.remove(item)
                continue
            if item[1] < 0 or item[1] >= self.size[1]:
                posList.remove(item)
                continue

        return posList

    def mouseClicked(self, pos, button):
        x, y = pos[0]-75, pos[1]-75
        
        if x >= 0 and x < self.size[0]*15:
            if y >= 0 and y < self.size[1]*15:
                gridPos = (x // 15, y // 15)
                if self.clickedPosArray[gridPos[1]][gridPos[0]] == 0:
                    if button == 1:
                        self.revealSquare(gridPos)
                    elif button == 3:
                        if self.flaggedPosArray[gridPos[1]][gridPos[0]] == 0:
                            self.flaggedPosArray[gridPos[1]][gridPos[0]] = 1
                        else:
                            self.flaggedPosArray[gridPos[1]][gridPos[0]] = 0
                return

                

    def revealSquare(self, pos):
        x, y = pos[0], pos[1]
        if self.flaggedPosArray[y][x] == 0:
            if self.board[y][x] != -1:
                self.clickedPosArray[pos[1]][pos[0]] = 1
                if self.board[y][x] == 0:
                    neighbors = self.findNeighborList((x, y))
                    for item in neighbors:
                        if self.clickedPosArray[item[1]][item[0]] == 0:
                            self.revealSquare(item)
            else:
                infoText = self.infoTextFont.render('Game Over', False, (240, 0, 0))
                txtX = self.width // 2 - infoText.get_width() // 2
                txtY = self.height // 2 - infoText.get_height() // 2
                self.canvas.blit(infoText, (txtX, txtY))
                pygame.display.update()
                time.sleep(2)
                self.setupGame()

def createTime(seconds):
    return str(seconds // 60) + ':' + str(seconds % 60).zfill(2)


if __name__ == '__main__':
    game = Minesweeper()