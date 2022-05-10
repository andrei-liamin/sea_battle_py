# The Sea Battle - The Game

class Ship():
    def __init__(self, *coords):
        self.coords = coords
        self.length = len(coords)

class Field():
    def __init__(self, *ships):
        self.ships = ships
        self.emptyCell = "O"
        self.size = 6

    @property
    def result(self):
        res = []
        for i in range(self.size + 1):
            if i == 0:
                res.append([" "] + list(range(1, self.size + 1)))
            else:
                res.append([i] + [self.emptyCell for j in range(self.size)])
        return res

    def printField(self):
        for row in self.result:
            print("|".join(map(str, row)) + "|")

myField = Field()
myField.printField()
