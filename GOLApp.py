import sys 
from GOLEngine import GOLEngine

from PySide6.QtCore import Qt, Slot, QTimer
from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class GOLApp(QMainWindow):
    def __init__(self) :
        super().__init__(None)
        
        self.setWindowTitle("Game of life")
        
        self.__engine = GOLEngine(250, 200, 0)
        self.__engine.randomize()
        
        self.__container = QLabel()
        self.__container.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.__container)
         
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__process_game)
        self.__timer.start(100)
    
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
        

def main():

    app = QApplication(sys.argv)
    window = GOLApp()
    window.show()
    
    result = app.exec()
    sys.exit(result)

if __name__ == '__main__':
    main()