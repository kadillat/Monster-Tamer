from settings import *
import random

class Creature:
    def get_data(self,name):
        self.element = monster_data[name]["element"]
        self.health = self.maxhealth = monster_data[name]["health"]
        self.abilities = random.sample(list(ability_data.keys()),4)
        self.name = name


class Monster(pygame.sprite.Sprite,Creature):
    def __init__(self, name, surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(bottomleft = (180,640))
        self.get_data(name)

    

class Enemy(pygame.sprite.Sprite,Creature):
    def __init__(self, name, surf,):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(midbottom = (1000,300))
        self.get_data(name)