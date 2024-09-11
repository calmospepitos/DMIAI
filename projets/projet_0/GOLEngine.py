import random

class GOLEngine:
    def __init__(self, width, height, i):
        self.__width = width
        self.__height = height
        self.__grid = [[i for _ in range(height)] for _ in range(width)] 
        self.__temp = self.__grid.copy()
        self.__iterations = 0 # compteur d'itérations

    @property
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        self.__height = value
          
    def get_cell(self, x, y):
        return self.__grid[x][y]
    
    def set_cell(self, x, y, value):
        self.__grid[x][y] = value
    
    def clamp(value, minimum, maximum):
        return max(minimum, min(value, maximum))
    
    def resize(self, width, height, i):
        self.__width = GOLEngine.clamp(width, 3, 2500)
        self.__height = GOLEngine.clamp(height, 3, 2500)
        self.__grid = [[i for _ in range(height)] for _ in range(width)] 
        self.__temp = self.__grid.copy()
        
        for x in range(width):
            self.__grid.append([])
            self.__temp.append([])
            for _ in range(height):
                # self.__grid[x].append(random.randint(0, 1))
                self.__grid[x].append(0)
                self.__temp[x].append(0)
    
    def randomize(self, percent=0.5):
        for y in range(self.__height):
             for x in range(self.__width):
                 if x != 0 and x != self.__width - 1 and y != 0 and y != self.__height - 1:
                     self.__grid[x][y] = 1 if random.random() > percent else 0
                     self.__grid[x][y] = int(random.random() > percent)
                
    def process(self):
        for x in range(1, self.__width-1):
            for y in range(1, self.__height-1):
                neighbors = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx != 0 or dy != 0:
                            neighbors += self.__grid[x+dx][y+dy]                   
                if self.__grid[x][y] == 0: # mort
                    self.__temp[x][y] = int(neighbors == 3)
                else: # vivant
                    self.__temp[x][y] = int(neighbors in (2, 3))

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
    gol = GOLEngine(12, 8, 0)

    # Randomisation de la grille
    gol.randomize()

    print("Largeur:", gol.width, "Hauteur:", gol.height)
    gol.print()

    gol.process()
    gol.print()

    print("Cellules vivantes:", gol.live_cells)
    print("Cellules mortes:", gol.dead_cells)
    gol.process()
    print("Itérations:", gol.iterations)

if __name__ == '__main__':
    main()