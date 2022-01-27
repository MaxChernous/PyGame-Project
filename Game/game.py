from abc import ABC, abstractmethod


# The Weapon class is an abstract base class that defines a generic way of creating ingame weapons
class Weapon(ABC):
    @abstractmethod
    def use(self, pos: "tuple[int, int]", speed: "tuple[int, int]"):
        """Use a weapon from position pos and moving with speed"""
        pass


# The Player class is a class that represents the player in the game.
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


# The Field class is a container for all the objects on the field.
class Field:
    def __init__(self):
        self.objects: "set[GameObject]" = set()

    def render(self, current_player: Player):
        """Renders all objects on the field"""
        deleted_objects: "list[GameObject]" = []

        for object in self.objects:
            object.interact(current_player)

            if not object.alive:
                deleted_objects.append(object)
                continue
            object.render()

        for x in deleted_objects:
            self.objects.remove(x)
