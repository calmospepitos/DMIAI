from random import random
from datetime import datetime

# -----------------------------------------------------------------------------
# f-string
# -----------------------------------------------------------------------------
# Une chaîne de caractères dans laquelle on retrouve des valeurs issues de 
# variables, de calculs, de résultats de fonctions, etc.
#
# Il suffit de préfixer la chaîne de caractères par un "f" ou "F" pour que les 
# expressions entre accolades soient évaluées et transformée en texte. Si on 
# désire afficher des accolades, il suffit de les doubler.
# 	
# Les f-strings sont apparu avec Python 3.6 et sont maintenant considéré comme
# la méthode la plus efficace pour formater des chaînes de caractères et celle 
# à utiliser de facto. Sachez qu'il existe d'autres méthodes pour formater des
# chaînes de caractères, elles peuvent être moins efficace, plus complexe et, 
# selon le contexte, considérées obsolètes.
#
# L'approche utilisée par Python est tellement efficace que d'autres langages
# ont implémenté des fonctionnalités similaires : JavaScript (ES6), C# (6.0),
# Java (12), PHP (7.0), C++ (20), etc.
#
# Pour plus d'information, voir :
# - https://realpython.com/python-f-strings/
# - https://docs.python.org/3/reference/lexical_analysis.html#f-strings
# - ...
#
# -----------------------------------------------------------------------------
a_string = 'Bonjour'
an_int = 666
a_float = 3.141592654
a_list = [1, 2, 3]
a_tuple = (11, 22, 33)
a_dictionary = { 'Name': 'Orange', 'RGB': (255, 128, 0) }
a_set = { 'apple', 'banana', 'cherry' }
a_datetime = datetime.now()

print(f'Une variable directement   : {a_string}') # entre accolade, la valeur est interprétée et transformée en str
print(f'Le nom et la valeur        : {an_int=}') # le = après la variable
print(f'Un calcul                  : {2.0 * a_float}') # les expressions sont possibles
print(f'Le résultat d\'une fonction : {random()}') # le résultat d'une fonction est une expression

print(f'Le formatage général :') # séparé par un : à droite
print(f' - la largeur et l\'alignement :')
print(f'   - : {an_int:<20}')
print(f'   - : {a_float:^20}')
print(f'   - : {a_string:>20}')
print(f' - le remplissage :')
print(f'   - : {an_int:20}')
print(f'   - : {a_float:.<20}')
print(f'   - : {a_string:.>20}')
print(f'Le formattage d\' un entier :')
print(f' - les bases :')
print(f'   - binaire      : {an_int:b}')
print(f'   - octale       : {an_int:o}')
print(f'   - décimale     : {an_int:d}')
print(f'   - hexadécimale : {an_int:x} ou {an_int:X}')
print(f' - les séparateurs de milliers :')
print(f'   - : {1000000:,}')
print(f'   - : {1000000:_}')
print(f'Le formattage d\' un flottant :')
print(f' - la précision :')
print(f'   - : {a_float:.2f}')
print(f'   - : {a_float:.5f}')
print(f'   - : {a_float:.9f}')
print(f' - les exposants :')
print(f'   - : {a_float:e}')
print(f'   - : {a_float:E}')
print(f'   - : {a_float:.2e}')
print(f'   - : {a_float:.2E}')
print(f' - les pourcentages (100 = 10000%, 1 = 100%, 0.01 = 1%) :')
print(f'   - : {a_float:.2%}')
print(f'   - : {1.0:.5%}')
print(f'   - : {0.25:.1%}')

# -----------------------------------------------------------------------------
print(f'La date et l\'heure :')
print(f' - Aujourd\'hui, c\'est le {a_datetime:%d/%m/%Y}')
print(f' - Il est {a_datetime:%H:%M %S sec}')
print(f' - Il est {a_datetime:%I:%M %S %p}')
print(f' - Il est {a_datetime:%d/%m/%Y %H:%M:%S:%f}')

# -----------------------------------------------------------------------------
print('Les collections (structures de données) :')
print(f' - les listes        : {a_list}')
print(f' - les tuples        : {a_tuple}')
print(f' - les dictionnaires : {a_dictionary}')
print(f' - les ensembles     : {a_set}')

# -----------------------------------------------------------------------------
print(f"Plusieurs valeurs dans une f-string avec des accolades '{{' et '}}', un entier {an_int}, une liste {a_list} et un tuple {a_tuple}.")

# -----------------------------------------------------------------------------
print(f'Les imbrications de {f"{'f-string':->10}":.>20} et {f"{'f-string':-<10}":.<20}.')

# -----------------------------------------------------------------------------
value_1 = 'CVM'
value_2 = None
print(f'Stratégie pour une valeur par défaut si une variable est None.')
print(f' - {value_1 or "valeur par défaut, au cas"}')
print(f' - {value_2 or "valeur par défaut, au cas"}')

# -----------------------------------------------------------------------------
# - il y a beaucoup plus à dire...
# - il est important de consulter la documentation officielle
# - nous reviendrons sur certains détails dans d'autres cours
# - ...