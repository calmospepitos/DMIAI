import sys 
import klustr_utils
import numpy as np
from db_credential import PostgreSQLCredential 
from klustr_dao import PostgreSQLKlustRDAO 
from klustr_widget import KlustRDataSourceViewWidget 
from scatter_3d_viewer import QScatter3dViewer
from KNN import KNN
from Engine import Engine

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QGroupBox, QGridLayout, QScrollBar, QMainWindow, QMessageBox
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap, QColor

from __feature__ import snake_case, true_property 

class BaseWidget(QGroupBox):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        
        # Layout par défaut pour chaque widget
        self.main_layout = QVBoxLayout()
        self.set_layout(self.main_layout)
        
    # ajouter des widgets au layout principal
    def add_widget(self, widget):
        self.main_layout.add_widget(widget)


class DatasetWidget(BaseWidget):
    dataset_selected = Signal()  # Signal pour indiquer qu'un dataset a été sélectionné
    
    def __init__(self, klustr_dao, engine, single_test_widget, qscatter3d_widget, parent=None):
        super().__init__("Dataset", parent)
        self.klustr_dao = klustr_dao
        self.engine = engine    
        self.single_test_widget = single_test_widget
        self.__qscatter3d_widget = qscatter3d_widget

        #### QT ITEMS ##### 
        #dataset
        self.__dataset_combo_box = QComboBox()
        self.__dataset_combo_box.add_item("Sélectionnez le dataset")
        datasets = [dataset[1] for dataset in self.klustr_dao.available_datasets]
        self.__dataset_combo_box.add_items(datasets)
        
        #included in dataset groupbox
        dataset_info_groupbox = QGroupBox("Included in Dataset") 
        self.__category_count_label = QLabel("Category count: ")
        self.__training_image_count_label = QLabel("Training Image Count: ")
        self.__test_image_count_label = QLabel("Test Image Count: ")
        self.__total_image_count_label = QLabel("Total Image Count: ")
        
        #Transformation groupbox
        transformation_groupbox = QGroupBox("Transformation") 
        self.__translated_label = QLabel("Translated: ")
        self.__rotated_label = QLabel("Rotated: ")
        self.__scaled_label = QLabel("Scaled: ")

        ##### LAYOUTS #####
        included_in_dataset_layout = QGridLayout()
        included_in_dataset_layout.add_widget(self.__category_count_label)
        included_in_dataset_layout.add_widget(self.__training_image_count_label)
        included_in_dataset_layout.add_widget(self.__test_image_count_label)
        included_in_dataset_layout.add_widget(self.__total_image_count_label)
        dataset_info_groupbox.set_layout(included_in_dataset_layout) 

        #transformation layout
        transformation_layout = QGridLayout()
        transformation_layout.add_widget(self.__translated_label)
        transformation_layout.add_widget(self.__rotated_label)
        transformation_layout.add_widget(self.__scaled_label)
        transformation_groupbox.set_layout(transformation_layout)
        
        #dataset layout
        self.add_widget(self.__dataset_combo_box)

        dataset_info_layout = QHBoxLayout()
        dataset_info_layout.add_widget(dataset_info_groupbox)
        dataset_info_layout.add_widget(transformation_groupbox)
        
        self.main_layout.add_layout(dataset_info_layout)

        # signal -> slot connection  
        self.__dataset_combo_box.currentIndexChanged.connect(self.__update_dataset_info)

    @Slot()
    def __update_dataset_info(self):
        dataset = self.klustr_dao
                
        # Vérifier si un dataset valide est sélectionné
        dataset_index = self.__dataset_combo_box.current_index
        if dataset_index == 0:
            # Aucun dataset sélectionné = vider les champs
            self.clear_dataset_info()
            return
        
        dataset_name = self.get_selected_dataset_name()
        
        # Appel à load_training_data pour charger les données du dataset sélectionné
        self.engine.load_training_data(dataset_name)

        # Met à jour les informations du dataset ici
        dataset_info = self.klustr_dao.labels_from_dataset(dataset_name)
        dataset_training = dataset.image_from_dataset(dataset_name, True)
        dataset_test = dataset.image_from_dataset(dataset_name, False)
        dataset_total = len(dataset_training) + len(dataset_test)  
        
        result = dataset._execute_simple_query('''SELECT * FROM klustr.data_set_info WHERE name = %s;''',(dataset_name,))
        data = result[0]
        dataset_translated = data[2]
        dataset_rotated = data[3]
        dataset_scaled = data[4]

        self.__category_count_label.text = f"Category count: {len(dataset_info)}"
        self.__training_image_count_label.text = f"Training Image Count: {len(dataset_training)}"
        self.__test_image_count_label.text = f"Test Image Count: {len(dataset_test)}"
        self.__total_image_count_label.text = f"Total Image Count: {dataset_total}"
        self.__translated_label.text = f"Translated: {dataset_translated}"
        self.__rotated_label.text = f"Rotated: {dataset_rotated}"
        self.__scaled_label.text = f"Scaled: {dataset_scaled}"

        images = [dataset[3] for dataset in self.klustr_dao.image_from_dataset(dataset_name, False)]
        self.single_test_widget.imageComboBox.clear()
        self.single_test_widget.imageComboBox.add_items(images)
        
        # Émettre le signal
        self.dataset_selected.emit()
        
    # Retourne le nom du dataset actuellement sélectionné
    def get_selected_dataset_name(self):
        return self.__dataset_combo_box.current_text if self.__dataset_combo_box.current_index > 0 else None
    
    def clear_dataset_info(self):
        self.__category_count_label.text = "Category count: "
        self.__training_image_count_label.text = "Training Image Count: "
        self.__test_image_count_label.text = "Test Image Count: "
        self.__total_image_count_label.text = "Total Image Count: "
        self.__translated_label.text = "Translated: "
        self.__rotated_label.text = "Rotated: "
        self.__scaled_label.text = "Scaled: "
        self.single_test_widget.imageComboBox.clear()
        self.single_test_widget.imagePreview.clear()
        self.__qscatter3d_widget.clear()
           
    #getter dataset combo box 
    @property
    def dataset_combo_box(self):
        return self.__dataset_combo_box


