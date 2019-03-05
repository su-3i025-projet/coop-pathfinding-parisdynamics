# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys
import math

# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----


# ---- ---- ---- ---- ---- ----
# ---- Magie             ----
# ---- ---- ---- ---- ---- ----
class PriorityQueue():
    def __init__(self, world):
        self.goal, self.wall = world
        self.frontier = []

    def put(self, position, cost):
        self.frontier.append((position, cost))

    def empty(self):
        return len(self.frontier) == 0

    def get(self):
        result = self.frontier[0]
        for t in self.frontier:
            if(t[1] != 0 and t[1] < result[1]):
                result = t
        pos, cos = result
        self.frontier.remove(result)
        return pos, cos

    def clear(self):
        self.frontier.clear()


def heuristic(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xa-xb) + abs(ya-yb)

def path(start, came_from):
    final = []
    if(start not in came_from):
        return final
    current = start
    while(current != None):
        final.append(current)
        current = came_from[current]
    return final

class Graph():
    def __init__(self, world):
        self.wall, self.goal= world

    def bas(self, position):
        x, y = position
        return (x, y-1)

    def droite(self, position):
        x, y = position
        return (x+1, y)

    def haut(self, position):
        x, y = position
        return (x, y+1)

    def gauche(self, position):
        x, y = position
        return (x-1, y)

    def neighbors(self, position):
        final = []
        test = [self.haut(position), self.gauche(position), self.droite(position), self.bas(position)]
        for p in test:
            if(p not in self.wall and p[0]>=0 and p[0]<=20 and p[1]>=0 and p[1]<=20):
                final.append(p)
        return final

    def cost(self, currentP, nextP):
        xa, ya = currentP
        xb, yb = nextP
        return math.sqrt((xb-xa)**2 + (yb-ya)**2)
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------
    start = initStates[0]
    goal = goalStates[0]
    graph = Graph((wallStates, goalStates))
    chemin = []
    frontier = PriorityQueue((wallStates, goalStates))
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    i=0
    y = -1

    while (not frontier.empty()) and i<iterations:
        print("\n\n**** TOUR"+str(i)+" ****")
        print("came from: "+str(came_from))
        print("cost so far: "+str(cost_so_far))
        print("frontier: "+str(frontier.frontier))

        position, cout = frontier.get()

        if(position == goal):
            frontier.clear()
            break

        for nextP in graph.neighbors(position):
            new_cost = cost_so_far[position] + graph.cost(position, nextP)
            if nextP not in cost_so_far or new_cost < cost_so_far[nextP]:
                cost_so_far[nextP] = new_cost
                priority = new_cost + heuristic(goal, nextP)
                frontier.put(nextP, priority)
                came_from[nextP] = position
                #player.set_rowcol(nextP[0],nextP[1])
                #print ("pos 1:",nextP[0],nextP[1])
                #game.mainiteration()
        i += 1

    chemin = path(goal, came_from)

    for a in range(len(chemin)):
        nextP = chemin[y]
        player.set_rowcol(nextP[0],nextP[1])
        print ("pos 1:",nextP[0],nextP[1])
        game.mainiteration()

        if (nextP[0],nextP[1])==goal:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            pygame.quit()
        y -= 1
    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    

"""
    row,col = initStates[0]
    #row2,col2 = (5,5)

    for i in range(iterations):
    
    
        x_inc,y_inc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        next_row = row+x_inc
        next_col = col+y_inc
        if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=20 and next_col>=0 and next_col<=20:
            player.set_rowcol(next_row,next_col)
            print ("pos 1:",next_row,next_col)
            game.mainiteration()

            col=next_col
            row=next_row

            
       
            
        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
"""
        
    
   

if __name__ == '__main__':
    main()
    


