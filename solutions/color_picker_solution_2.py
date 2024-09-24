# Adapter le color picker à la norme PEP8 de Python.
# actuellement le code suit la norme de Qt
import sys
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
                                QWidget, QLabel, QScrollBar, 
                                QHBoxLayout, QVBoxLayout)
from PySide6.QtGui import QIcon, QPixmap, QColor
from __feature__ import snake_case, true_property

class ColorPickerApplication(QMainWindow):
    
    def __init__(self):
        super().__init__(None)
        
        self.set_window_title('Color picker')
        self.window_icon = QIcon('color_picker_icon.jpg')

        fixed_widget_width = 50
        self.__red_control = QScrollBar()
        self.__red_color = QLabel()
        self.__green_control = QScrollBar()
        self.__green_color = QLabel()
        self.__blue_control = QScrollBar()
        self.__blue_color = QLabel()
        
        self.__mixed_color = QLabel()
        self.__mixed_color.set_fixed_width(fixed_widget_width)
        
        red_layout = self.__create_channel('Red', self.__red_control, self.__red_color, fixed_widget_width)
        green_layout = self.__create_channel('Green', self.__green_control, self.__green_color, fixed_widget_width)
        blue_layout = self.__create_channel('Blue', self.__blue_control, self.__blue_color, fixed_widget_width)
        channel_layout = QVBoxLayout()
        channel_layout.add_layout(red_layout)
        channel_layout.add_layout(green_layout)
        channel_layout.add_layout(blue_layout)

        mixed_layout = QHBoxLayout()
        mixed_layout.add_layout(channel_layout)
        mixed_layout.add_widget(self.__mixed_color)
        
        self.__central_widget = QWidget()
        self.__central_widget.set_layout(mixed_layout)
        
        self.set_central_widget(self.__central_widget)

    def __create_channel(self, title_text, control, color, fixed_widget_width):
        title = QLabel()
        value = QLabel()
        
        title.text = title_text
        title.set_fixed_width(fixed_widget_width)
        
        control.set_range(0, 255)
        control.value = 0
        control.orientation = Qt.Horizontal
        control.minimum_width = 2 * fixed_widget_width
        
        value.set_num(control.value)
        value.set_fixed_width(fixed_widget_width)
        value.alignment = Qt.AlignCenter
        
        color.set_fixed_width(fixed_widget_width)
        
        # connection signal -> slot
        control.valueChanged.connect(value.set_num)
        control.valueChanged.connect(self.__update_all_colors)
        
        layout = QHBoxLayout()
        layout.add_widget(title)
        layout.add_widget(control)
        layout.add_widget(value)
        layout.add_widget(color)
        
        return layout

    @Slot()
    def __update_all_colors(self):
        r = self.__red_control.value
        g = self.__green_control.value
        b = self.__blue_control.value
        self.__update_single_color(self.__red_color, r, 0, 0)
        self.__update_single_color(self.__green_color, 0, g, 0)
        self.__update_single_color(self.__blue_color, 0, 0, b)
        self.__update_single_color(self.__mixed_color, r, g, b)
        
    def __update_single_color(self, label, red_value, green_value, blue_value):
        image = QPixmap(label.size)
        image.fill(QColor(red_value, green_value, blue_value))
        label.pixmap = image

def main():
    app = QApplication(sys.argv)
    
    window = ColorPickerApplication()
    window.show()
    
    sys.exit(app.exec())    
    

if __name__ == '__main__':
    main()
