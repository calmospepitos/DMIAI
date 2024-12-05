import numpy as np
import klustr_utils
from PySide6.QtGui import QVector3D

class Engine:
    def __init__(self, klustr_dao, knn):
        self.klustr_dao = klustr_dao 
        self.knn = knn
    
######## fonctions supplémentaires ###############
    # Aire
    def _area(self, image):
        # Somme des pixels
        return np.sum(image)

    # Aire d'un cercle
    def _area_circle(self, radius):
        return np.pi * (radius ** 2)

    # Grille
    def _grid(self, image):
        height, width = image.shape
        col, row = np.meshgrid(np.arange(width), np.arange(height))
        return (col, row)
    
    # Centroïde   
    def _centroid(self, image):
        total_area = self._area(image)
        col, row = self._grid(image)
        x = float(np.sum(col * image) / total_area) 
        y = float(np.sum(row * image) / total_area) 
        return (x, y)

    # Distance maximum
    def _max_distance(self, image):
        col, row = self._grid(image)
        centroid_point = self._centroid(image)
        # Calcul tous les points par rapport au centroïde
        distances = np.sqrt((row - centroid_point[1]) ** 2 + (col - centroid_point[0]) ** 2) # Pythagore, ça retourne tous les distances de centroïdes et les points de l'image
        max_distance = np.max(distances[image != 0])    
        return max_distance

    # Distance minimum
    def _min_distance(self, image):
        col, row = self._grid(image)
        centroid_point = self._centroid(image)
        # Calcul tous les points par rapport au centroïde   
        distances = np.sqrt((row - centroid_point[1]) ** 2 + (col - centroid_point[0]) ** 2) # Pythagore, ça retourne tous les distances de centroïdes et les points de l'image
        min_distance = np.min(distances[image != 0]) 
        return min_distance

    def _perimeter(self, image):
        form_mask = image != 0
        # Masques pour chaque voisin (haut, bas, gauche, droite)
        top = form_mask[:-1, :]  # tous sauf la dernière ligne
        bottom = form_mask[1:, :]  # tous sauf la première ligne
        left = form_mask[:, :-1]  # toutes sauf la dernière colonne
        right = form_mask[:, 1:]  # toutes sauf la première colonne
        
        # (~top signifie "le voisin n'appartient pas à la forme").
        top_edge = form_mask[1:, :] & ~top  # Si haut est un bord
        bottom_edge = form_mask[:-1, :] & ~bottom  # Si bas est un bord
        left_edge = form_mask[:, 1:] & ~left  # Si gauche est un bord
        right_edge = form_mask[:, :-1] & ~right  # Si droite est un bord
        
        # Détection des coins : bord supérieur-gauche, bord supérieur-droit, etc.
        top_left_corner = form_mask[1:, 1:] & ~top[:, 1:] & ~left[1:, :]
        top_right_corner = form_mask[1:, :-1] & ~top[:, :-1] & ~right[1:, :]
        bottom_left_corner = form_mask[:-1, 1:] & ~bottom[:, 1:] & ~left[:-1, :]
        bottom_right_corner = form_mask[:-1, :-1] & ~bottom[:, :-1] & ~right[:-1, :]

        return (np.sum(top_edge) + np.sum(bottom_edge) + np.sum(left_edge) + np.sum(right_edge) -
                        (np.sum(top_left_corner) + np.sum(top_right_corner) + np.sum(bottom_left_corner) + np.sum(bottom_right_corner)))

    ####################################
    ######## MÉTRIQUE #1 ###############
    ####################################
    # E ]0, 1/4*pi]
    def _ratio_area_perimeter(self, image):
        return (4 * np.pi * (self._area(image))) / (self._perimeter(image) ** 2)

    ####################################
    ######## MÉTRIQUE #2 ###############
    ####################################
    def _circum_circle(self, image):
        max_dist = self._max_distance(image)
        circum_circle_area = self._area_circle(max_dist)
        area_val = self._area(image)
        return area_val / circum_circle_area

    ####################################
    ######## MÉTRIQUE #3 ###############
    ####################################
    def _inscr_circle(self, image):
        # Calcule la distance minimale pour le cercle inscrit
        min_dist = self._min_distance(image)
        inscr_circle_area = self._area_circle(min_dist)
        
        # Calcule l'aire du cercle circonscrit pour la normalisation
        circum_circle_area = self._circum_circle(image) * self._area(image)  # Utilise l'aire pour ajuster

        # Vérifie que l'aire du cercle circonscrit n'est pas zéro pour éviter les divisions par zéro
        if circum_circle_area == 0:
            return 0

        # Calcule le ratio entre l'aire du cercle inscrit et celle du cercle circonscrit
        ratio = inscr_circle_area / circum_circle_area

        # Normalise le ratio pour le garder entre 0 et 1
        normalized_ratio = max(0, min(ratio, 1))
        
        return normalized_ratio

