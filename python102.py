# Classe
class GameCharacter:
    # def __new__(cls) -> Self: # Constructeur
    #    pass

    def __init__(self, name, health, power): # Initialisateur
        self.name = name # public
        self._health = health # protected, ça veut dire qu'on peut y accéder mais on ne devrait pas y toucher
        self.__power = power # private, name mangling

    def attack(self):
        print("Attaque !")

    # @ est un décorateur
    @property # Getter
    def health(self):
        return self._health
    
    @health.setter # Setter
    def health(self, value):
        self._health = max(0, value) # On ne peut pas avoir de points de vie négatifs

roger = GameCharacter("Roger", 100, 15) # Instance
william = GameCharacter("William", 150, 10) # Instance

print(f"{roger.name} a {roger.health()} points de vie.") # On ne peut pas accéder directement à la variable _health, donc on doit passer par le getter

roger.attack() 
GameCharacter.attack(roger) # C'est la même chose que la ligne précédente, mais meilleure pratique

variable = 100
roger._health = variable
roger._GameCharacter__power = 0 # Pour accéder à une variable privée, on doit passer par le name mangling
GameCharacter.attack(roger)