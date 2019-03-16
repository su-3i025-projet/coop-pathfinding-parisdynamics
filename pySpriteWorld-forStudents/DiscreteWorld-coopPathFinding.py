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
    def __init__(self):
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
    positions = {}

    def __init__(self, game, player, nom, init, goal, wallStates, goalStates):
        self.game = game
        self.player = player
        self.nom = nom
        self.position = init
        self.goal = goal
        self.graph = Graph((wallStates, goalStates))
        self.chemin = []
        self.frontier = PriorityQueue()
        self.frontier.put(init, 0)
        self.came_from = {}
        self.cost_so_far = {}
        self.came_from[init] = None
        self.cost_so_far[init] = 0
        self.i=0
        self.pause=0
        Jeu.positions[self.nom] = init

    def play(self):
        while (not self.frontier.empty()):
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
        self.chemin.append(result)

    def reset(self):
        self.frontier.put(self.position, 0)
        self.came_from = {}
        self.cost_so_far = {}
        self.came_from[self.position] = None
        self.cost_so_far[self.position] = 0

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

    def move(self):
        Jeu.positions[self.nom] = (-1,-1)
        print("chemin: "+str(self.chemin))
        if(len(self.chemin) == 0):
            print("joueur {0}: RIEN A CHERCHER".format(self.nom))
            Jeu.positions[self.nom] = self.position
            return
        if(len(self.chemin[-1]) == 0):
            print("joueur {0}: CHEMIN FINI".format(self.nom))
            Jeu.positions[self.nom] = self.position
            self.chemin.pop(-1)
            return
        if(self.chemin[-1][0] in Jeu.positions.values()):
            print("joueur {0}: conflit avec un autre joueur".format(self.nom))
            Jeu.positions[self.nom] = self.position
            self.pause += 1
            return
        if(self.pause > 0):
            if(self.pause > 1):
                pass
            else:
                print("joueur {0}: passe mon tour".format(self.nom))
                Jeu.positions[self.nom] = self.position
                self.pause -= 1
            return
        row, col = self.chemin[-1][0]
        self.player.set_rowcol(row, col)
        self.position = (row, col)
        self.chemin[-1].pop(0)
        Jeu.positions[self.nom] = self.position
        print("pos :", self.nom, self.position)
        game.mainiteration()

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer3'
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
    # Placement aleatoire des fioles
    #-------------------------------


    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre


    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------


    # bon ici on fait juste plusieurs random walker pour exemple...

    posPlayers = initStates

    jeux = []
    chemins = []
    z=0
    for i in range(len(goalStates)):
        jeux.append(Jeu(game, players[z], z, posPlayers[z], goalStates[i], wallStates, goalStates))
        jeux[i].play()
        if(z >= nbPlayers):
            z=0
        else:
            z+=1

    for i in range(iterations):
        for jeu in jeux:
            jeu.move()
            # si on a  trouvé un objet on le ramasse
            if(jeu.position in goalStates):
                o = jeu.player.ramasse(game.layers)
                game.mainiteration()
                print ("Objet trouvé par le joueur ", jeu.nom)
                goalStates.remove(jeu.position) # on enlève ce goalState de la liste
                score[jeu.nom]+=1


                # et on remet un même objet à un autre endroit
                x = random.randint(1,19)
                y = random.randint(1,19)
                while (x,y) in wallStates:
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                o.set_rowcol(x,y)
                goalStates.append((x,y)) # on ajoute ce nouveau goalState
                game.layers['ramassable'].add(o)
                jeu.goal = (x, y)
                jeu.reset()
                jeu.play()
                game.mainiteration()

                break

    print ("scores:", score)
    pygame.quit()

if __name__ == '__main__':
    main()
