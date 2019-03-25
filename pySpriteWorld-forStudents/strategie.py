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
        case = Jeu.chemin[0]
        for currentJ in Jeu.references.values():
            if(not(currentJ is Jeu) and currentJ.position == case and currentJ.ID < Jeu.ID):
                return
        if(len(Jeu.caches["l1"][Jeu.nom]) <= 0 and len(Jeu.caches["l2"][Jeu.nom]) > 0):
            Jeu.caches["l1"][Jeu.nom] = Jeu.caches["l2"][Jeu.nom]
            Jeu.caches["l2"][Jeu.nom] = []
        if(len(Jeu.caches["l1"][Jeu.nom]) > 0):
            Jeu.chemin.insert(0, Jeu.position)
            Jeu.chemin.insert(0, Jeu.caches["l1"][Jeu.nom][-1])
            Jeu.caches["l1"][Jeu.nom].pop(-1)
        else:
            print("impossible finir chemin")
            return

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
        #self.garbage(t)
        print("\n\n\nresa", self.reservation)
        while(not self.arrangementLineaire(Jeu, t)):
            print("arrangement")
        #on effectue la reservation
        for i in range(len(Jeu.chemin)):
            if(t+i in self.reservation.keys()):
                self.reservation[t+i][Jeu.chemin[i]] = Jeu.nom
            else:
                self.reservation[t+i] = {Jeu.chemin[i]:Jeu.nom}
        print("resa", self.reservation)

    def reply(self, Jeu):
        pass

    def arrangementLineaire(self, Jeu, t):
        #on modifie le chemin en fonction des conflits rencontres
        temoin = True
        ecart = 0
        length = len(Jeu.chemin)
        for i in range(length):
            if(t+i in self.reservation.keys()):
                if(Jeu.chemin[i+ecart] in self.reservation[t+i].keys()):
                    print("conflit a t =", t+i)
                    y = 1;
                    while(t+i+y in self.reservation.keys() and Jeu.chemin[i+ecart-y] in self.reservation[t+i+y].keys()):
                        y += 1
                    print("y:", y)
                    for inter in range(y):
                        Jeu.chemin.insert(i-ecart-y, Jeu.chemin[i-ecart-y])
                    ecart += y
        #on regle les derniers conflits
        return self.arrangementFace2Face(Jeu, t)

    def arrangementFace2Face(self, Jeu, t):
        for i in range(len(Jeu.chemin)):
            if(t+i-1 in self.reservation.keys() and Jeu.chemin[i] in self.reservation[t+i-1].keys() and Jeu.nom != self.reservation[t+i-1][Jeu.chemin[i]]):
                print(Jeu.chemin[i])
                print(Jeu.nom)
                print(self.reservation[t+i-1][Jeu.chemin[i]])
                print(Jeu.chemin)
                print("t=",t+i)
                if(i <= 2):
                    print("impossible de finir le chemin")
                    return True
                print("je rajoute", Jeu.chemin[i-2])
                Jeu.chemin.insert(i-1, Jeu.chemin[i-2])
                return False
        return True

    def garbage(self, t):
        collector = []
        for k in self.reservation.keys():
            if(k < t):
                collector.append(k)
        for k in collector:
            del self.reservation[k]
