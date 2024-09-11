import sys
import copy
print('Version', sys.version)

# Bonnes pratiques:
#
# 1 - CALTAL: Code A Little, Test A Little
# 2 - DRY: Don't Repeat Yourself
# 3 - UMUD: You Must Use The Debugger
# ...

# Normes de programmation:
# 
# PEP 8: Norme de codage pour Python
# ->
# PascalCase: types (classes, ...). lower_snake_case: fonction, méthode, variable. UPPER_SNAKE_CASE: constante.
# Lignes de 80 caractères (exclue de la norme).
# Nom de variable et types pertinents même s'ils sont longs.
# Autodocumentation.
# Pas de commentaires creux (Pourquoi ce choix ou à quoi ça sert).

# Types de données fondamentaux:
#
a = 3 # integer (immutable)
b = 3.14 # float (immutable)
c = 1+2j # complex (immutable)
d = "allo" # string (immutable)
e = True # boolean (immutable)
f = None # NoneType (immutable)
g = b'allo' # bytes (immutable)
h = bytearray(b'allo') # bytes (mutable)
#
# Les types sont immutables, donc quand on "change" la valeur de la variable, on créé actuellement une nouvelle variable à une nouvelle addresse et le garbage collector va aller effacer la variable précédente.

# Opérateurs ternaires
#
value = 5
print(value > 0 and value < 10) # le if est déja assumé
print(0 < value < 10) # cela fonctionne aussi
print('positif' if value >= 0 else 'negatif')

# Structures de données fondamentales
#
#                               # mutable | subscriptable[read/write] | iterable | duplicable |
my_str = "string"               # false   | true/false                | true     | true       |
my_list = [0, 1, 2, 3, 4]       # true    | true/true                 | true     | true       |
my_tuple = (0, 1, 2, 3, 4)      # false   | true/false                | true     | true       |
my_set = { 0, 1, 2 }            # true    | false/false               | true     | false      |
my_dicti = { 0:'zero',          # true    | true/true                 | true     | false:true |
             1:'un',
             2:'deux' }

# Indexation et slicing
#
my_list = [10, 11, 12, 13, 14, 25, 26, 27, 28, 29]
print(my_list)
print(my_list[0]) # de gauche à droite de 0 à n-1, n étant l'index de la dernière valeur.
print(my_list[3])
print(my_list[9])
print(my_list[-1]) # de droite à gauche de 1 à n, n étant l'index de la dernière valeur.
print(my_list[-2])
print(my_list[0:3]) # ":" signifie un interval, donc de 0 à 3
print(my_list[1:-2]) # de 1 à l'avant dernier
print(my_list[:]) # tout
print(my_list[:3]) # tout de la droite jusqu'à 3
print(my_list[-3:]) # tout de la droite jusqu'à -3
print(my_list[0:5:2]) # de 0 jusqu'à 5 en sautant à chaque 2 index
print(my_list[8:3:-1])
print(my_list[::-1])

# Un interateur conceptuellement
#
# i = my_list.iterator()
# while i != my_list.last_iterator():
#     print(i) # do something
#     i += 1
#
for i in my_list:
    print(i, end=' ')
print('')
#
for i in range(10):
    print(i, end=' ')
print('')
#
for i in range(3):
    print('C52!', end=' ')
print('')
#
for key in my_dicti:
    print(key, end=' ')
print('')
#
for value in my_dicti.values():
    print(value, end=' ')
print('')
#
for key, value in my_dicti.items():
    print(key, ' => ', value)
#
# for i in range(len(my_dicti)):
#    print(my_dicti.keys[i], ' => ', my_dicti.values[i]) # Trop lent, à ne pas faire
#
list1 = ['a', 'l', 'l', 'o']
list2 = [5, 12, 45, 7]
list3 = [[1, 3], [2, 4], [5, 6]]
for a,b in list3:
    print('(', a, ':', b, ')')
#   
for i, value in enumerate(list1):
    print('position', i, ' => ', value, ' ', ord(value))
#
for v1, v2 in zip(list1, list2): # Fonction zip parcoure la list1 et list2 en même temps
    print(v1, ' <=> ', v2)
#
for v1, v2 in zip(list1, list2):
    v1 = 0
    
# Comprehension list
# Basic empty list construction
#
my_list = [] # 1
my_list = list() # 2
# Basic list construction
#
my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # 1
my_list = my_list(range(10)) # 2
my_list = [] # 3
for i in range(10):
    if i % 2:
        my_list.append(i)
my_list = [None] * 10 # 4
#
# Le comprehension list
# my_list = [ _expression_ for _member_in_iterable_ {if _condition_} ]
# est équivalent à...
# my_list = [] # 3
# for i in range(10):
#    if i % 2:
#        my_list.append(i)
#
my_list = [i**2 for i in range(10) if i % 2] # ** signifie un pouvoir, comme ^2
my_list = [0 for _ in range(10)]

# Référence/pointeur/"Garbage collector"
a = 3
print(a, hex(id(a)))
a = 4
print(a, hex(id(a)))
a[0] = 200
print(a, hex(id(a)))
a[:] = [20, 21, 22, 23]
print(a, hex(id(a)))

# Shallow copy: 
# Deep copy: 
b = a # Shallow copy
c = a[:] # Deep copy (ne fonctionne pas tout le temps)
d = copy.deepcopy(a) # Deep copy (méthode préférée)
print(b, hex(id(b)))
b[0] = 'Cool'
print(b, hex(id(b)))
print(a, hex(id(a)))

a = (0, 'allo',  (0,1), [5, 'Cool'])
print(a[0])
a[0] = 1 # Ne peut pas aller écrire parce qu'il est immuable
a[3][0] = 'Oh yeah'
a[3].append('C52')
print(a)

print(a, hex(id(a)))
print(b, hex(id(b)))
print(c, hex(id(c)))