######## fonction pour retourner les metriques ###############
    def metrics(self, image):
        metric1 = self._ratio_area_perimeter(image)
        metric2 = self._circum_circle(image)
        metric3 = self._inscr_circle(image)
        return (metric1, metric2, metric3)

    #### FONCTIONS POUR LE SCATTER 3D ####
    # Récupère toutes les images d'entraînement pour un dataset donné en utilisant la fonction image_from_dataset du DAO.
    def get_training_images_for_dataset(self, dataset_name):
        # Récupère les images d'entraînement pour le dataset spécifié
        training_images = self.klustr_dao.image_from_dataset(dataset_name, training_image=True)
        # Vérification du nombre d'images d'entraînement récupérées
        print(f"Nombre d'images d'entraînement pour le dataset '{dataset_name}': {len(training_images)}")
        return training_images
    
    def img_vector3d(self, dataset_name):
        vectors3d = []
        training_images = self.get_training_images_for_dataset(dataset_name)
        
        print(f"Nombre d'images pour le scatter 3D : {len(training_images)}")  # Vérification du nombre d'images

        for img in training_images:
            qimage_argb32 = klustr_utils.qimage_argb32_from_png_decoding(img[6])
            np_image = klustr_utils.ndarray_from_qimage_argb32(qimage_argb32)
            
            np_image = 1-np_image
            
            metric1 = self._ratio_area_perimeter(np_image)
            metric2 = self._circum_circle(np_image)
            metric3 = self._inscr_circle(np_image)

            vector_tmp = QVector3D(metric1, metric2, metric3)

            vectors3d.append(vector_tmp)
        return vectors3d
    
    ########## FONCTION LOAD TRAINING IMAGES AND LABELS ########## 
    def get_all_images(self, dataset_name):
        all_images = []
        training_images = self.get_training_images_for_dataset(dataset_name)
        
        for img in training_images:
            qimage_argb32 = klustr_utils.qimage_argb32_from_png_decoding(img[6])
            np_image = klustr_utils.ndarray_from_qimage_argb32(qimage_argb32)
            
            np_image = 1-np_image
            
            all_images.append(np_image)
        return all_images
      
    def get_all_labels(self, dataset_name):
        all_labels = []
        # Récupère uniquement les images d'entraînement pour le dataset sélectionné
        training_images = self.get_training_images_for_dataset(dataset_name)
        all_labels = [label[1] for label in training_images]
        return all_labels
    
    def load_training_data(self,dataset_name):
        # Effacer les données précédentes avant de charger les nouvelles
        self.knn.clear_training_data()
        
        training_images = self.get_all_images(dataset_name)
        labels = self.get_all_labels(dataset_name)
        
        for image, label in zip(training_images, labels):          
            metrics = self.metrics(image) 
            self.knn.add_training_data(metrics, label)


if __name__ == "__main__":
    pass