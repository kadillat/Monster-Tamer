from settings import * 
import random

class Creature:
    def get_data(self,name):
        self.element = monster_data[name]["element"]
        self._health = self.maxhealth = monster_data[name]["health"]
        self.name = name

        if "abilities" in monster_data[name]:
            self.abilities = monster_data[name]["abilities"]
        else:
            self.abilities = random.sample(list(ability_data.keys()), 4)

    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self,value):
        self._health = min(self.maxhealth,max(0,value))


class Monster(pygame.sprite.Sprite,Creature):
    def __init__(self, name, surf,groups):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(bottomleft = (180,640))
        self.get_data(name)

    

class Enemy(pygame.sprite.Sprite,Creature):
    def __init__(self, name, surf,groups):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_frect(midbottom = (1000,300))
        self.get_data(name)