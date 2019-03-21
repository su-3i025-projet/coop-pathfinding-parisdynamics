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
            if(len(currentJ.chemin) > 0 and len(currentJ.chemin[-1]) > 0):
                if(currentJ.chemin[-1][0] is Jeu.chemin[-1][0]):
                    currentJ.chemin[-1].insert(0, currentJ.position)
                    if(len(Jeu.caches["l1"][currentJ.nom]) > 0):
                        currentJ.chemin[-1].insert(0, Jeu.caches["l1"][currentJ.nom][-1])
                        Jeu.caches["l1"][currentJ.nom].pop(-1)

class OppoStrategie(Strategie):
    def __init__(self):
        super().__init__("Opportuniste")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        case = Jeu.chemin[-1][0]
        for currentJ in Jeu.references.values():
            if(len(currentJ.chemin[-1]) > 0):
                if(currentJ.chemin[-1][0] == case):
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
        for case in Jeu.chemin[-1]:
            if case in self.reservation.keys():
                print(Jeu.nom, "MEGA FREEZE par rapport au chemin de", self.reservation[case][0])
                Jeu.freeze(len(self.reservation[case][1])+Jeu.references[self.reservation[case][0]].priority)
                return
        for case in Jeu.chemin[-1]:
            self.reservation[case] = (Jeu.nom, Jeu.chemin[-1])

    def reply(self, Jeu):
        self.apply(Jeu)

    def garbage(self):
        collector = []
        for k, v in self.reservation.items():
            if(len(v[1]) <= 0):
                collector.append(k)
        for k in collector:
            del self.reservation[k]
