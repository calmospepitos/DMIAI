import numpy as np
from numpy.typing import NDArray

from gacvm import Domains, ProblemDefinition, Parameters, GeneticAlgorithm
from gaapp import QSolutionToSolvePanel

from uqtwidgets import QImageViewer, create_scroll_real_value

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QSizePolicy, QLabel
from PySide6.QtGui import QImage, QPainter, QColor, QPolygonF, QPen, QTransform, QBrush
from PySide6.QtCore import Slot, Qt, QSize, QPointF

from __feature__ import snake_case, true_property


class QCamera(QSolutionToSolvePanel):

    def __init__(self, width: int = 500, height: int = 250, nb_cameras: int = 1, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._canvas_width = width
        self._canvas_height = height
        self._nb_cameras = nb_cameras
        self._min_cameras = 1
        self._max_cameras = 5
        self._min_fov_layout = 60
        self._max_fov_layout = 120
        self._min_fov = 30
        self._max_fov = 180
        
        # scroll bar pour les cameras
        self._camera_scroll_bar, camera_layout = create_scroll_real_value(
            self._min_cameras, self._nb_cameras, self._max_cameras, 0)
        
        # scroll bar pour les fovs
        self._min_fov_scroll_bar, min_fov_layout = create_scroll_real_value(self._min_fov, self._min_fov_layout, self._max_fov, 0, value_suffix="°")
        self._max_fov_scroll_bar, max_fov_layout = create_scroll_real_value(self._min_fov, self._max_fov_layout, self._max_fov, 0, value_suffix="°")

        param_group_box = QGroupBox('Parameters')
        param_layout = QFormLayout(param_group_box)
        param_layout.add_row('Canvas size', QLabel(f'{self._canvas_width} x {self._canvas_height}'))
        param_layout.add_row('Number of Cameras', camera_layout)
        param_layout.add_row("Min FOV", min_fov_layout)
        param_layout.add_row("Max FOV", max_fov_layout)
        param_group_box.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
        # slot -> signal
        self._camera_scroll_bar.valueChanged.connect(self._update_camera_count)
        self._min_fov_scroll_bar.valueChanged.connect(self._update_fov_limits)
        self._max_fov_scroll_bar.valueChanged.connect(self._update_fov_limits)

        # visualisation
        visualization_group_box = QGroupBox('Visualization')
        visualization_group_box.size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        visualization_layout = QGridLayout(visualization_group_box)
        self._visualization_widget = QImageViewer(True)
        visualization_layout.add_widget(self._visualization_widget)

        # layout principal
        layout = QVBoxLayout(self)
        layout.add_widget(param_group_box)
        layout.add_widget(visualization_group_box)

        # colors pour les shapes - CHANGER SI NÉCESSAIRE
        self._background_color = QColor(48, 48, 48)
        self._camera_color = QColor(255, 0, 0)
        self._coverage_color = QColor(0, 255, 0, 128)

    @property
    def name(self) -> str:
        return "Camera"

    @property
    def summary(self) -> str:
        return "Camera."

    @property
    def description(self) -> str:
        return """
        Camera.
        """
    
    # @property
    # def obstacle_count(self) -> int:
    #     return 0

    @property
    def problem_definition(self) -> ProblemDefinition:
        def objective_fonction(chromosome: NDArray) -> float:
            
            # Objectif : Maximiser la couverture du terrain avec le minimum de recouvrement inutile.
            
            # Chaque chromosome représente une caméra sous la forme :
            # x, y : Position de la caméra sur le terrain.
            # theta : Orientation de la caméra (en degrés).
            # fov : Champ de vision (Field of View) de la caméra en degrés.
            
            # initializer coverage map
            coverage_map = np.zeros((self._canvas_width, self._canvas_height), dtype=int)
            
            # paramètres de toutes les caméras
            cameras = chromosome.reshape(self._nb_cameras, 4)  # Chaque ligne : [x, y, theta, fov]
            
            # grille de coordonnées pour chaque pixel du terrain
            grid_x, grid_y = np.meshgrid(np.arange(self._canvas_width), np.arange(self._canvas_height))
            
            # calcule les pixels couverts par la caméra
            dx = grid_x[:, :, np.newaxis] - cameras[:, 0]
            dy = grid_y[:, :, np.newaxis] - cameras[:, 1]
            # calcule l'angle en radians entre le vecteur (dx, dy) et l'axe des x (horizontal) et transforme les radians en degrés
            # % 360 => force à 360°
            angles_to_pixels = np.degrees(np.arctan2(dy, dx)) % 360
            # calcule l'angle relatif d'un pixel par rapport à l'orientation de la caméra.
            relative_angles = (angles_to_pixels - cameras[:, 2] + 360) % 360
            
            # mask pour les pixels dans le fov
            in_fov = (relative_angles <= cameras[:, 3] / 2) | (relative_angles >= 360 - cameras[:, 3] / 2)
            
            # m-à-j la carte de couverture
            coverage_map = np.any(in_fov, axis=-1).astype(int)
            
            # calcule la couverture totale
            total_coverage = np.sum(coverage_map)
            return total_coverage / (self._canvas_width * self._canvas_height)

        # domaine
        # Position limitée aux dimensions du terrain.
        # Champ de vision limité (entre 60° et 120° ??).
        domains = Domains(
            np.array([
                [0, self._canvas_width],  # x
                [0, self._canvas_height],  # y
                [0, 360],  # orientation (theta)
                [self._min_fov, self._max_fov]  # field of view (fov)
            ] * self._nb_cameras, dtype=float),
            [f'Camera {i + 1} {param}' for i in range(self._nb_cameras) for param in ('x', 'y', 'theta', 'fov')]
        )
        return ProblemDefinition(domains, objective_fonction)

    @property
    def default_parameters(self) -> Parameters:
        params = Parameters()
        params.population_size = 30
        params.maximum_epoch = 100
        params.elitism_rate = 0.1
        params.selection_rate = 0.6
        params.mutation_rate = 0.3
        return params

    @Slot()
    def _update_camera_count(self):
        self._nb_cameras = int(self._camera_scroll_bar.get_real_value())
        self._update_from_simulation(None)
    
    @Slot()
    def _update_fov_limits(self):
        self._min_fov = self._min_fov_scroll_bar.get_real_value()
        self._max_fov = self._max_fov_scroll_bar.get_real_value()

        if self._min_fov >= self._max_fov:
            self._max_fov = self._min_fov + 1
            self._max_fov_scroll_bar.set_real_value(self._max_fov)

        self._update_from_simulation(None)

    
    
    
    # fonction du prof - matrices
    def _transform_camera(self, x: float, y: float, theta: float, fov: float) -> QPolygonF:

        t = QTransform()
        t.translate(x, y)  # Translation
        #t.scale(scale, scale)  # Mise à l'échelle
        t.rotate(theta)  # Rotation (en degrés)

        # define the FOV as a triangle
        fov_sector = QPolygonF([
            QPointF(0, 0),  # Origin
            QPointF(1000, -np.tan(np.radians(fov / 2)) * 1000),  # left edge 
            QPointF(1000, np.tan(np.radians(fov / 2)) * 1000),   # right edge
        ])

        return t.map(fov_sector) # Appliquer les transformations




    # fonctions pour dessiner
    def _draw_canvas(self, painter, best_solution=None):

        painter.save()
        painter.set_brush(self._background_color)
        painter.set_pen(Qt.NoPen)
        painter.draw_rect(0, 0, self._canvas_width, self._canvas_height)
        #painter.draw_rect(0, 0, self._visualization_widget.width, self._visualization_widget.height)

        painter.scale(self._visualization_widget.width / self._canvas_width, self._visualization_widget.height / self._canvas_height)
        # painter.scale(self._canvas_width, self._canvas_height)

        # dessiner les caméras
        if best_solution is not None:
            cameras = best_solution.reshape(self._nb_cameras, 4)
            x_position, y_position, theta, fov = cameras[:, 0], cameras[:, 1], cameras[:, 2], cameras[:, 3]

            painter.set_pen(QPen(self._camera_color))
            painter.set_brush(QBrush(self._camera_color))
            rects = np.column_stack((x_position - 5, y_position - 2.5, np.full_like(x_position, 10), np.full_like(y_position, 5)))
            for rect in rects:
                painter.draw_rect(*rect)
            # for x, y in zip(x_position, y_position):
            #     painter.draw_ellipse(QPointF(x, y), 3, 3)
            
            # dessiner le champ de vision
            painter.set_brush(self._coverage_color)
            fov_polygons = [
                self._transform_camera(x, y, theta, fov)
                for x, y, theta, fov in zip(x_position, y_position, theta, fov)
            ]
            for polygon in fov_polygons:
                painter.draw_polygon(polygon)
            # for x, y, theta, fov in zip(x_position, y_position, theta, fov):
            #     fov_polygon = self._transform_camera(x, y, theta, fov)
            #     painter.draw_polygon(fov_polygon)

        painter.restore()

    def _update_from_simulation(self, ga: GeneticAlgorithm | None):

        #image = QImage(QSize(self._canvas_width, self._canvas_height), QImage.Format_ARGB32)
        image = QImage(QSize(self._visualization_widget.width - 1, self._visualization_widget.height - 1), QImage.Format_ARGB32)
        image.fill(self._background_color)
        painter = QPainter(image)

        best_solution = None
        if ga:
            best_solution = ga.history.best_solution

        self._draw_canvas(painter, best_solution)
        painter.end()
        self._visualization_widget.image = image
