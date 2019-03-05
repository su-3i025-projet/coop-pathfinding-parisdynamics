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
# ---- Magie               ----
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
            if(p not in self.wall and p[0]>=0 and p[0]<=19 and p[1]>=0 and p[1]<=19):
                final.append(p)
        return final

    def cost(self, currentP, nextP):
        xa, ya = currentP
        xb, yb = nextP
        return math.sqrt((xb-xa)**2 + (yb-ya)**2)

class Jeu():
    def __init__(self, player, init, goal, wallStates, goalStates, iterations=100):
        self.iterations = iterations
        self.player = player
        self.start = init
        self.goal = goal
        self.graph = Graph((wallStates, goalStates))
        self.chemin = []
        self.frontier = PriorityQueue((wallStates, goalStates))
        self.frontier.put(init, 0)
        self.came_from = {}
        self.cost_so_far = {}
        self.came_from[self.start] = None
        self.cost_so_far[self.start] = 0
        self.i=0
        self.y = -1

    def play(self):
        while (not self.frontier.empty()) and self.i<self.iterations:
            print("\n\n**** TOUR"+str(self.i)+" ****")
            print("came from: "+str(self.came_from))
            print("cost so far: "+str(self.cost_so_far))
            print("frontier: "+str(self.frontier.frontier))

            position, cout = self.frontier.get()

            if(position == self.goal):
                self.frontier.clear()
                break

            for nextP in self.graph.neighbors(position):
                new_cost = self.cost_so_far[position] + self.graph.cost(position, nextP)
                if nextP not in self.cost_so_far or new_cost < self.cost_so_far[nextP]:
                    self.cost_so_far[nextP] = new_cost
                    priority = new_cost + self.heuristic(self.goal, nextP)
                    self.frontier.put(nextP, priority)
                    self.came_from[nextP] = position
            self.i += 1

        result = self.path()
        result.reverse()
        return result

    def heuristic(self,a, b):
        xa, ya = a
        xb, yb = b
        return abs(xa-xb) + abs(ya-yb)

    def path(self):
        final = []
        if(self.goal not in self.came_from):
            return final
        current = self.goal
        while(current != None):
            final.append(current)
            current = self.came_from[current]
        return final
    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'match'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
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
    # Placement aleatoire des fioles de couleur 
    #-------------------------------
    
    for o in game.layers['ramassable']: # les rouges puis jaunes puis bleues
    # et on met la fiole qqpart au hasard
        x = random.randint(1,19)
        y = random.randint(1,19)
        while (x,y) in wallStates:
            x = random.randint(1,19)
            y = random.randint(1,19)
        o.set_rowcol(x,y)
        game.layers['ramassable'].add(o)
        game.mainiteration()                

    print(game.layers['ramassable'])


    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    
    posPlayers = initStates
    chemin = []

    for i in range(nbPlayers):
        jeuBis = Jeu(players[i], initStates[i], goalStates[i], wallStates, goalStates, 200)
        chemin.append(jeuBis.play())
    print("\n\nchemin: "+str(chemin))
    for i in range(iterations):
        
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            row,col = posPlayers[j]

            if(i < len(chemin[j])):
                next_row, next_col = chemin[j][i]
            else:
                next_row, next_col = (0, 0)
            # and ((next_row,next_col) not in posPlayers)
            if ((next_row,next_col) not in wallStates) and next_row>=0 and next_row<=19 and next_col>=0 and next_col<=19:
                players[j].set_rowcol(next_row,next_col)
                print ("pos :", j, next_row,next_col)
                game.mainiteration()
    
                col=next_col
                row=next_row
                posPlayers[j]=(row,col)
            
      
        
            
            # si on a  trouvé un objet on le ramasse
            if (row,col) in goalStates:
                o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Objet trouvé par le joueur ", j)
                goalStates.remove((row,col)) # on enlève ce goalState de la liste
                score[j]+=1
                
        
                # et on remet un même objet à un autre endroit
                x = random.randint(1,19)
                y = random.randint(1,19)
                while (x,y) in wallStates:
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                #o.set_rowcol(x,y)
                #goalStates.append((x,y)) # on ajoute ce nouveau goalState
                #game.layers['ramassable'].add(o)
                game.mainiteration()                
                
                break
            
    
    print ("scores:", score)
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


