class Strategie():
    def __init__(self, nom):
        print("Strategie: ", nom)

    def apply(self, Jeu):
        raise NotImplementedError

    def reply(self, Jeu):
        raise NotImplementedError

class NullStrategie(Strategie):
    def __init__(self):
        super().__init__("Null")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        pass

class CacheStrategie(Strategie):
    def __init__(self):
        super().__init__("Cache")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        for currentJ in Jeu.references.values():
            if(len(currentJ.chemin) > 0 and len(currentJ.chemin) > 0):
                if(currentJ.chemin[0] is Jeu.chemin[0]):
                    currentJ.chemin.insert(0, currentJ.position)
                    if(len(Jeu.caches["l1"][currentJ.nom]) > 0):
                        currentJ.chemin.insert(0, Jeu.caches["l1"][currentJ.nom][-1])
                        Jeu.caches["l1"][currentJ.nom].pop(-1)

class OppoStrategie(Strategie):
    def __init__(self):
        super().__init__("Opportuniste")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        case = Jeu.chemin[0]
        for currentJ in Jeu.references.values():
            if(len(currentJ.chemin) > 0):
                if(currentJ.chemin[0] == case):
                    currentJ.reset()
                    currentJ.avoid.append(case)
                    currentJ.graph.wall.append(case)
                    currentJ.play()
                if(not(currentJ is Jeu) and currentJ.position == case):
                    currentJ.freeze(3)

class CoopStrategie(Strategie):
    def __init__(self):
        super().__init__("Cooperative")
        self.reservation = {}

    def apply(self, Jeu):
        self.garbage()
        for case in Jeu.chemin:
            if case in self.reservation.keys():
                print(Jeu.nom, "MEGA FREEZE par rapport au chemin de", self.reservation[case][0])
                Jeu.freeze(len(self.reservation[case][1])+Jeu.references[self.reservation[case][0]].priority+1)
                return
            if(Jeu.isObstacle(case)):
                for k, v in Jeu.references.items():
                    if(Jeu.positions[k] == case):
                        Jeu.freeze(v.priority+1)
                        return
        for case in Jeu.chemin:
            self.reservation[case] = (Jeu.nom, Jeu.chemin)

    def reply(self, Jeu):
        pass

    def garbage(self):
        collector = []
        for k, v in self.reservation.items():
            if(len(v[1]) <= 0):
                collector.append(k)
        for k in collector:
            del self.reservation[k]

class AdvancedCoopStrategie(Strategie):
    def __init__(self):
        super().__init__("Advanced Cooperation")
        self.reservation = {}

    def apply(self, Jeu):
        t = Jeu.clock
        ecart = 0
        #self.garbage(t)
        print("\n\n\nresa", self.reservation)
        length = len(Jeu.chemin)
        #on modifie le chemin en fonction des conflits rencontres
        for i in range(length):
            if(t+i in self.reservation.keys()):
                if(Jeu.chemin[i+ecart] in self.reservation[t+i]):
                    print("conflit a t =", t+i)
                    y = 1;
                    while(t+i+y in self.reservation.keys() and Jeu.chemin[i+ecart-y] in self.reservation[t+i+y]):
                        y += 1
                    print("y:", y)
                    for inter in range(y+3):
                        Jeu.chemin.insert(i-ecart-y, Jeu.chemin[i-ecart-y])
                    ecart += y
        #on effectue la reservation
        for i in range(len(Jeu.chemin)):
            if(t+i in self.reservation.keys()):
                self.reservation[t+i].append(Jeu.chemin[i])
            else:
                self.reservation[t+i] = [Jeu.chemin[i]]
        print("resa", self.reservation)

    def reply(self, Jeu):
        exit(0)

    def garbage(self, t):
        collector = []
        for k in self.reservation.keys():
            if(k < t):
                collector.append(k)
        for k in collector:
            del self.reservation[k]
