import numpy as np

class KNN:
    def __init__(self, k, max_dist):
        self.k = max(1, min(k, 10))
        self.max_dist = max(1, min(max_dist, 10))
        self._metrics = []   
        self._labels = []
    
    def add_training_data(self, metrics, label):
        # convertir les métriques en tableau NumPy
        metrics = np.array(metrics).reshape(1, -1)
        label = np.array([label])
        
        # Si _metrics est None, on initialise _metrics avec metrics, sinon on empile metrics sur _metrics (vstack = ajouter des lignes)
        if self._metrics is None:
            self._metrics = metrics
        else:
            self._metrics = np.vstack([self._metrics, metrics])
        
        # ajouter label à _labels (concatenate = liste ordonnée)
        self._labels = np.concatenate([self._labels, label])
    
    def clear_training_data(self):
        # Réinitialiser _metrics et _labels à des tableaux vides
        self._metrics = None
        self._labels = np.empty(0, dtype=object)
        

    def classify(self, metrics):
       # Assure que metrics est un tableau NumPy
        metrics = np.array(metrics)

        # Calcule le nombre de dimensions
        num_dimensions = metrics.shape[0]
        
        # calcule la distance normalisée entre le vecteur à classifier et chaque vecteur d’entraînement 
        # utilise le broadcasting pour soustraire le vecteur metrics de chaque vecteur dans __metrics_array
        # axis=1 faire la somme des éléments sur chaque ligne individuellement
        distances = np.sqrt(np.sum((self._metrics - metrics) ** 2, axis=1)) / np.sqrt(num_dimensions)
        
        # Filtre par la distance maximale si elle est définie
        if self.max_dist is not None:
            valid_indices = distances <= self.max_dist
            distances = distances[valid_indices]
            valid_labels = self._labels[valid_indices]
            
            # Si aucun point ne satisfait max_dist, retourner None
            if len(distances) == 0:
                return None
    
        #argsort triés de la plus petite à la plus grande distance
        k_nearest_indices = np.argsort(distances)[:self.k]
        k_nearest_labels = valid_labels[k_nearest_indices]
        
        # renvoie deux tableaux: 
        # labels - contient les étiquettes uniques trouvées
        # counts - contient le nombre d’occurrences de chaque étiquette dans le même ordre.
        labels, counts = np.unique(k_nearest_labels, return_counts=True)

        # Si counts est vide, retourner None
        if len(counts) == 0:
            return None
        
        # Trouve la classe avec le max de votes
        max_count = np.max(counts)
        max_labels = labels[counts == max_count]  # Toutes les étiquettes ayant le nombre maximum
        
        # En cas d'égalité, retourne None
        if len(max_labels) > 1:
            return None
        else:
            return max_labels[0]