from os import system, name
from random import randrange

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Sea Battle - The Game

field_size = 6
game_end = False
user_turn = True
is_error = False


class Ship():
    def __init__(self, *coords):
        self.decks = {"coords": coords,
                    "is_wrecked": [False for i in coords]}
        self.water_coords = self.generateWaterCoords(coords)
        self.length = len(coords)

    def generateWaterCoords(self, coords):
        water_coords = []
        delta_coords = [i for i in range(-1, 2)]
        for deck in coords:
            for dx in delta_coords:
                for dy in delta_coords:
                    x = deck[0]+dx
                    y = deck[1]+dy
                    if field_size >= x > 0 and field_size >= y > 0 and [x,y] not in [*coords, *water_coords]:
                        water_coords.append([x,y])

        return water_coords

class Field():
    def __init__(self, show_ships, *ships):
        self.ships = ships
        self.result = []
        self.empty_cell = "O"
        self.deck_cell = "■"
        self.wreck_deck_cell = "X"
        self.miss_cell = "T"
        self.show_ships = show_ships

        for i in range(field_size + 1):
            if i == 0:
                self.result.append([" "] + list(range(1, field_size + 1)))
            else:
                self.result.append([i] + [self.empty_cell for j in range(field_size)])

        for ship in self.ships:
            for deck_coords in ship.decks["coords"]:
                self.result[deck_coords[0]][deck_coords[1]] = self.deck_cell

    def shoot(self, x, y):
        global user_turn
        try:
            if self.result[x][y] == self.empty_cell:
                self.result[x][y] = self.miss_cell
                user_turn = not user_turn
            elif self.result[x][y] == self.deck_cell:
                self.result[x][y] = self.wreck_deck_cell
                coords = [x, y]
                ship = [sh for sh in self.ships if coords in sh.decks["coords"]][0]
                si = ship.decks["coords"].index(coords)
                ship.decks["is_wrecked"][si] = True
                if all(ship.decks["is_wrecked"]):
                    for w_coords in ship.water_coords:
                        self.result[w_coords[0]][w_coords[1]] = self.miss_cell
                    self.checkWinner()
        except IndexError:
            print(f"Уфф, ошибка координат. Лучше вводить числа от 1 до {field_size}")
    
    def checkWinner(self):
        global game_end
        if all(map(lambda ship: all(ship.decks["is_wrecked"]), self.ships)):
            game_end = True

    def printField(self):
        output = []
        if self.show_ships:
            output = self.result
        else:
            output = map(lambda row: [self.empty_cell if i == self.deck_cell else i for i in row.copy()], self.result)
            
        for row in output:
            print("|".join(map(str, row)) + "|")

my_ships = [Ship([1,4],[1,5],[1,6]), Ship([3,4],[4,4]), Ship([6,3],[6,4]), Ship([2,2]), Ship([5,1]), Ship([3,6]), Ship([6,6])]
ai_ships = [Ship([1,4],[1,5],[1,6]), Ship([3,4],[4,4]), Ship([6,3],[6,4]), Ship([2,2]), Ship([5,1]), Ship([3,6]), Ship([6,6])]

clear()

print("Сразись с искусственным интеллектом!\n")
print("Вводи номер колонки и строчки по очереди\n")
print("\nА теперь в морской бой!\n")

myField = Field(True, *my_ships)
aiField = Field(False, *ai_ships)

def printFields():
    print("\nТвоя гавань")
    myField.printField()
    print("\nГавань роботов")
    aiField.printField()


while not game_end:
    printFields()

    x = None
    y = None
    if user_turn:
        print("\nТвой ход")
        x = input("Номер строки: ")
        y = input("Номер колонки: ")
        aiField.shoot(int(x), int(y))
    else:
        x = randrange(1, field_size + 1)
        y = randrange(1, field_size + 1)
        myField.shoot(int(x), int(y))
    
    clear()
    
    if game_end:
        printFields()
        if user_turn:
            print("\nВы одержали победу!\n")
        else:
            print("\nК сожалению, победила бездушная машина... F\n")
