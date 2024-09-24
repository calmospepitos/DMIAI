# Encapsulation d'un widget autonome
import sys
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
                                QWidget, QLabel, QScrollBar, 
                                QHBoxLayout, QVBoxLayout)
from PySide6.QtGui import QIcon, QPixmap, QColor
from __feature__ import snake_case, true_property

class QColorPicker(QWidget):
    
    colorChanged = Signal(QColor)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        fixed_widget_width = 50
        self.__red_control = QScrollBar()
        self.__red_value = QLabel()
        self.__red_color = QLabel()
        self.__green_control = QScrollBar()
        self.__green_value = QLabel()
        self.__green_color = QLabel()
        self.__blue_control = QScrollBar()
        self.__blue_value = QLabel()
        self.__blue_color = QLabel()
        
        self.__mixed_color = QLabel()
        self.__mixed_color.set_fixed_width(fixed_widget_width)
        
        red_layout = self.__create_channel('Red', self.__red_control, self.__red_value, self.__red_color, fixed_widget_width)
        green_layout = self.__create_channel('Green', self.__green_control, self.__green_value, self.__green_color, fixed_widget_width)
        blue_layout = self.__create_channel('Blue', self.__blue_control, self.__blue_value, self.__blue_color, fixed_widget_width)
        channel_layout = QVBoxLayout()
        channel_layout.add_layout(red_layout)
        channel_layout.add_layout(green_layout)
        channel_layout.add_layout(blue_layout)

        mixed_layout = QHBoxLayout()
        mixed_layout.add_layout(channel_layout)
        mixed_layout.add_widget(self.__mixed_color)
        
        self.set_layout(mixed_layout)
        
    def __create_channel(self, title_text, control, value, color, fixed_widget_width):
        title = QLabel()
        
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
        control.valueChanged.connect(self.__emit_color_changed_signal)
        
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
        
    def __block_scroll_bar_signals(self, block):
        self.__red_control.block_signals(block)
        self.__green_control.block_signals(block)
        self.__blue_control.block_signals(block)
        
    @Slot()
    def __emit_color_changed_signal(self):
        self.colorChanged.emit(self.color)
        
    @property
    def color(self):
        return QColor(self.__red_control.value, self.__green_control.value, self.__blue_control.value)

    @color.setter
    def color(self, value):
        self.__block_scroll_bar_signals(True)
        self.__red_control.value = value.red()
        self.__green_control.value = value.green()
        self.__blue_control.value = value.blue()
        self.__red_value.set_num(self.__red_control.value)
        self.__green_value.set_num(self.__green_control.value)
        self.__blue_value.set_num(self.__blue_control.value)
        self.__update_all_colors()
        self.__block_scroll_bar_signals(False)
        self.__emit_color_changed_signal()

    @Slot()
    def set_color(self, color):
        self.color = color
    
    
    # override implicite de la classe parent QWidget
    def show_event(self, event):
        super().show_event(event)
        self.__update_all_colors()
        
# ------------------------------



class ColorPickerApplication(QMainWindow):
    
    def __init__(self):
        super().__init__(None)
        
        self.set_window_title('Color picker')
        self.window_icon = QIcon('color_picker_icon.jpg')


        central_layout = QVBoxLayout()
        self.__central_widget = QWidget()
        self.__central_widget.set_layout(central_layout)
        
        color_pickers = [QColorPicker() for _ in range(5)]
        
        color_pickers[0].colorChanged.connect(color_pickers[2].set_color)
        color_pickers[2].colorChanged.connect(color_pickers[-1].set_color)
        
        for color_picker in color_pickers:
            central_layout.add_widget(color_picker)
        
        self.set_central_widget(self.__central_widget)


def main():
    app = QApplication(sys.argv)
    
    window = ColorPickerApplication()
    window.show()
    
    sys.exit(app.exec())    
    
    



if __name__ == '__main__':
    main()