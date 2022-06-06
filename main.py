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
history = []

cell_empty = "O"
cell_deck = "■"
cell_wreck_deck = "X"
cell_miss = "T"

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
        self.show_ships = show_ships

        for i in range(field_size + 1):
            if i == 0:
                self.result.append([" "] + list(range(1, field_size + 1)))
            else:
                self.result.append([i] + [cell_empty for j in range(field_size)])

        for ship in self.ships:
            for deck_coords in ship.decks["coords"]:
                self.result[deck_coords[0]][deck_coords[1]] = cell_deck

    def shoot(self, x, y):
        global user_turn
        prefix = "-> " if user_turn else "-> [робот] "
        try:
            if self.result[x][y] == cell_empty:
                self.result[x][y] = cell_miss
                if user_turn:
                    history.clear()
                history.append(f"{prefix}Снаряд попал мимо цели")
                user_turn = not user_turn
            elif self.result[x][y] == cell_miss:
                history.append("Повнимательней. На этой клетке уже точно пусто. Стреляй по кружочкам")
            elif self.result[x][y] == cell_wreck_deck:
                history.append("Здесь лишь обломки корабля. Стреляй по кружочкам")
            elif self.result[x][y] == cell_deck:
                history.append(f"{prefix}Точное попадание!")
                self.result[x][y] = cell_wreck_deck
                coords = [x, y]
                ship = [sh for sh in self.ships if coords in sh.decks["coords"]][0]
                si = ship.decks["coords"].index(coords)
                ship.decks["is_wrecked"][si] = True
                if all(ship.decks["is_wrecked"]):
                    for w_coords in ship.water_coords:
                        self.result[w_coords[0]][w_coords[1]] = cell_miss
                    history.append(f"{prefix}{ship.length}-палубный корабль разбит")
                    self.checkWinner()
        except IndexError:
            history.append(f"Уфф, ошибка координат. Лучше вводить числа от 1 до {field_size}")
    
    def checkWinner(self):
        global game_end
        if all(map(lambda ship: all(ship.decks["is_wrecked"]), self.ships)):
            game_end = True

    def printField(self):
        output = []
        if self.show_ships:
            output = self.result
        else:
            output = map(lambda row: [cell_empty if i == cell_deck else i for i in row.copy()], self.result)
            
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
    print("")


while not game_end:
    printFields()

    x = None
    y = None
    
    for line in history:
        print(line)
    if user_turn:
        print("\nТвой ход")
        x = input("Номер строки: ")
        y = input("Номер колонки: ")
        if x and y:
            aiField.shoot(int(x), int(y))
        else:
            history.append(f"Уфф, ошибка координат. Лучше вводить числа от 1 до {field_size}")
    else:
        x = 0
        y = 0
        while not myField.result[x][y] == cell_empty and not myField.result[x][y] == cell_deck:
            x = randrange(1, field_size + 1)
            y = randrange(1, field_size + 1)
        myField.shoot(int(x), int(y))
    
    clear()
    
    if game_end:
        printFields()
        if user_turn:
            print("\nВы одержали победу!")
        else:
            print("\nК сожалению, победила бездушная машина... F")
