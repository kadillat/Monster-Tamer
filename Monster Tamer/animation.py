
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
os.chdir(script_dir)

from settings import *

class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self,target,frames,groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = target.rect.center)

    def update(self,dt):
        self.frame_index = self.frame_index + 5*dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()