class SingleTestWidget(BaseWidget):
    #classifyImage = Signal()  # signal button Classify

    def __init__(self, klustr_dao, engine, knn, knn_widget, qscatter3d_widget, parent=None):
        super().__init__("Single test", parent)
        self.klustr_dao = klustr_dao
        self.engine = engine
        self.knn = knn
        self.widget = knn_widget
        self.qscatter3d_widget = qscatter3d_widget
        self.__current_test_points_series_name = "Test Image"
        
        #### QT ITEMS #####
        #single test
        self.__image_combo_box = QComboBox()
        self.__image_preview = QLabel()
        self.__image_preview.alignment = Qt.AlignCenter
        self.__classify_button = QPushButton("Classify")
        self.__classified_label = QLabel("Image Name")
        self.__classified_label.alignment = Qt.AlignCenter

        ##### LAYOUTS #####
        #single test layout
        self.add_widget(self.__image_combo_box)
        self.add_widget(self.__image_preview)
        self.add_widget(self.__classify_button)
        self.add_widget(self.__classified_label)

        # signal -> slot connection  
        self.__image_combo_box.currentIndexChanged.connect(self.__update_image_preview)
        self.__classify_button.clicked.connect(self.__classify_image)
        
    #getter image combo box
    @property
    def imageComboBox(self):
        return self.__image_combo_box
    
    #getter image preview
    @property
    def imagePreview(self):
        return self.__image_preview
    
    @Slot()
    def __update_image_preview(self):
        image_name = self.__image_combo_box.current_text
        image_info = self.klustr_dao._execute_simple_query('''SELECT image FROM klustr.image_list_info WHERE image_name = %s;''',(image_name,))
        
        # Vérifie si image_info contient bien des données
        if image_info and len(image_info[0]) > 0:
            # Si les données existent, décodez et affichez l'image
            image_data = klustr_utils.qimage_argb32_from_png_decoding(image_info[0][0])
            pixmap = QPixmap.from_image(image_data)
            self.__image_preview.pixmap = pixmap
        else:
            # Si aucune donnée n'est trouvée, afficher un message par défaut
            self.__image_preview.text = "Image non disponible"
       
    @Slot()
    def __classify_image(self):
        image_name = self.__image_combo_box.current_text
        image_info = self.klustr_dao._execute_simple_query('''SELECT image FROM klustr.image_list_info WHERE image_name = %s;''',(image_name,))
        
        qimage = klustr_utils.qimage_argb32_from_png_decoding(image_info[0][0])
        np_image = klustr_utils.ndarray_from_qimage_argb32(qimage)
        
        np_image = 1-np_image
        
        metrics = self.engine.metrics(np_image)
        
        # Normalise la troisième métrique avec max_z_value calculé sur les données d'entraînement
        if hasattr(self, 'max_z_value') and self.max_z_value != 0:
            metrics = (metrics[0], metrics[1], metrics[2] / self.max_z_value)
        
        img_predicted = self.knn.classify(metrics)
        
        self.__classified_label.text = f"Classified Image Name: {img_predicted}"
        
        self.qscatter3d_widget.remove_serie(self.__current_test_points_series_name)
        
        test_points_array = np.array([metrics])
        self.qscatter3d_widget.add_serie(test_points_array, QColor("red"), title=self.__current_test_points_series_name)
    

