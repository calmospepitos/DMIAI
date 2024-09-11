# Moteur de jeu de la vie (Game Of Life).
#
# Version préliminaire simple et fonctionnelle.
#
# Cette implémentation respecte l'encapsulation et l'utilisaiton des propriétés.
#
# Toutefois, elle est sans :  
#  - documentation
#  - tests
#  - optimisation
#  - interface graphique (c'est souhaité puisque c'est le moteur)


import random

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

class GOLEngine:
    def __init__(self, width, height):
        self.__width = None
        self.__height = None
        self.__grid = None
        self.__temp = None
        
        self.resize(width, height)
    
    @property
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, value):
        self.resize(value, self.__height)
    
    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.resize(self.__width, value)
        
    def get_cell_value(self, x, y):
        # no input validation for performance consideration
        return self.__grid[x][y]
        
    def set_cell_value(self, x, y, value):
        # no input validation for performance consideration
        self.__grid[x][y] = value
        
    
    def resize(self, width, height):
        # if width < 3 or height < 3:
        #     raise ValueError('width and height must be greater or equal to 3.')

        self.__width = clamp(width, 3, 2500)
        self.__height = clamp(height, 3, 2500)
        self.__grid = []
        self.__temp = []
        
        for x in range(width):
            self.__grid.append([])
            self.__temp.append([])
            for _ in range(height):
                # self.__grid[x].append(random.randint(0, 1))
                self.__grid[x].append(0)
                self.__temp[x].append(0)

    def randomize(self, percent=0.5):
        # for y in range(self.__height):
        #     for x in range(self.__width):
        #         if x != 0 and x != self.__width - 1 and y != 0 and y != self.__height - 1:
        #             self.__grid[x][y] = 1 if random.random() > percent else 0
        #             self.__grid[x][y] = int(random.random() > percent)
        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):
                self.__grid[x][y] = int(random.random() > percent)
        
    def process(self):
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                neighbours = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        if i != 0 or j != 0:
                            # neighbours += 1 if world[x+i][y+j] == 1 else 0
                            neighbours += self.__grid[x+i][y+j]
                if self.__grid[x][y] == 0: # mort
                    # self.__temp[x][y] = 1 if neighbours == 3 else 0
                    self.__temp[x][y] = int(neighbours == 3)
                else: # vivant
                    # temp[x][y] = 1 if neighbours == 2 or neighbours == 3 else 0
                    # self.__temp[x][y] = 1 if neighbours in (2, 3) else 0
                    self.__temp[x][y] = int(neighbours in (2, 3))
                    
        # for y in range(self.__height):
        #     for x in range(self.__width):
        #         self.__world[x][y] = self.__temp[x][y]

        # from copy import deepcopy
        # self.__world = deepcopy(self.__temp)
        self.__grid, self.__temp = self.__temp, self.__grid
    
    def print(self):
        for y in range(self.__height):
            for x in range(self.__width):
                print(self.__grid[x][y], end='')
            print()
        print()
    
    
    
    
    
# quelques tests simples    
def main():
    gol_engine = GOLEngine(12, 8)
    
    gol_engine.randomize()
    print(f'World {gol_engine.width} x {gol_engine.height}')
    gol_engine.print()
    
    gol_engine.process()
    gol_engine.print()
    
    
    gol_engine.width = 100
    gol_engine.process()
    gol_engine.resize(100, 100)


if __name__ == '__main__':
    main()
    

