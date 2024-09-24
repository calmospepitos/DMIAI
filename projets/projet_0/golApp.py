    import sys 
    from GOLEngine import GOLEngine

    from PySide6.QtCore import Qt, QTimer, Signal

    from PySide6.QtGui import QImage, QPixmap, QColor
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QWidget, QGroupBox, QVBoxLayout, QScrollBar, QComboBox, QSpacerItem, QSizePolicy

    from __feature__ import snake_case, true_property



    class ControlWidget(QGroupBox):
        # signal pour chacun des bouttons
        startedStopped = Signal() # boutton start / stop
        stepRequested = Signal() # boutton One single step
        speedChanged = Signal(int) # boutton scroll bar speed
        
        def __init__(self):
            super().__init__(None)
            
            self.title = "Control"
            
            # buttons et options
            self.__button_start_stop = QPushButton("Start")
            self.__button_step = QPushButton("One single step")
            self.__button_step.enabled = True
            # au lieu de faire : self.__speed.orientation = Qt.Horizontal
            self.__speed = QScrollBar(Qt.Horizontal)
            self.__speed.set_range(1,6)
            self.__speed.value = 1
            self.__speed_label = QLabel("1x")
            self.__speed_label.alignment = Qt.AlignCenter
            
            # connection signal -> slot
            self.__button_start_stop.clicked.connect(self.__toggle_start_stop)
            self.__button_step.clicked.connect(self.__request_step)
            self.__speed.valueChanged.connect(self.__update_speed)
            
            # layout central
            layout_central = QVBoxLayout()
            layout_central.add_widget(self.__button_start_stop)
            layout_central.add_widget(self.__button_step)
            layout_central.add_widget(self.__speed)
            layout_central.add_widget(self.__speed_label)
            self.set_layout(layout_central)
            
            self.__running = False  # Indicateur de l'état du jeu
        
        # fonctions pour connection / emission signal avec GOLApp
        def __toggle_start_stop(self):
            if self.__running:
                self.__button_start_stop.text = "Start"
                self.__button_step.enabled = True
            else:
                self.__button_start_stop.text = "Stop"
                self.__button_step.enabled = False
            
            self.__running = not self.__running

            # emmission d'un signal à la classe principale
            # self. nom de signal + .emit()
            self.startedStopped.emit()
        
        def __request_step(self):
            # emmission d'un signal à la classe principale
            # self. nom de signal + .emit()
            self.stepRequested.emit()
        
        def __update_speed(self):
            self.__speed_label.text = f"{self.__speed.value}x"
            # emmission d'un signal à la classe principale
            # self. nom de signal + .emit()
            self.speedChanged.emit(self.__speed.value)
            




    class InformationWidget(QGroupBox):  
        def __init__(self):
            super().__init__(None)
            
            self.title = "Informations"
            
            self.__generation = QLabel("Generation : 0")
            self.__cell_count = QLabel("Cell count : 0")
            self.__dead = QLabel("Dead : 0 (0.0 %)")
            self.__alive = QLabel("Alive : 0 (0.0 %)")
         
            # connection signal -> slot

            
            # layout central
            layout_central = QVBoxLayout()
            layout_central.add_widget(self.__generation)
            layout_central.add_widget(self.__cell_count)
            layout_central.add_widget(self.__dead)
            layout_central.add_widget(self.__alive)
            self.set_layout(layout_central)
        
        def update_informations(self, generation, total_cells, dead_cells, alive_cells):
            self.__generation.text = f"Generation: {generation:^20}"
            self.__cell_count.text = f"Cell count: {total_cells:^20}"
            self.__dead.text = f"Dead: {dead_cells} ({round(dead_cells/total_cells*100, 1)}%)"
            self.__alive.text = f"Alive: {alive_cells} ({round(alive_cells/total_cells*100, 1)}%)"

        
        
        
        
    class PatternWidget(QGroupBox):
        # signal pour chacun des bouttons
        randomize = Signal(float)
        setDead = Signal() 
        setAlive = Signal() 
        
        def __init__(self):
            super().__init__(None)
            
            self.title = "Pattern"
            
            self.__randomize = QScrollBar(Qt.Horizontal)
            self.__randomize.set_range(0,100)
            self.__randomize.value = 50
            self.__randomize_button = QPushButton()
            self.__randomize_button.text = f"Randomize {self.__randomize.value}%"
            self.__button_all_dead = QPushButton("Set all dead")
            self.__button_all_alive = QPushButton("Set all alive")
            
            # connection signal -> slot
            self.__randomize_button.clicked.connect(self.__randomize_all)
            self.__button_all_dead.clicked.connect(self.__all_dead)
            self.__button_all_alive.clicked.connect(self.__all_alive)
            self.__randomize.valueChanged.connect(self.__update_randomize_button)
            
            # layout central
            layout_central = QVBoxLayout()
            layout_central.add_widget(self.__randomize)
            layout_central.add_widget(self.__randomize_button)
            layout_central.add_widget(self.__button_all_dead)
            layout_central.add_widget(self.__button_all_alive)
            self.set_layout(layout_central)
        
         # fonctions pour connection / emission signal avec GOLApp
        def __randomize_all(self):
            self.randomize.emit(self.__randomize.value / 100.0)
        
        def __all_dead(self):
            self.setDead.emit()
        
        def __all_alive(self):
            self.setAlive.emit()
        
        def __update_randomize_button(self):
            self.__randomize_button.text = f"Randomize {self.__randomize.value}%"





    class ParametersWidget(QGroupBox):  
        # signal pour chacun des parameters
        mapSize = Signal(int, int) # map size
        
        def __init__(self):
            super().__init__(None)
            
            self.title = "Parameters"
            
            self.__map_size = QComboBox()
            self.__map_size_text = QLabel("Map size")
            self.__map_size.add_items(["100 x 100", "200 x 200", "300 x 300", "400 x 400", "500 x 500"])
            self.__rule_text = QLabel("Rule")
            
            # connection signal -> slot
            self.__map_size.currentIndexChanged.connect(self.__map_size_change)
            
            # layout central
            layout_central = QVBoxLayout()
            layout_central.add_widget(self.__map_size_text)
            layout_central.add_widget(self.__map_size)
            layout_central.add_widget(self.__rule_text)
            self.set_layout(layout_central)
        
        def __map_size_change(self, index):
            # fonction combo box map size change
            if index == 0:
                self.mapSize.emit(100, 100)
            elif index == 1:
                self.mapSize.emit(200, 200)
            elif index == 2:
                self.mapSize.emit(300, 300)
            elif index == 3:
                self.mapSize.emit(400, 400)
            elif index == 4:
                self.mapSize.emit(500, 500)
            

        

            

        


        

            

    class GOLApp(QMainWindow):
        def __init__(self) :
            super().__init__(None)
            
            self.set_window_title("Game of life")
            
            self.__engine = GOLEngine(100, 100) 
            self.__engine.randomize()
            
            # Label pour afficher le jeu
            self.__container = QLabel()
            self.__container.alignment = Qt.AlignCenter
            
            # création widgets
            self.__control_widget = ControlWidget()
            self.__informations_widget = InformationWidget()
            self.__pattern_widget = PatternWidget()
            self.__parameters_widget = ParametersWidget()
            
            # connection slots <- signal
            self.__control_widget.startedStopped.connect(self.__start_stop)
            self.__control_widget.stepRequested.connect(self.__one_step)
            self.__control_widget.speedChanged.connect(self.__change_speed)
            
            self.__pattern_widget.randomize.connect(self.__new_randomize)
            self.__pattern_widget.setDead.connect(self.__all_rip)
            self.__pattern_widget.setAlive.connect(self.__all_born)
            
            self.__parameters_widget.mapSize.connect(self.__resize_game)
            
            
            ##### timer ################
            self.__timer = QTimer(self)
            self.__timer.timeout.connect(self.__process_game)
            self.__speed = 100
            
            self.__running = False
            
            
            ######LAYOUTS##########
             # Layout 1 
            layout_1 = QVBoxLayout()
            layout_1.add_widget(self.__control_widget)
            layout_1.add_widget(self.__parameters_widget)
            
            # Layout 2
            layout_2 = QVBoxLayout()
            layout_2.add_widget(self.__pattern_widget)
            
            # Layout 3
            layout_3 = QVBoxLayout()
            layout_3.add_widget(self.__informations_widget)
            
            # Main Layout
            main_layout = QHBoxLayout()
            main_layout.add_layout(layout_1)
            main_layout.add_layout(layout_2)
            main_layout.add_widget(self.__container)
            main_layout.add_layout(layout_3)
                  
                  
        
            ###### CENTRAL WIDGET #########        
            # Créer un widget central avec le layout
            central_widget = QWidget()
            central_widget.set_layout(main_layout)
            self.set_central_widget(central_widget)




        
        ######## FONCTIONS CONTROL WIDGET ########    
        def __start_stop(self):
            if self.__running:
                self.__timer.stop()
            else:
                self.__timer.start(self.__speed)
            self.__running = not self.__running
        
        def __one_step(self):
            if not self.__running: 
                self.__process_game()
        
        def __change_speed(self, value):
            if self.__running:
                self.__timer.start(self.__speed/value) 
        
            
        
        
        ######## FONCTIONS PATTERN WIDGET ########    
        def __new_randomize(self, value):
            self.__engine.randomize(value)
            self.__update()
        
        def __all_rip(self):
            for y in range(self.__engine.height):
                for x in range(self.__engine.width):
                    self.__engine.set_cell(x, y, 0) 
            self.__update()
        
        def __all_born(self):
            for y in range(self.__engine.height):
                for x in range(self.__engine.width):
                    self.__engine.set_cell(x, y, 1) 
            self.__update()
        




        ######## FONCTION PARAMETERS WIDGET ########   
        def __resize_game(self, width, height):
            self.__engine = GOLEngine(width, height)
            self.__engine.randomize()
            self.__update()
        
        
        
        
        
        
        ######## GENERAL GAME FUNCTIONS ########         
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
            
            # update informations
            generation = self.__engine.iterations
            total_cells = self.__engine.live_cells + self.__engine.dead_cells
            dead_cells = self.__engine.dead_cells
            alive_cells = self.__engine.live_cells
            self.__informations_widget.update_informations(generation, total_cells, dead_cells, alive_cells)
           

    def main():
        app = QApplication(sys.argv)
        window = GOLApp()
        window.show()
        
        result = app.exec()
        sys.exit(result)

    if __name__ == '__main__':
        main()
