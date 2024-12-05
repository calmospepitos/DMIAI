
import sys


from gaapp import QGAApp

from ga_strategy_genes_mutation import GenesMutationStrategy
from ga_problem_unknown_number import QUnknownNumberProblemPanel
from ga_problem_open_box import QOpenBoxProblemPanel
from ga_optimisation_geometrique import QGeometryProblem


from PySide6.QtWidgets import QApplication

from __feature__ import snake_case, true_property



def main():
    # Création de l'application Qt
    # -----------------------------------------------
    app = QApplication(sys.argv)
    
    # Création de l'application de résolution de problèmes génétiques
    # -----------------------------------------------
    ga_app = QGAApp()
    
    # Exemples d'ajout de stratégies : sélection, croisement et mutation
    # -----------------------------------------------
    # ga_app.add_selection_strategy(...)
    # ga_app.add_crossover_strategy(...)
    ga_app.add_mutation_strategy(GenesMutationStrategy)                             # note : on passe une classe, pas une instance


    # Exemple d'ajout de panneau de résolution de problème
    # -----------------------------------------------
    # Problème de la boîte ouverte
    ga_app.add_solution_panel(QUnknownNumberProblemPanel(-1000.0, 0.0, 1000.0))     # note : on passe une instance, pas une classe
    ga_app.add_solution_panel(QOpenBoxProblemPanel())                               # note : on passe une instance, pas une classe
    ga_app.add_solution_panel(QGeometryProblem())
    # ...
    # ga_app.add_solution_panel(...)

    # Affichage et exécution de l'application
    # -----------------------------------------------
    ga_app.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()

