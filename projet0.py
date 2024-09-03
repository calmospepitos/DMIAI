class GOLEngine:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.grid = [[False for _ in range(width)] for _ in range(height)] # On crée une grille de False de la taille width x height
    
    def resize(self, width, height):
        self.__width = width
        self.__height = height
        self.grid = [[False for _ in range(width)] for _ in range(height)]

    def randomize(self):
        pass
    
    def process(self):
        # ticks
        pass

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height
    
    # Getter et setter pour la grille
    @property
    def get_cell(self, x, y):
        return self.grid[y][x]
    
    @get_cell.setter
    def set_cell(self, x, y, value):
        self.grid[y][x] = value