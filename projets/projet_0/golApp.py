import projet0 as gol
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout

class Jeu(QMainWindow):
    def __init__(self):
        super().__init__(None)
        
        self.setWindowTitle('Game of Life')

        fixed_widget_width = 500
        fixed_widget_height = 500

        self.__game_window = QLabel()
        self.__engine = gol(fixed_widget_width, fixed_widget_height, False)
        
        layout = QVBoxLayout()

        layout.addWidget(self.__game_window)

        self.setCentralWidget()
        
        self.__timer = QTimer(self)
        self.__timer.timeout.connect(gol.process)
        self.__timer.start(100)
        
        self.__running = True


def main():
    app = QApplication(sys.argv)
    window = Jeu()
    window.show()
    sys.exit(app.exec()) 

if __name__ == '__main__':
    main()