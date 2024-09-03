import random

class GOLEngine:
    def __init__(self, width, height, i):
        self.__width = width
        self.__height = height
        self.__grid = [[i for _ in range(width)] for _ in range(height)] # On crée une grille de False de la taille width x height
        self.__temp = self.__grid.copy()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
    
    @width.setter
    def width(self, value):
        self.__width = value
    
    @height.setter
    def height(self, value):
        self.__height = value
    
    def get_cell(self, x, y):
        return self.__grid[y][x]
    
    def set_cell(self, x, y, value):
        self.__grid[y][x] = value

    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))
    
    def resize(self, width, height, i):
        self.__width = GOLEngine.clamp(width, 3, 2500)
        self.__height = GOLEngine.clamp(height, 3, 2500)
        self.__grid = [[i for _ in range(width)] for _ in range(height)]

    def randomize(self):
        for y in range(self.height):
            for x in range(self.width):
                GOLEngine.set_cell(self, x, y, random.choice([True, False]))
    
    def process(self):
        for y in range(self.height):
            for x in range(self.width):
                neighbors = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        if self.get_cell(x + dx, y + dy):
                            neighbors += 1
                if self.get_cell(x, y):
                    self.__temp[y][x] = neighbors == 2 or neighbors == 3
                else:
                    self.__temp[y][x] = neighbors == 3

        for y in range(self.height):
            for x in range(self.width):
                self.__grid[y][x] = self.__temp[y][x]

# Instanciation de la classe
gol = GOLEngine(10, 10, False)

# Randomisation de la grille
gol.randomize()

#Test de la grille
#for y in range(gol.height):
#    for x in range(gol.width):
#        print(gol.get_cell(x, y), end=' ')
#    print()
#
#print(gol.width, gol.height)