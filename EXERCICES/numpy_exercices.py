import numpy as np

# Statistiques
# Données
salaire_horaire = [ 9.50, 33.50, 30.25, 10.75, 41.50, 16.75, 18.00, 15.50, 21.00,
                   15.25, 21.50, 38.00, 25.25, 42.00, 25.00, 18.75, 37.25, 38.50,
                   40.00, 41.00]
heures_par_semaine = 37.5           # nombre d'heures travaillées par semaine
semaine_par_annee = 52              # nombre de semaines payées par année

# Convertir la liste en tableau numpy
salaire_horaire = np.array(salaire_horaire)

# Fonction pour afficher le titre et le résultat
def print_title_and_result(title, result):
    print_title_and_result.nbr = getattr(print_title_and_result, 'nbr', 0) + 1
    print(f'{print_title_and_result.nbr:02}) {title} :\n{" " * 4}{result}')

# Questions:
# 01) Calculer la masse salariale hebdomadaire
total_sum = np.sum(salaire_horaire) * heures_par_semaine
print_title_and_result('Masse salariale hebdomadaire:', total_sum)

# 02) Calculer le salaire annuel moyen
average = np.mean(salaire_horaire) * heures_par_semaine * semaine_par_annee
print_title_and_result('Salaire annuel moyen:', average)

# 03) Calculer le salaire annuel médian
median = np.median(salaire_horaire) * heures_par_semaine * semaine_par_annee
print_title_and_result('Salaire annuel médian:', median)

# 04) Créer une liste de tous les salaires horaires inférieurs à 15.50 $/h
salaires_inf_15_50 = salaire_horaire[salaire_horaire < 15.50]
formatted_wage_below = [f'{value:.02f} $' for value in salaires_inf_15_50]
assembled_wage_below = '  -  '.join(formatted_wage_below)
print_title_and_result('Salaires inférieurs à 15.5 $/h', f'{assembled_wage_below}')

# 05) Compter tous les salaires horaires égaux ou supérieurs à 30.00 $/h
salaires_sup_30 = np.count_nonzero(salaire_horaire >= 30.00)
print_title_and_result('Salaires égaux ou supérieurs à 30.00 $/h:', salaires_sup_30)

# 06) Calculer le coût annuel d'une augmentation de la masse salariale de 2.5% pour tous les employés faisant moins de 25.00 $/h
augmentation = 1.025
augmented_salaries = salaire_horaire[salaire_horaire < 25.00] * augmentation # Nouvelle liste de salaires augmentés
total_sum_augmented = np.sum(augmented_salaries) * heures_par_semaine * semaine_par_annee

# Géométrie
# Question 1: Créer une image carrée de taille donnée
def create_image(size):
    return np.zeros((size, size), dtype=np.uint8) # np.zeros crée une matrice avec des éléments de valeur 0, uint8 pour des valeurs entières non signées sur 8 bits (plage de 0 à 255)

# Question 2: Remplir une image avec une couleur donnée
def fill(image, color=1): # Par défaut, la couleur est 1
    image[:] = color # Remplir l'image avec la couleur donnée, [:] pour remplir tous les éléments de l'image

# Question 3: Réinitialiser une image avec la couleur 0
def clear(image):
    fill(image, 0) # Remplir l'image avec la couleur 0

# Question 4: Remplire tous les pixels d'une image avec une couleur aléatoire
def randomize(image, percent=0.5):
    rng = np.random.default_rng() # Générateur de nombres aléatoires
    image[:] = (rng.random(image.shape) <= percent).astype(image.dtype) # Remplir l'image avec des valeurs aléatoires inférieures à un certain pourcentage

# Question 5: Dessiner un point dans une image
def draw_point(image, point, color=1):
    if point[0] >= 0 and point[0] < image.shape[0] and point[1] >= 0 and point[1] < image.shape[1]: # Vérifier si le point est dans l'image
        image[point[0], point[1]] = color # Dessiner un point dans l'image à la position donnée avec la couleur donnée

# Question 6: Dessiner un rectangle dans une image
def draw_rectangles(image, top_left, bottom_right):
    if top_left[0] < bottom_right[0] and top_left[1] < bottom_right[1]:
        image[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]] = 1

# Question 7: Reset la bordure d'une image
def reset_border(image):
    image[0, :] = 0 # Réinitialiser la première ligne
    image[-1, :] = 0 # Réinitialiser la dernière ligne
    image[:, 0] = 0 # Réinitialiser la première colonne
    image[:, -1] = 0 # Réinitialiser la dernière colonne

# Question 8: Dessiner un point d'une couleur spécifique à un point aléatoire
def draw_random_point(image, color=1):
    rng = np.random.default_rng() # Générateur de nombres aléatoires
    x = rng.integers(0, image.shape[1]) # Coordonnée x aléatoire (colonne)
    y = rng.integers(0, image.shape[0]) # Coordonnée y aléatoire (ligne)
    draw_point(image, (x,y), color)

# Question 9: Inverse un point de l'image à une position aléatoire
def inverse_random_point(image, color=0):
    pass