class KnnWidget(BaseWidget):
    kChange = Signal(int) # signal k value change
    maxDistanceChange = Signal(float) #signal max distance change

    def __init__(self, parent=None):
        super().__init__("Knn parameters", parent)

        #### QT ITEMS ##### 
        #knn
        self.__k_slider = QScrollBar(Qt.Horizontal)
        self.__k_slider.set_range(1, 10)
        self.__k_slider.value = 3
        self.__k_label = QLabel("k-value: 3")     
        self.__max_dist_slider = QScrollBar(Qt.Horizontal)
        self.__max_dist_slider.set_range(1, 10)
        self.__max_dist_slider.value = 3
        self.__max_dist_label = QLabel("Max Distance: 0.3")   

        ##### LAYOUTS #####
        #knn layout
        self.add_widget(self.__k_label)
        self.add_widget(self.__k_slider)
        self.add_widget(self.__max_dist_label)
        self.add_widget(self.__max_dist_slider)

        # signal -> slot connection 
        self.__k_slider.valueChanged.connect(self.__change_k_value)
        self.__max_dist_slider.valueChanged.connect(self.__change_max_distance)

    @Slot()
    def __change_k_value(self):
        self.__k_label.text = f"k-value: {self.__k_slider.value}"
        self.kChange.emit(self.__k_slider.value)

    @Slot()
    def __change_max_distance(self):
        self.__max_dist_label.text = f"Max Distance: {self.__max_dist_slider.value / 10}"
        self.maxDistanceChange.emit(self.__max_dist_slider.value)
    
    #getter slider k value
    @property
    def slider_k_value(self):
        return self.__k_slider
    
    #getter slider max_dist value 
    @property
    def slider_max_dist_value(self):
        return self.__max_dist_slider

