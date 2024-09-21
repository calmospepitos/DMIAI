import random
from copy import deepcopy

class GOLEngine:
    def __init__(self, width, height):
        self.__width = None
        self.__height = None
        self.__grid = None 
        self.__temp = None
        self.__iterations = 0 # compteur d'itérations
        
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
          
    def get_cell(self, x, y):
        return self.__grid[x][y]
    
    def set_cell(self, x, y, value):
        self.__grid[x][y] = value
    
    #def clamp(value, minimum, maximum):
        #return max(minimum, min(value, maximum))
    
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
        self.__grid = [[0 for _ in range(self.__height)] for _ in range(self.__width)] 
        #self.__temp = self.__grid.copy()
        self.__temp = deepcopy(self.__grid)
        
        #for x in range(width):
            #self.__grid.append([])
            #self.__temp.append([])
            #for _ in range(height):
                # self.__grid[x].append(random.randint(0, 1))
                #self.__grid[x].append(0)
                #self.__temp[x].append(0)
    
    def randomize(self, percent=0.5):
        for y in range(self.__height):
             for x in range(self.__width):
                 if x != 0 and x != self.__width - 1 and y != 0 and y != self.__height - 1:
                     self.__grid[x][y] = 1 if random.random() > percent else 0
                     #self.__grid[x][y] = int(random.random() > percent)
                
    def process(self):
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                neighbours = sum(self.__grid[x-1][y-1:y+2]) \
                    + sum(self.__grid[x][y-1:y+2:2]) \
                    + sum(self.__grid[x+1][y-1:y+2])
                #neighbours = 0
                #for dx in range(-1, 2):
                    #for dy in range(-1, 2):
                        #if dx != 0 or dy != 0:
                            #neighbours += self.__grid[x+dx][y+dy]  
                #aliveordead = rule[self.__grid[x][y]]   
                #temp = aliveordead[neighbours]
                self.__temp[x][y] = self.__rules[self.__grid[x][y]][neighbours]                  
                #if self.__grid[x][y] == 0: # mort
                    #self.__temp[x][y] = int(neighbours == 3)
                    #self.__temp[x][y] = dead(neighbours == 3)
                #else: # vivant
                    #self.__temp[x][y] = int(neighbours in (2, 3))
                    #self.__temp[x][y] = alive(neighbours in (2, 3))

        #for y in range(self.__height):
        #    for x in range(self.__width):
        #        self.__grid[x][y] = self.__temp[x][y]
        self.__grid, self.__temp = self.__temp, self.__grid

        self.__iterations += 1 # incrémentation du compteur

    @property
    def live_cells(self): # renvoie le nb de cels vivantes
        return sum(cell for row in self.__grid for cell in row)
    
    @property
    def dead_cells(self): #renvoie le nb de cels mortes
        return self.width * self.height - self.live_cells
    
    @property
    def iterations(self): #renvoie le nb d'itérations effectuées
        return self.__iterations

    def print(self):
        for y in range(self.__height):
            for x in range(self.__width):
                print(self.__grid[x][y], end='')
            print()
        print()
        
        
    
def main():
    # Instanciation de la classe
    gol = GOLEngine(2000, 1800)

    # Randomisation de la grille
    gol.randomize()

    #print("Largeur:", gol.width, "Hauteur:", gol.height)
    gol.print()

    gol.process()
    gol.print()

    #print("Cellules vivantes:", gol.live_cells)
    #print("Cellules mortes:", gol.dead_cells)
    gol.process()
    #print("Itérations:", gol.iterations)

if __name__ == '__main__':
    main()
