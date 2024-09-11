import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QScrollBar, QLabel, QHBoxLayout, QVBoxLayout ,QWidget
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtCore import Qt, Slot

class ColorPickerApplication(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.setWindowTitle('Color Picker')
        self.setWindowIcon(QIcon('color-picker.jpg'))

        ## Initialisation des composants
        fixed_widget_width = 50

        ## Initialisation des composants
        self.__red_control = QScrollBar()
        self.__red_color = QLabel()
        self.__green_control = QScrollBar()
        self.__green_color = QLabel()
        self.__blue_control = QScrollBar()
        self.__blue_color = QLabel()
        self.__mixed_color = QLabel()
        self.__mixed_color.setFixedWidth(fixed_widget_width)

        ## Création des layouts
        red_layout = self.__create_channel('Red', self.__red_control, self.__red_color, fixed_widget_width)
        green_layout = self.__create_channel('Green', self.__green_control, self.__green_color, fixed_widget_width)
        blue_layout = self.__create_channel('Blue', self.__blue_control, self.__blue_color, fixed_widget_width)
        channel_layout = QVBoxLayout()
        channel_layout.addLayout(red_layout)
        channel_layout.addLayout(green_layout)
        channel_layout.addLayout(blue_layout)

        mixed_layout = QHBoxLayout()
        mixed_layout.addLayout(channel_layout)
        mixed_layout.addWidget(self.__mixed_color)

        self.__central_widget = QWidget()
        self.__central_widget.setLayout(mixed_layout)
        self.setCentralWidget(self.__central_widget)

    def __create_channel(self, title_text, control, color, fixed_widget_width):
        title = QLabel()
        value = QLabel()
        
        title.setText(title_text)
        title.setFixedWidth(fixed_widget_width)
        
        control.setRange(0, 255)
        control.setValue(0)
        control.setOrientation(Qt.Horizontal)
        control.setMinimumWidth(2 * fixed_widget_width)
        
        value.setNum(control.value())
        value.setFixedWidth(fixed_widget_width)
        value.setAlignment(Qt.AlignCenter)
        
        color.setFixedWidth(fixed_widget_width)
        
        # Connection signal -> slot
        control.valueChanged.connect(value.setNum)
        control.valueChanged.connect(self.__update_all_colors)
        
        layout = QHBoxLayout()
        layout.addWidget(title)
        layout.addWidget(control)
        layout.addWidget(value)
        layout.addWidget(color)
        
        return layout

    @Slot()
    def __update_all_colors(self):
        r = self.__red_control.value()
        g = self.__green_control.value()
        b = self.__blue_control.value()
        self.__update_single_color(self.__red_color, r, 0, 0)
        self.__update_single_color(self.__green_color, 0, g, 0)
        self.__update_single_color(self.__blue_color, 0, 0, b)
        self.__update_single_color(self.__mixed_color, r, g, b)

    def __update_single_color(self):
        image = QPixmap(self.__red_color.size())
        image.fill(QColor(self.__red_control.value(), 0, 0))
        self.__red_color.setPixmap(image)
    
## Meilleure pratique pour lancer un programme
def main():
    app = QApplication(sys.argv)
    window = ColorPickerApplication()
    window.show()
    sys.exit(app.exec()) # On attend que l'application se termine

## Tout ce qui est en dessous de cette ligne ne sera pas exécuté si on importe ce fichier
## Seulement mettre le main() à l'intérieur d'un if __name__ == '__main__': permet de lancer le programme
if __name__ == '__main__':
    main()