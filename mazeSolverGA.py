# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 20:14:04 2019

@author: janwa
"""

import numpy as np
import pygame
import time
import operator        

class Bot(object):
    
    def __init__(self, dnaSize):
        self.dnaSize = dnaSize
        self.gene = list()
        self.distance = 0.
        self.posx = 0
        self.posy = 0
        self.colour = (255,0,0)
        for i in range(self.dnaSize):
            self.gene.append(np.random.randint(0,4))
    
    def move(self, speedx, speedy):
        self.posx += speedx
        self.posy += speedy

class Environment(object):
    
    def __init__(self):
        self.width = 800
        self.height = 800
        self.nRows = 30
        self.nColumns = 30
        self.populationSize = 50
        self.dnaSize = 200
        self.bestCopied = 10
        self.mutationRate = 0.2
        self.offspringMutationRate = 0.15
        self.waitTime = 0.1
        self.slowdownRateOfChange = 0.025
        self.wallRatio = 0.3
        
        self.population = list()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.maze = np.zeros((self.nRows, self.nColumns))
        
        if self.bestCopied > self.populationSize:
            self.bestCopied = self.populationSize

        for i in range(self.nRows):
            for j in range(self.nColumns):
                if np.random.rand() < self.wallRatio:
                    self.maze[i][j] = 1
                else:
                    self.maze[i][j] = 0
                
        for i in range(min(3, self.nRows)):
            for j in range(min(3, self.nColumns)):
                self.maze[i][j] = 0
                
        for i in range(self.populationSize):
            bot = Bot(self.dnaSize)
            self.population.append(bot)
        
        
    def drawMaze(self):
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
        self.screen.fill((0,0,0))
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, (255,255,255), (j*cellWidth, i*cellHeight, cellWidth, cellHeight))
                    
        for i in range(self.populationSize):
            bot = self.population[i]
            pygame.draw.rect(self.screen, bot.colour, (bot.posx * cellWidth, bot.posy*cellHeight, cellWidth, cellHeight))
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.waitTime -= self.slowdownRateOfChange
                    if self.waitTime < 0:
                        self.waitTime = 0
                    print('Wait time lowered to {:.3f}'.format(self.waitTime))
                elif event.key == pygame.K_s:
                    self.waitTime += self.slowdownRateOfChange
                    print('Wait time increased to {:.3f}'.format(self.waitTime))
        
    
    def step(self, nAction):
        for bot in self.population:
            if bot.gene[nAction] == 0:
                if bot.posy > 0:
                    if self.maze[bot.posy - 1][bot.posx] == 0:
                        bot.move(0, -1)
            elif bot.gene[nAction] == 1:
                if bot.posy < self.nRows - 1:
                    if self.maze[bot.posy + 1][bot.posx] == 0:
                        bot.move(0, 1)
            elif bot.gene[nAction] == 2:
                if bot.posx < self.nColumns - 1:
                    if self.maze[bot.posy][bot.posx + 1] == 0:
                        bot.move(1, 0)
            elif bot.gene[nAction] == 3:
                if bot.posx > 0:
                    if self.maze[bot.posy][bot.posx - 1] == 0:
                        bot.move(-1, 0)
            bot.distance = pow(pow(bot.posx,2) + pow(bot.posy, 2), 0.5)          
            
        
        self.drawMaze()
        time.sleep(self.waitTime)
        
    
    def mix(self, dna1, dna2):
        offspring = Bot(self.dnaSize)
        for i in range(self.dnaSize):
            if np.random.rand() > self.offspringMutationRate:
                if np.random.randint(0,2) == 0:
                    offspring.gene[i] = dna1[i]
                else:
                    offspring.gene[i] = dna2[i]
            else:
                offspring.gene[i] = np.random.randint(0,4)
                    
        return offspring
    
    def createNewPopulation(self, gen):
        
        sortedPopulation = sorted(self.population, key = operator.attrgetter('distance'), reverse = True)
        self.population.clear()
        
        bestResult = sortedPopulation[0].distance
        available = self.populationSize - self.bestCopied
        
        for i in range(self.bestCopied):
            best = sortedPopulation[i]
            best.posx = 0
            best.posy = 0
            best.distance = 0.
            best.colour = (255, 255, 0)
            self.population.append(best)
        
        for i in range(available):
            new = Bot(self.dnaSize)
            if np.random.rand() > self.mutationRate:
                p1rnd = np.random.randint(0, self.bestCopied)
                parent1 = sortedPopulation[p1rnd]
                
                p2rnd = np.random.randint(0, self.bestCopied)
                while p2rnd == p1rnd:
                    p2rnd = np.random.randint(0, self.bestCopied)
                parent2 = sortedPopulation[p2rnd]
                
                dna1 = parent1.gene
                dna2 = parent2.gene
            
                new = self.mix(dna1, dna2)
                new.colour = (0,0,255)
                
            self.population.append(new)
            
        print('Generation: ' + str(gen) + ' Population Size: ' + str(len(self.population)) + ' Current Leader Distance: {:.2f}'.format(bestResult))

 
env = Environment()
nAction = 0
gen = 0
while True:
    if nAction < env.dnaSize:
        env.step(nAction)
        nAction += 1
    else:
        gen += 1
        nAction = 0
        env.createNewPopulation(gen)