import random
from copy import deepcopy

# Ajoute quelques optimisations :
# - utilisation de la fonction sum pour calculer le nombre de voisins vivants
# - utilisation d'une LUT pour gérer les règles de vie et de mort


class GOLEngine:
    def __init__(self, width, height):
        self.__width = None
        self.__height = None
        self.__world = None
        self.__temp = None
        # Concept de table de recherche (LUT : Look-Up Table)
        # Indique si une cellule est morte ou vivante directement
        # à partir de l'index. À l'index i se trouve le nombre de 
        # voisins vivants (Nvoisins) : 
        #    Nvoisins -----> 0  1  2  3  4  5  6  7  8
        #                    |  |  |  |  |  |  |  |  | 
        #                    v  v  v  v  v  v  v  v  v  
        self.__alive_rule = (0, 0, 1, 1, 0, 0, 0, 0, 0)
        self.__dead_rule  = (0, 0, 0, 1, 0, 0, 0, 0, 0)
        self.__rules = (self.__dead_rule, self.__alive_rule)
        
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
        
    def cell_value(self, x, y):
        # pour des raisons de performance, aucune validation des intrants
        return self.__world[x][y]
        
    def set_cell_value(self, x, y, value):
        # pour des raisons de performance, aucune validation des intrants
        self.__world[x][y] = value
    
    def __validate_size(self, size):
        if not isinstance(size, int):
            raise TypeError('size must be an int')
        if not(3 <= size <= 2000):
            raise ValueError('size must be between 3 and 2000')
    
    def resize(self, width, height):
        # l'importance de cette fonction justifie ces étapes de validation
        # => mettre l'importance sur l'interface de programmation
        # => on veut indiquer le plus précocement possible les problèmes potentiels
        self.__validate_size(width)
        self.__validate_size(height)
        
        self.__width = width
        self.__height = height
        self.__world = [[0 for _ in range(self.__height)] for _ in range(self.__width)]
        self.__temp = deepcopy(self.__world)

    def randomize(self, percent=0.5):
        for y in range(1, self.__height - 1):
            for x in range(1, self.__width - 1):
                self.__world[x][y] = int(random.random() > percent)
        
    def process(self):
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                neighbours = sum(self.__world[x-1][y-1:y+2]) \
                           + sum(self.__world[x][y-1:y+2:2]) \
                           + sum(self.__world[x+1][y-1:y+2])

                self.__temp[x][y] = self.__rules[self.__world[x][y]][neighbours]
                    
        self.__world, self.__temp = self.__temp, self.__world