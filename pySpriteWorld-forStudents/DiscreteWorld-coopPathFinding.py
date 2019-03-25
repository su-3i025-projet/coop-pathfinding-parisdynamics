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

from jeu import Jeu

# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer11'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 30  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def main():

    #for arg in sys.argv:
    iterations = 500 # default
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
    posPlayers = initStates

    temoin = False
    jeux = []
    z=0
    for i in range(len(goalStates)):
        jeux.append(Jeu(game, players[z], "j"+str(z), posPlayers[z], goalStates[i], wallStates, goalStates))
        jeux[i].play()
        if(z >= nbPlayers):
            z=0
        else:
            z+=1

    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------

    for i in range(iterations):
        if(temoin):
            break
        for jeu in jeux:
            jeu.move()
            # si on a  trouvé un objet on le ramasse
            if(jeu.position == jeu.goal):
                o = jeu.player.ramasse(game.layers)
                game.mainiteration()
                # print ("Objet trouvé par le joueur ", jeu.nom)
                goalStates.remove(jeu.position) # on enlève ce goalState de la liste
                score[jeu.ID]+=1


                # et on remet un même objet à un autre endroit

                x = random.randint(1,19)
                y = random.randint(1,19)
                while (x,y) in wallStates:
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                #o.set_rowcol(x,y)
                #goalStates.append((x,y)) # on ajoute ce nouveau goalState
                game.layers['ramassable'].add(o)
                jeu.goal = (-1, -1)
                jeu.reset()
                jeu.play()
                temoin = jeu.done()
                game.mainiteration()

                break

    print ("scores:", score)
    pygame.quit()

if __name__ == '__main__':
    main()
