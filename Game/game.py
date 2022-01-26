from abc import ABC, abstractmethod


class Weapon(ABC):
    @abstractmethod
    def use(self, pos: "tuple[int, int]", speed: "tuple[int, int]"):
        """Use a weapon from position pos and moving with speed"""
        pass

class Player:
    def __init__(self):
        self.pos = (0, 0)
        self.speed = (0, 0)
        self.weapons = []


class GameObject(ABC):
    def __init__(self):
        super().__init__()
        self.alive = True

    @abstractmethod
    def render(self):
        """Renders object"""
        pass

    @abstractmethod
    def interact(self, player: Player):
        """Interacts with given player"""
        pass

class Field:
    def __init__(self):
        self.objects: "set[GameObject]" = set()

    def render(self, current_player: Player):
        """Renders all objects on the field"""
        for object in self.objects:
            object.interact(current_player)
            if not object.alive: # Not sure if it works
                self.objects.remove(object)
                continue
            object.render()
            


    