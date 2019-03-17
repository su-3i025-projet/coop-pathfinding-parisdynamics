from priorityQueue import PriorityQueue
from graph import Graph

class Jeu():
    cpt = 0
    positions = {}
    caches = {}
    caches["l1"] = {}
    caches["l2"] = []

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
        self.pause=0
        self.ID = Jeu.cpt
        Jeu.cpt += 1
        Jeu.positions[self.nom] = init
        Jeu.caches["l1"][self.nom] = []

    def play(self):
        i = 1
        while (not self.frontier.empty()):
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
            i += 1

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
        # print("chemin: "+str(self.chemin))
        if(len(self.chemin) == 0):
            # print("joueur {0}: RIEN A CHERCHER".format(self.nom))
            Jeu.positions[self.nom] = self.position
            return
        if(len(self.chemin[-1]) == 0):
            # print("joueur {0}: CHEMIN FINI".format(self.nom))
            Jeu.positions[self.nom] = self.position
            self.chemin.pop(-1)
            return
        if(self.chemin[-1][0] in Jeu.positions.values() and self.pause <= 0):
            print("joueur {0}: conflit avec un autre joueur".format(self.nom))
            Jeu.positions[self.nom] = self.position
            self.pause += 1
            return
        elif(self.pause > 1):
            if(len(Jeu.caches["l1"][self.nom]) > 0):
                row, col = Jeu.caches["l1"][self.nom][-1]
            else:
                return
            if((row, col) in Jeu.positions.values()):
                return
            self.chemin[-1].insert(0, (self.position))
            self.chemin[-1].insert(0, (-1, -1))
            Jeu.caches["l1"][self.nom].pop(-1)
            self.pause -= 1
        elif(self.pause > 0):
            print("joueur {0}: passe mon tour".format(self.nom))
            Jeu.positions[self.nom] = self.position
            if(self.chemin[-1][0] in Jeu.positions.values()):
                self.pause += 1
            else:
                self.pause -= 1
            return
        else:
            Jeu.caches["l1"][self.nom].append(self.position)
            row, col = self.chemin[-1][0]
        self.player.set_rowcol(row, col)
        self.position = (row, col)
        self.chemin[-1].pop(0)
        Jeu.positions[self.nom] = self.position
        # print("pos :", self.nom, self.position)
        self.game.mainiteration()
