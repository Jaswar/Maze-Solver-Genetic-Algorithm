# Maze-Solver-Genetic-Algorithm

Description: This repository contains a genetic algorithm approach to solving mazes. Algorithm contains certain amount of bots in its population, which DNAs contain a sequence of moves. As the rules say, best bots are then mixed although best bots stay in population in order to prevent losing best sequences.

Required libraries:
- numpy
- pygame
- operator

My specs:
- i7-7700HQ Processor
- 16GB RAM
- NVIDIA Quadro M1200 4GB graphics card

Training: It all starts with a population of completely random bots. Their DNA was chosen randomly therefore their moves are random as well. For each bot a fitness function is calculated, this function is the distance from last position to the start. What the algorithm does next is it sorts these bots according to their fitness and chooses best ones. These are then mixed between themselves and preserved for the next generation. During the mixing some random mutations are added, either to only particular genes or to the bot as a whole making a completely new one. Due to the way my algorithm works, population size will be constant. Then the process repeats. 
