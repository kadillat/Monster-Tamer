from settings import *

class Timer:
    def __init__(self,duration,repeat = False ,autostart = False ,func = None):
        self.duration = duration
        self.starttime = 0
        self.active=False
        self.repeat = repeat
        self.func = func

        if autostart:
            self.activate()
    
    def __bool__(self):
        return self.active
    
    def activate(self):
        self.active = True
        self.starttime = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.starttime = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.starttime >= self.duration:
                if self.func and self.starttime != 0:
                    self.func()
                self.deactivate()

        