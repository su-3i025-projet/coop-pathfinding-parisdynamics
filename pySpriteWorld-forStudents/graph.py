import math

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
