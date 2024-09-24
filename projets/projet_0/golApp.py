import sys 
from GOLEngine import GOLEngine

from PySide6.QtCore import Qt, Slot, QTimer, Signal

from PySide6.QtGui import QImage, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QWidget, QLineEdit, QFormLayout, QGroupBox, QVBoxLayout, QScrollBar

from __feature__ import snake_case, true_property

class ControlWidget(QGroupBox):
    
    startedStopped = Signal()
    
    def __init__(self):
        super().__init__(None)
        
        self.title = "Control"
        
        self.__button_start_stop = QPushButton("Start")
        self.__button_step = QPushButton("One single step")
        self.__speed = QScrollBar()
        self.__speed_title = QLabel()
        
        self.__speed_title.text = (f'{self.__speed.value} px')
        self.__speed.set_range(0,6)
        self.__speed.orientation = Qt.Horizontal
        
        start_stop = self.__create_channel(self.__button_start_stop)
        
        layout_central = QVBoxLayout()
        #layout_central.add_widget(self.__button_start_stop)
        layout_central.add_widget(start_stop)
        layout_central.add_widget(self.__button_step)
        layout_central.add_widget(self.__speed)
        layout_central.add_widget(self.__speed_title)
        self.set_layout(layout_central)
        
        
    def __create_channel(self, control):
        # connection signal -> slot
        control.clicked.connect(self.__start_stop)
        #control.valueChanged.connect(self.__update_all_colors)
        #control.valueChanged.connect(self.__emit_color_changed_signal)
        
        return control
    
    
    def __start_stop(self):
        if self.__running:
            # Si le jeu tourne, on le stoppe
            self.__timer.stop()
            self.__button.text = "Start"
        else:
            # Si le jeu est arrêté, on le démarre          
            self.__timer.start(100) 
            self.__button.text = "Stop"
            print("Largeur:", self.__engine.width, "Hauteur:", self.__engine.height)
            print("Cellules vivantes:", self.__engine.live_cells)
            print("Cellules mortes:", self.__engine.dead_cells)
            print("Itérations:", self.__engine.iterations)
        
        # Bascule l'état du jeu
        self.__running = not self.__running
        

class GOLApp(QMainWindow):
    def __init__(self) :
        super().__init__(None)
        
        self.set_window_title("Game of life")
        
        self.__engine = GOLEngine(300, 300)
        self.__engine.randomize()
 
        # Label pour afficher le jeu
        self.__container = QLabel()
        self.__container.alignment = Qt.AlignCenter
        #self.setCentralWidget(self.__container)
        
         # Bouton
        #self.__button = QPushButton("Start")
        self.__button = ControlWidget()
        #self.__button.clicked.connect(self.__start_stop)
        
         # Layout principal avec le bouton et le label
        layout = QHBoxLayout()
        layout.add_widget(self.__button) 
        layout.add_widget(self.__container) 
        
        # Créer un widget central avec le layout
        central_widget = QWidget()
        central_widget.set_layout(layout)
        self.set_central_widget(central_widget)
         
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
                image.set_pixel_color(x, y, cell_color)
        pixmap = QPixmap.from_image(image) # Conversion du QImage en QPixmap
        self.__container.pixmap = pixmap
    

        

def main():
    app = QApplication(sys.argv)
    window = GOLApp()
    window.show()
    
    result = app.exec()
    sys.exit(result)

if __name__ == '__main__':
    main()
