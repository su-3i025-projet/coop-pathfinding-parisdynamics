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
