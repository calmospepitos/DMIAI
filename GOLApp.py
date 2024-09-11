import sys 
from GOLEngine import GOLEngine

from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QWidget

class GOLApp(QMainWindow):
    def __init__(self) :
        super().__init__(None)
        
        self.setWindowTitle("Game of life")
        
        self.__engine = GOLEngine(250, 200, 0)
        self.__engine.randomize()
        
        # Label pour afficher le jeu
        self.__container = QLabel()
        self.__container.setAlignment(Qt.AlignCenter)
        #self.setCentralWidget(self.__container)
        
         # Bouton
        self.__button = QPushButton("Start")
        self.__button.clicked.connect(self.__start_stop)
        
         # Layout principal avec le bouton et le label
        layout = QHBoxLayout()
        layout.addWidget(self.__button) 
        layout.addWidget(self.__container) 
        
        # Créer un widget central avec le layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
         
           # Timer
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__process_game)
        #self.__timer.start(100)
        
        self.__running = False  # Indicateur de l'état du jeu
    
    @Slot()
    def __process_game(self):
        self.__engine.process()
        self.__update()
        
    def __update(self):
        black_color = QColor(0, 0, 0)
        white_color = QColor(255, 255, 255)
        image = QImage(self.__engine.width, self.__engine.height, QImage.Format_ARGB32)
        for x in range(self.__engine.width):
            for y in range(self.__engine.height):
                cell_color = white_color if self.__engine.get_cell(x, y) else black_color
                image.setPixelColor(x, y, cell_color)
        pixmap = QPixmap.fromImage(image) # Conversion du QImage en QPixmap
        self.__container.setPixmap(pixmap)
    
    def __start_stop(self):
        if self.__running:
            # Si le jeu tourne, on le stoppe
            self.__timer.stop()
            self.__button.setText("Start")
        else:
            # Si le jeu est arrêté, on le démarre
            self.__timer.start(100) 
            self.__button.setText("Stop")
            print("Largeur:", self.__engine.width, "Hauteur:", self.__engine.height)
            print("Cellules vivantes:", self.__engine.live_cells)
            print("Cellules mortes:", self.__engine.dead_cells)
            print("Itérations:", self.__engine.iterations)
        
        # Bascule l'état du jeu
        self.__running = not self.__running
        

def main():

    app = QApplication(sys.argv)
    window = GOLApp()
    window.show()
    
    result = app.exec()
    sys.exit(result)

if __name__ == '__main__':
    main()