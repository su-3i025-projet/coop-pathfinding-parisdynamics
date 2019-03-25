import math

class Graph():
    def __init__(self, world, limit_x, limit_y):
        self.wall, self.goal= world
        self.limit_x = limit_x
        self.limit_y = limit_y

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
            if(p not in self.wall and p[0]>=0 and p[0]<self.limit_x and p[1]>=0 and p[1]<self.limit_y):
                final.append(p)
        return final

    def cost(self, currentP, nextP):
        xa, ya = currentP
        xb, yb = nextP
        return math.sqrt((xb-xa)**2 + (yb-ya)**2)
