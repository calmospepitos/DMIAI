import numpy as np
from numpy.typing import NDArray

from gacvm import Domains, ProblemDefinition, Parameters, GeneticAlgorithm
from gaapp import QSolutionToSolvePanel

from uqtwidgets import QImageViewer, create_scroll_real_value

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QSizePolicy, QLabel, QComboBox
from PySide6.QtGui import QImage, QPainter, QColor, QPolygonF, QPen, QTransform
from PySide6.QtCore import Slot, Qt, QSize, QPointF

from __feature__ import snake_case, true_property


class QGeometryProblem(QSolutionToSolvePanel):

    def __init__(self, width : int = 500, height : int = 250, obstacle_count : int = 1, parent : QWidget | None = None) -> None:
        super().__init__(parent)
        self._canvas_width = width
        self._canvas_height = height
        self._obstacle_count = obstacle_count
        
        self._min_obstacle_count = 1
        self._max_obstacle_count = 100
         
        
        # liste des formes 
        self._shapes = {
            "Triangle": QPolygonF([QPointF(0, 0), QPointF(10, 0), QPointF(5, 10)]),
            "Square": QPolygonF([QPointF(0, 0), QPointF(10, 0), QPointF(10, 10), QPointF(0, 10)]),
            "Pentagon": QPolygonF([QPointF(0, 0), QPointF(5, -10), QPointF(10, 0), QPointF(7, 10), QPointF(3, 10)])
        }
        
        # default
        self._polygon = self._shapes["Triangle"]

        # création du scrollbar pour le nombre d'obstacles
        self._value_scroll_bar, value_layout = create_scroll_real_value(
            self._min_obstacle_count, self._obstacle_count, self._max_obstacle_count, 0)

        # Mise en place de la disposition des widgets
        param_group_box = QGroupBox('Parameters')
        param_layout = QFormLayout(param_group_box)
        shape_box = QComboBox()
        # ajoute les formes au combo box
        shape_box.add_items(self._shapes.keys())
        param_layout.add_row('Canvas size', QLabel(f'{self._canvas_width} X {self._canvas_height}')) 
        param_layout.add_row('Obstacle Count', value_layout)
        param_layout.add_row('Shape', shape_box)
        param_group_box.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # slot -> signal
        self._value_scroll_bar.valueChanged.connect(self._update_from_configuration)
        shape_box.currentTextChanged.connect(self._on_shape_selected)

        # create visualization widget and layouting
        visualization_group_box = QGroupBox('Visualization')
        visualization_group_box.size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        visualization_layout = QGridLayout(visualization_group_box)
        self._visualization_widget = QImageViewer(True)
        visualization_layout.add_widget(self._visualization_widget)

        # final layouting
        layout = QVBoxLayout(self)
        layout.add_widget(param_group_box)
        layout.add_widget(visualization_group_box)

        # colors pour les shapes - CHANGER SI NÉCESSAIRE
        self._background_color = QColor(48, 48, 48)
        self._shape_color = QColor(148, 164, 222)
        self._obstacle_color = QColor(255, 255, 0)
        self._best_shape_color = QColor(0, 255, 0, 128)

        # random pour les obstacles
        self._obstacles = self._generate_obstacles()
        #self._polygon = self._default_polygon()

    @property
    def name(self) -> str:
        return 'Name'

    @property
    def summary(self) -> str:
        return "."

    @property
    def description(self) -> str:
        return ''''''

    # get du scroll bar
    @property
    def obstacle_count(self) -> int:
        return self._value_scroll_bar.get_real_value()

    @property
    def problem_definition(self) -> ProblemDefinition:
        def objective_fonction(chromosome: NDArray) -> float:
            x, y, theta, scale = chromosome

            # appliquer les transformations
            transformed_polygon = self._transform_polygon(self._polygon, x, y, theta, scale)

            # hors des limites du canevas ?
            for point in transformed_polygon:
                if not (0 <= point.x() <= self._canvas_width and 0 <= point.y() <= self._canvas_height):
                    return 0.0

            # entre en collision avec un obstacle 
            for obstacle in self._obstacles:
                obstacle_point = QPointF(obstacle[0], obstacle[1]) 
                if transformed_polygon.contains_point(obstacle_point, Qt.WindingFill):
                    return 0.0  

            return self._polygon_area(transformed_polygon)

        domains = Domains(np.array([
            [0, self._canvas_width],          # Translation en x
            [0, self._canvas_height],         # Translation en y
            [0, 360],                         # Rotation (en degrés)
            [0.1, self._canvas_height]        # Mise à l'échelle (homothétie) ???
        ], dtype=float), ('Largeur', 'Hauteur', 'Angle de rotation', 'Homothétie'))
        return ProblemDefinition(domains, objective_fonction)

    # changer si nêcessaire - j'ai juste copié et collé du prof
    @property
    def default_parameters(self) -> Parameters: # note : override
        params = Parameters()
        params.population_size = 30
        params.maximum_epoch = 200
        params.elitism_rate = 0.1
        params.selection_rate = 0.6
        params.mutation_rate = 0.3
        return params

    # fonction random des obstacles
    def _generate_obstacles(self):
        obstacle_count = int(self.obstacle_count) 
        return np.random.rand(obstacle_count, 2) * [self._canvas_width, self._canvas_height]
    
    
    # fonction du prof - matrices
    def _transform_polygon(self, polygon: QPolygonF, x: float, y: float, theta: float, scale: float) -> QPolygonF:
        t = QTransform()
        t.translate(x, y)  # Translation
        t.scale(scale, scale)  # Mise à l'échelle
        t.rotate(theta)  # Rotation (en degrés)

        transformed_polygon = t.map(polygon)  # Appliquer les transformations

        return transformed_polygon


    def _polygon_area(self, polygon: QPolygonF):
        # fonction du prof
        return polygon.bounding_rect().width() * polygon.bounding_rect().height()




    # FONCTIONS POUR DESSINER 
    def _draw_canvas(self, painter, best_polygon=None, population=None):
        """Draw the canvas, obstacles, and polygons."""
        painter.save()
        painter.set_brush(self._background_color)
        painter.set_pen(Qt.NoPen)
        painter.draw_rect(0, 0, self._visualization_widget.width, self._visualization_widget.height)

        # Draw obstacles
        painter.set_brush(self._obstacle_color)
        for obs in self._obstacles:
            painter.draw_rect(obs[0], obs[1], 5, 5)

        # Draw population polygons
        if population:
            painter.set_brush(Qt.NoBrush)
            painter.set_pen(QPen(self._shape_color, 0.5))
            for polygon in population:
                # Assurez-vous que polygon est un QPolygonF
                if isinstance(polygon, QPolygonF):
                    painter.draw_polygon(polygon)
                else:
                    polygon_q = QPolygonF([QPointF(p[0], p[1]) for p in polygon])
                    painter.draw_polygon(polygon_q)

        # Draw the best polygon
        if best_polygon is not None:
            painter.set_brush(self._best_shape_color)
            if isinstance(best_polygon, QPolygonF):
                painter.draw_polygon(best_polygon)
            else:
                best_polygon_q = QPolygonF([QPointF(p[0], p[1]) for p in best_polygon])
                painter.draw_polygon(best_polygon_q)

        painter.restore()



    def _update_from_simulation(self, ga: GeneticAlgorithm | None):
        # image = QImage(QSize(self._canvas_width, self._canvas_height), QImage.Format_ARGB32)
        # image.fill(self._background_color)
        image = self.img()
        painter = QPainter(image)

        try:
            best_polygon = None
            population = None
            if ga:
                best_chromosome = ga.history.best_solution
                best_polygon = self._transform_polygon(self._polygon, *best_chromosome)
                population = [self._transform_polygon(self._polygon, *chrom) for chrom in ga.population]

            self._draw_canvas(painter, best_polygon, population)
        finally:
            painter.end()  # Assurez-vous que le painter est toujours terminé

        self._visualization_widget.image = image
        


    @Slot()
    def _update_from_configuration(self):
        self._obstacles = self._generate_obstacles()
        
        # Redessiner uniquement la forme sélectionnée
        image = self.img()
        painter = QPainter(image)
        # Dessiner la forme actuelle (self._polygon)
        self._draw_canvas(painter, best_polygon=self._polygon)
        painter.end()
        self._visualization_widget.image = image
    
    def _on_shape_selected(self, shape_name: str):
        if shape_name in self._shapes:
            self._polygon = self._shapes[shape_name]
            self._update_from_configuration() 
    
    def img(self):
        image = QImage(QSize(self._canvas_width, self._canvas_height), QImage.Format_ARGB32)
        image.fill(self._background_color)
        return image