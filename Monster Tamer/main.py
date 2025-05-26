from settings import *
from support import *
from menus import *
from timer import *
from monster import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Monster Tamer [Demo]")
        self.run = True
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.import_assets()



        player_monsterlist = ["Batty","Flare","Groudon","Hornet","Hydro","Jelly","Kamai","Lorri","Pla","Slyph","Windy"]
        enemy_monsterlist = ["Behemoth","Cerberus","Crow","Garuda","Ghost","Helm","Keltos","Kraken","Reaper","Wolvem"]
        self.player_monsters = [Monster(name,self.player_monsterimages[name]) for name in player_monsterlist]
        self.enemy_monsters = [Enemy(name,self.enemy_monsterimages[name]) for name in enemy_monsterlist]
        self.monster_sprite = self.player_monsters[random.randint(0,10)]
        self.sprites.add(self.monster_sprite)
        self.enemy_sprite = self.enemy_monsters[random.randint(0,9)]
        self.sprites.add(self.enemy_sprite)

        self.ui = UI(self.monster_sprite,self.player_monsters)

    def import_assets(self):
        self.player_monsterimages = folder_import("player")
        self.backgrounds = folder_import("otherimg")
        self.enemy_monsterimages = folder_import("enemies")

    def draw_floor(self):
        for sprite in self.sprites:
            floor_rect = self.backgrounds["floor"].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0,-10))
            self.display_surface.blit(self.backgrounds["floor"], floor_rect)

    def start(self):
        while self.run:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.sprites.update(dt)
            self.ui.update()
            self.display_surface.blit(self.backgrounds["2"], (0,0))
            self.draw_floor()
            self.sprites.draw(self.display_surface)
            self.ui.draw()
            pygame.display.update()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.start()