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
        self.player_active = True



        player_monsterlist = ["Batty","Flare","Groudon","Hornet","Hydro","Jelly","Kamai","Lorri","Pla","Slyph","Windy"]
        enemy_monsterlist = ["Behemoth","Cerberus","Crow","Garuda","Ghost","Helm","Keltos","Kraken","Reaper","Wolvem"]
        self.player_monsters = [Monster(name, self.player_monsterimages[name], self.sprites) for name in player_monsterlist]
        self.enemy_monsters = [Enemy(name,self.enemy_monsterimages[name],self.sprites) for name in enemy_monsterlist]
        self.player_number = int(random.randint(0,9))
        self.player_name = player_monsterlist[self.player_number]
        self.player = self.player_monsters[self.player_number]
        self.player_sprite = self.player_monsters[self.player_number]
        self.enemy_number = int(random.randint(0,9))
        self.enemy_sprite = self.enemy_monsters[self.enemy_number]
        self.enemy_name = enemy_monsterlist[self.enemy_number] 
        self.enemy = self.enemy_monsters[self.enemy_number]
        self.sprites.add(self.player)
        self.sprites.add(self.enemy)

        self.ui = UI(self.player, self.player_monsters, self.get_input)
        self.enemy_ui = EnemyUI(self.enemy)

        self.timers = {
            "player end": Timer(1000, func = self.enemy_turn),
            "enemy end": Timer(1000,func=self.player_turn)
            }

    def get_input(self,state,data = None):
        if state == "attack":
            self.apply_attack(self.enemy,data)
        
        self.player_active = False
        self.timers["player end"].activate()


    def apply_attack(self,target,attack):
        attack_data = ability_data[attack]
        base_damage = attack_data["damage"]
        target_element = target.element
        attack_element = attack_data["element"]
        attack_multiply = element_data[attack_element][target_element]
        print(attack)
        print(base_damage * attack_multiply)
        
        target.health -= base_damage * attack_multiply
        print(target.health,"/",target.maxhealth)


    def enemy_turn(self):
        attack = random.choice(self.enemy.abilities)
        self.apply_attack(self.player,attack)
        self.timers["enemy end"].activate()

    def player_turn(self):    
        self.player_active = True


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

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
            self.update_timers()
            self.sprites.update(dt)
            if self.player_active:
                self.ui.update()
            self.display_surface.blit(self.backgrounds["2"], (0,0))
            self.draw_floor()
            self.sprites.draw(self.display_surface)
            self.ui.draw()
            self.enemy_ui.draw()
            pygame.display.update()
        

        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.start()