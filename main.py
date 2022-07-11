from random import randint

# Sea Battle - The Game

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Уфф, ошибка координат. Лучше вводить числа от 1 до 6"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Эта клетка уже использована. Стреляй по кружочкам!"

class BoardWrongShipException(BoardException):
    pass

class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return f"Dot({self.x}, {self.y})"

class Ship():
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow
        self.orientation = orientation
        # 0 - vertical
        # 1 - horizontal
        self.lives = length
    
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.orientation == 0:
                cur_x += i
            elif self.orientation == 1:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

class Board():
    def __init__(self, is_hidden = False, size = 6):
        self.size = size
        self.board_list = [["O" for i in range(size)] for j in range(size)]
        self.is_hidden = is_hidden
        self.ships = []
        self.death_ships_count = 0
        self.busy = []

    def is_out(self, dot):
        return not((0 <= dot.x < self.size) and (0 <= dot.y < self.size))
    
    def add_ship(self, ship):
        for dot in ship.dots:
            if self.is_out(dot) or dot in self.busy:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.board_list[dot.x][dot.y] = "■"
            self.busy.append(dot)
        
        self.ships.append(ship)
        self.contour(ship)
    
    def contour(self, ship, show = False):
        for dot in ship.dots:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    d_dot = Dot(dot.x + dx, dot.y + dy)
                    if not(self.is_out(d_dot)) and d_dot not in self.busy:
                        if show:
                            self.board_list[d_dot.x][d_dot.y] = "T"
                        self.busy.append(d_dot)
    
    def shot(self, dot):
        if self.is_out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        
        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.board_list[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.death_ships_count += 1
                    self.contour(ship, show = True)
                    print(f"{ship.length}-палубный корабль разбит!")
                    return True
                else:
                    print("Ранил!")
                    return True
        
        self.board_list[dot.x][dot.y] = "T"
        print("Промах")
        return False
    
    def __str__(self):
        output = " |" + "|".join([(str(i)) for i in range(1, self.size+1)]) + "|"
        for i in range(self.size):
            output += f"\n{str(i+1)}|" + "|".join(self.board_list[i]) + "|"
        if self.is_hidden:
            output = output.replace("■", "O")
        return output
    
    def begin(self):
        self.busy = []

class Player():
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board
    
    def ask(self):
        return None
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        while True:
            dot = Dot(randint(0, 5), randint(0, 5))
            if dot not in self.enemy_board.busy:
                print(f"Ход компьютера: {dot.x+1} {dot.y+1}")
                return dot

class User(Player):
    def ask(self):
        while True:
            coords = []
            coords.append(input("Введите номер строки: "))
            coords.append(input("Введите номер столбца: "))

            x = None
            y = None
            try:
                x = int(coords[0])
                y = int(coords[1])
            except ValueError:
                print("Введите числа!")
                continue
            
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        self.lengths = [3, 2, 2, 1, 1, 1, 1]
        self.pl_board = self.random_board()
        self.ai_board = self.random_board()
        self.ai_board.is_hidden = True
        
        self.ai = AI(self.ai_board, self.pl_board)
        self.us = User(self.pl_board, self.ai_board)
    
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        board = Board(size = self.size)
        attempts = 0
        for length in self.lengths:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(length, Dot(randint(0, self.size), randint(0, self.size)), randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("\nСразись с искусственным интеллектом в морском бою!\n")
        print("Как выстрелить по вражескому кораблю?")
        print("Вводи номер строчки и столбца по очереди\n")
        print("А теперь в морской бой!\n")
    
    
    def loop(self):
        num = 0
        while True:
            self.print_boards()
            if num % 2 == 0:
                print("\nВаш ход!")
                repeat = self.us.move()
            else:
                print("\nХодит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.death_ships_count == len(self.lengths):
                self.print_boards()
                print("\nПользователь выиграл!\n")
                break
            
            if self.us.board.death_ships_count == len(self.lengths):
                self.print_boards()
                print("\nК сожалению, выиграла бездушная машина :(\n")
                break
            num += 1
    
    def print_boards(self):
        print("\nТвоя доска:")
        print(self.us.board)
        print("\nДоска компьютера:")
        print(self.ai.board)
            
    def start(self):
        self.greet()
        self.loop()
            
            
game = Game()
game.start()