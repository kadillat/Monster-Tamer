from settings import *
from support import *
from menus import *
from timer import *
from monster import *
from animation import *


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280,720))
        pygame.display.set_caption("Monster Tamer [Demo]")
        self.run = True
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.import_assets()
        self.audio["music"].play(-1)
        self.player_active = True
        self.enemy_counter = 0



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

        elif state == "rest":
            print(self.player.health)
            self.player.health += random.randint(15,30)
            print(self.player.health)
            AttackAnimation(self.player,self.attack_frames["heal"],self.sprites)
            self.audio["heal"].play()

        elif state == "switch":
            self.player.kill()
            self.player = data
            self.sprites.add(self.player)
            self.ui.monster = self.player

        self.player_active = False
        self.timers["player end"].activate()


    def apply_attack(self,target,attack):
        attack_data = ability_data[attack]
        base_damage = attack_data["damage"]
        target_element = target.element
        attack_element = attack_data["element"]
        attack_multiply = element_data[attack_element][target_element]
        AttackAnimation(target,self.attack_frames[attack_data["animation"]],self.sprites)
        self.audio[attack_data["animation"]].play()
        print(attack)
        print(base_damage * attack_multiply)
        
        target.health -= base_damage * attack_multiply
        print(target.health,"/",target.maxhealth)


    def enemy_turn(self):
        if self.enemy.health <= 0:
            self.player_active = True
            self.enemy.kill()
            self.enemy_number = int(random.randint(0,9))
            self.enemy = self.enemy_monsters[self.enemy_number]
            self.enemy_ui.monster = self.enemy
            self.sprites.add(self.enemy)
            self.enemy_counter += 1
            if self.enemy_counter == 3:
                pygame.quit()



        else:
            attack = random.choice(self.enemy.abilities)
            self.apply_attack(self.player,attack)
            self.timers["enemy end"].activate()

    def player_turn(self):
        self.player_active = True
        if self.player.health <= 0:
            available_monsters = [monster for monster in self.player_monsters if monster.health > 0]
            if available_monsters:
                self.player.kill()
                self.player = available_monsters[0]
                self.sprites.add(self.player)
                self.ui.monster = self.player
            else:
                self.run = False


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.player_monsterimages = folder_import("player")
        self.backgrounds = folder_import("otherimg")
        self.enemy_monsterimages = folder_import("enemies")
        self.attack_frames = tile_importer(4,"attacks")
        self.audio = audio_import("audio")

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