class KlustRDataSourceViewWidget(QMainWindow):
    def __init__(self, klustr_dao):
        super().__init__(None)
        self.klustr_dao = klustr_dao
        
        self.set_window_title("Knn Image Classification")

        # création widgets
        self.__knn_widget = KnnWidget()
        self.__qscatter3d_widget = QScatter3dViewer()
        self.knn = KNN(self.__knn_widget.slider_k_value.value, self.__knn_widget.slider_max_dist_value.value)    
        self.engine = Engine(klustr_dao, self.knn)
        
        self.__singletest_widget = SingleTestWidget(klustr_dao, self.engine, self.knn, self.__knn_widget, self.__qscatter3d_widget)
        self.__dataset_widget = DatasetWidget(klustr_dao, self.engine, self.__singletest_widget, self.__qscatter3d_widget)  
        
        # Connection du signal lorsqu'un dataset est sélectionné
        self.__dataset_widget.dataset_selected.connect(self.__update_scatter_viewer)

        # Récupération du nom du dataset sélectionné et chargement des données d'entraînement
        dataset_name = self.__dataset_widget.get_selected_dataset_name()
        self.engine.load_training_data(dataset_name)
        
        # main layout
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.add_widget(self.__dataset_widget)
        left_layout.add_widget(self.__singletest_widget)
        left_layout.add_widget(self.__knn_widget)
        
        # Ajout du QScatter3dViewer
        main_layout.add_layout(left_layout)
        main_layout.add_widget(self.__qscatter3d_widget)
        
        # About button
        about_button = QPushButton("About")
        about_button.clicked.connect(self.__show_about_message)
        left_layout.add_widget(about_button)
        
        #central widget
        central_widget = QWidget()
        central_widget.set_layout(main_layout)
        self.set_central_widget(central_widget)
    
    def __update_scatter_viewer(self):
        self.__qscatter3d_widget.clear()
        
        # Obtiens le dataset_name actuellement sélectionné
        dataset_name = self.__dataset_widget.get_selected_dataset_name()
        
        # Appel de img_vector3d avec dataset_name
        vector3d_data = self.engine.img_vector3d(dataset_name)
        
        if vector3d_data:  # Affiche uniquement si des données existent
            # Crée vector3d_array sans la normalisation
            vector3d_array = np.array([[v.x(), v.y(), v.z()] for v in vector3d_data])

            # Calcule le maximum pour la normalisation de la troisième colonne
            max_z_value = np.max(vector3d_array[:, 2])
            
            # Normalise la troisième colonne si max_z_value n'est pas zéro pour éviter la division par zéro
            # Ramène toutes les valeurs de z dans un intervalle allant de 0 à 1.
            if max_z_value != 0:
                vector3d_array[:, 2] /= max_z_value
            
            # Ajout des points au scatter viewer
            self.__qscatter3d_widget.add_serie(vector3d_array, QColor("green"), title='Training Data')
        else:
            print(f"Aucun point trouvé pour le dataset '{dataset_name}'")

    def __initialize_scatter_viewer(self):
        viewer = self.__qscatter3d_widget
        viewer.clear()
        
        # Set title and labels
        viewer.title = "Métriques des images"

        # Configure axes
        viewer.axis_x.title = "Ratio aire/périmètre"
        #viewer.axis_x.range = (0, 1)
        viewer.axis_y.title = "Cercle circonscrit"
        #viewer.axis_y.range = (0, 1)
        viewer.axis_z.title = "Cercle inscrit"
        #viewer.axis_z.range = (0, 1)

        # Show the viewer
        viewer.show()
        
    @Slot()
    def __show_about_message(self):
        about_message = """
        Ce logiciel est le projet no 1 du cours C52. Il a été réalisé par : 
        - Alexandre Couret
        - Alexia Levesque
        - Vinícius Tolotti Borba
        Il consiste à implémenter et visualiser un système de classification d'images basé sur l'algorithme K-Nearest Neighbors (KNN) avec les concepts suivants : 
        - Traitement d'images
        - Calcul et extraction de descripteurs de forme
        - Visualisation 3D des données avec des métriques calculées
        - Classification supervisée avec l'algorithme KNN
        Nos 3 descripteurs de forme sont : 
        - Ratio aire/périmètre - en %, pour le domaine de la reconnaissance de forme - correspondant au rapport entre l'aire et le périmètre de l'objet.
        - Cercle circonscrit - en %, pour le domaine de la reconnaissance de forme - correspondant au ratio entre l'aire de l'objet et celle de son cercle circonscrit.
        - Cercle inscrit - en %, pour le domaine de la reconnaissance de forme - correspondant au ratio entre l'aire du cercle inscrit et celle du cercle circonscrit de l'objet.
        Plus précisément, ce laboratoire permet de mettre en pratique les notions de :
        - Utilisation de la bibliothèque NumPy pour le traitement efficace des données
        - Utilisation de la bibliothèque PyQt pour l'interphace graphique
        - Calcul des distances et sélection des voisins les plus proches dans l'algorithme KNN
        - Visualisation des points 3D pour représenter les données dans un espace tridimensionnel, basé sur les descripteurs de forme
        Un effort d'abstraction a été fait pour ces points :
        - Modularité du code, avec des classes séparées pour l'Engine de calcul, l'algorithme KNN et l'interface utilisateur
        - Utilisation de fonctions d'utilité pour le calcul de descripteurs de forme
        Finalement, l’ensemble de données le plus complexe que nous avons été capable de résoudre est :
        - Un ensemble de données contenant des images de différentes formes, permettant de tester la robustesse de l'algorithme KNN avec des descripteurs de forme variés.
        """
        QMessageBox.about(self, "About", about_message)
   

def main():
    # Application principale de Qt 
    app = QApplication(sys.argv)
    
    # Information de connexion à la base de données
    credential = PostgreSQLCredential(host='localhost', port=5432, database='postgres', user='postgres', password='AAAaaa123')
    
    # DAO utilisé
    klustr_dao = PostgreSQLKlustRDAO(credential)
    
    # Instanciation et affichage du widget de visualisation des données du projet KlustR 
    source_data_widget = KlustRDataSourceViewWidget(klustr_dao)
    
    # Initialisation et mise à jour du QScatter3dViewer
    source_data_widget.__initialize_scatter_viewer()
    source_data_widget.__update_scatter_viewer()
    source_data_widget.show()
    
    # Démarrage de l’engin Qt 
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
