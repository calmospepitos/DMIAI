import numpy as np
from numpy.typing import NDArray

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QSizePolicy, QGridLayout, QComboBox
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPolygonF
from gacvm import Domains, ProblemDefinition, Parameters, GeneticAlgorithm
from uqtwidgets import QImageViewer, create_scroll_real_value
from gaapp import QSolutionToSolvePanel

from __feature__ import snake_case, true_property

class QGeometryProblem(QSolutionToSolvePanel):
    # a voir si on a besoin d'un point pour refermer la forme
    # Shape possibles (rectangle, Lettre L, étoile)
    _rectangle_points = [
        QPointF(0, 0), # coin haut gauche
        QPointF(2, 0),
        QPointF(2, 1),
        QPointF(0, 1)
    ]
    _rectangle_shape = QPolygonF(_rectangle_points)
    
    _L_points = [
        QPointF(0, 0), 
        QPointF(0.5, 0),
        QPointF(0.5, 1.5), 
        QPointF(1, 1.5),
        QPointF(1, 2),
        QPointF(0, 2)
    ]
    _L_shape = QPolygonF(_L_points)
    
    _star_points = [
        QPointF(5, 0),
        QPointF(1.62, 1.18),
        QPointF(1.55, 4.76),
        QPointF(-0.62, 1.9),
        QPointF(-4.05, 2.94),
        QPointF(-2, 0),
        QPointF(-4.05, -2.94),
        QPointF(-0.62, -1.9),
        QPointF(1.55, -4.76),
        QPointF(1.62, -1.18),    
    ]
    _star_shape = QPolygonF(_star_points)
    
    
    
    
    
    
    
    def __init__(self, width : int = 500, height : int = 250, obstacle_count : int = 1, parent : QWidget | None = None): # à voir pour shape
        super().__init__(parent)
        self._width = width
        self._height = height
        self._obstacle_count = obstacle_count # getter du scrollbar pour avoir la valeur
        
        self._min_obstacles = 1
        self._max_obstacles = 100
        

        # création du scrollbar pour le nombre d'obstacles
        self._value_scroll_bar, value_layout = create_scroll_real_value(self._min_obstacles, self._obstacle_count, self._max_obstacles, 0, title = "Nombre d'obstacles")
        self._value_scroll_bar.valueChanged.connect(lambda : self._update_from_simulation(None))

        
        # Mise en place de la disposition des widgets
        param_group_box = QGroupBox('Parameters')
        param_layout = QFormLayout(param_group_box)
        shape_box = QComboBox()
        param_layout.add_row(value_layout)
        param_layout.add_row('Shape', shape_box)
        param_group_box.size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        
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
        
        # self._value_scroll_bar.valueChanged.connect(self._update_from_configuration)
        
        
    @property
    def name(self) -> str:
        return "Shape Optimizer"

    @property
    def summary(self) -> str:
        return "Déterminer la transformation affine permettant de disposer une forme la plus grande possible sur un canvas sans collision."

    @property
    def description(self) -> str:
        return '''On cherche à obtenir la forme avec la plus grande surface sur le canvas sans collisions avec les obstacles.

Données initiales du problème : 
    - zone de recherche : position x[0, width], position y[0, height], angle theta[0, 360], scale[0, 250]
    - unknown : La plus grande surface
Dimension du problème : 
    - d = 4
    - d1 = x[0, width]
    - d2 = y[0, height]
    - d3 = [0, 360]
    - d4 = [0, 250]
Structure du chromosome :
    - 1 gène représentant la position x,y, l'angle de rotation et l'homothétie de la forme
Fonction objective :
    - Si la surface de la forme est en dehors du canvas, la fitness est de 0 
    - On cherche la surface de la forme 
    - Le plus élevée est la surface, le mieux est la fitness (pas besoin de maximiser)
'''
    @property
    def problem_definition(self) -> ProblemDefinition:
        def objective_function(chromosome : NDArray) -> float:
            # verifier si les coins du bounding box sont en dehors (si oui return 0)
            # vérifier si collision avec les points (bord et à l'intérieur)
            if(chromosome[0] > self._width or chromosome[1] > self._height):
                return 0.0
            elif (chromosome[0] < self._width or chromosome[1] < self._height):
                return 0.0
            else:
                pass
                
            # matrices de transformation (translation, rotation, scale)
            # calculer la surface 
            # vérifier si c'est hors de la plage de recherche (si oui retourner 0)
            # retourner surface
            
        domains = Domains(np.array([[0, self._width], [0, self._height], [0, 360], [0, 250]]), ('Largeur', 'Hauteur', 'Angle de rotation', 'Homothétie',))
        return ProblemDefinition(domains, objective_function)
    
    @property
    def default_parameters(self) -> Parameters:
        engine_parameters = Parameters()
        engine_parameters.maximum_epoch = 50
        engine_parameters.population_size = 10
        engine_parameters.elitism_rate = 0.1
        engine_parameters.selection_rate = 0.9
        engine_parameters.mutation_rate = 0.1
        return engine_parameters

    def _update_from_simulation(self, ga : GeneticAlgorithm | None) -> None:
        '''
        Fonction utilitaire permettant de donner du 'feedback' pour chaque pas de simulation. Il faut gérer le cas où ga est None. Lorsque ga est None, on donne un feedback d'initialisation sans aucune évolution.
        '''
        raise NotImplementedError()

    # @Slot()
    # def update_solution(self, ga : GeneticAlgorithm) -> None:
    #     """Slot provoquant la mise à jour de l'interface utilisateur du panneau.
        
    #     Attention, cette fonction n'est pas destinée à être 'override'."""
    #     self._update_from_simulation(ga)