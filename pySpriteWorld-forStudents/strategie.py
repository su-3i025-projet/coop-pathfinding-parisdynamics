class Strategie():
    def __init__(self, nom):
        print("Strategie: ", nom)

    def apply(self, Jeu):
        raise NotImplementedError

    def reply(self, Jeu):
        raise NotImplementedError

class CacheStrategie(Strategie):
    def __init__(self):
        super().__init__("Cache")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        for currentJ in Jeu.references.values():
            if(len(currentJ.chemin) > 0 and len(currentJ.chemin[-1]) > 0):
                if(currentJ.chemin[-1][0] is Jeu.chemin[-1][0]):
                    if(len(Jeu.caches["l1"][currentJ.nom]) > 0):
                        currentJ.chemin[-1].insert(0, Jeu.caches["l1"][currentJ.nom][-1])
                        Jeu.caches["l1"][currentJ.nom].pop(-1)
                    currentJ.chemin[-1].insert(0, currentJ.position)

class OppoStrategie(Strategie):
    def __init__(self):
        super().__init__("Opportuniste")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        case = Jeu.chemin[-1][0]
        print("refences:", Jeu.references)
        for currentJ in Jeu.references.values():
            if(len(currentJ.chemin[-1]) > 0):
                print(currentJ.nom, currentJ.chemin[-1][0], case)
                if(currentJ.chemin[-1][0] == case):
                    currentJ.avoid.append(case)
                    currentJ.graph.wall.append(case)
                    currentJ.reset()
                    currentJ.play()
                if(not(currentJ is Jeu) and currentJ.position == case):
                    currentJ.freeze(3)
        #exit(0)



class CoopStrategie(Strategie):
    def __init__(self):
        super().__init__("Cooperative")

    def apply(self, Jeu):
        pass

    def reply(self, Jeu):
        pass
