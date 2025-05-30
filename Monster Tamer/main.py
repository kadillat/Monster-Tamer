
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
os.chdir(script_dir)

from settings import *
from support import *
from menus import *
from timer import Timer
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
        self.state = "opening"
        self.selected_monsters = []
        self.selected_enemies = []
        self.intro_music_started = False
        self.import_assets()
        self.player_active = True
        self.enemy_counter = 0
        self.selection_index = 0



        player_monsterlist = ["Batty","Flare","Groudon","Hornet","Hydro","Jelly","Kamai","Lorri","Pla","Slyph","Windy","Pav"]
        enemy_monsterlist = ["Behemoth","Cerberus","Crow","Garuda","Ghost","Helm","Keltos","Kraken","Reaper","Wolvem"]
        self.player_monsters = [Monster(name, self.player_monsterimages[name], self.sprites) for name in player_monsterlist]
        self.enemy_monsters = [Enemy(name,self.enemy_monsterimages[name],self.sprites) for name in enemy_monsterlist]
        for i in range(3):
            enemy_number = int(random.randint(0, len(enemy_monsterlist)-1))
            enemy = Enemy(enemy_monsterlist[enemy_number], self.enemy_monsterimages[enemy_monsterlist[enemy_number]], self.sprites)
            enemy_monsterlist.remove(enemy_monsterlist[enemy_number])
            self.selected_enemies.append(enemy)
        self.player_number = int(random.randint(0,9))
        self.player_name = player_monsterlist[self.player_number]
        # self.player = self.player_monsters[self.player_number]
        self.player_sprite = self.player_monsters[self.player_number]
        self.current_enemy_index = 0
        self.enemy = self.selected_enemies[self.current_enemy_index]
        # self.sprites.add(self.player)
        self.sprites.add(self.enemy)


        self.enemy_ui = EnemyUI(self.enemy, self.selected_enemies)

        self.timers = {
            "player end": Timer(1000, func = self.enemy_turn),
            "enemy end": Timer(1000,func=self.player_turn)
            }
        
            
    def draw_selection_screen(self):
        self.display_surface.fill("white")
        font = pygame.font.Font(None, 36)
        title_surf = font.render("Choose 6 Monsters", True, "black")
        title_rect = title_surf.get_rect(center=(1280 // 2, 80))
        self.display_surface.blit(title_surf, title_rect)

        spacing_x = 200
        spacing_y = 100
        start_x = (1280 - (spacing_x * 4)) // 2
        start_y = (720 - (spacing_y * 3)) // 2 

        for i, monster in enumerate(self.player_monsters):
            col = i % 4
            row = i // 4
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            rect = pygame.Rect(x, y, 150, 60)

            if monster in self.selected_monsters:
                border_color = "green"
            elif i == self.selection_index:
                border_color = "red"
            else:
                border_color = "black"

            pygame.draw.rect(self.display_surface, border_color, rect, 3)

            name_surf = font.render(monster.name, True, "black")
            self.display_surface.blit(name_surf, (x + 10, y + 20))


    def get_input(self,state,data = None):
        if state == "attack":
            self.apply_attack(self.enemy,data)

        elif state == "rest":
            print(self.player.health)
            heal_amount = random.randint(15,30)
            self.player.health += heal_amount
            print(self.player.health)
            AttackAnimation(self.player,self.attack_frames["heal"],self.sprites)
            self.audio["heal"].play()
            self.ui.message = f"{self.player.name} rested, it gained {heal_amount} health!"
            self.ui.message_timer.activate()

        elif state == "switch":
            self.player.kill()
            self.audio["switch"].play()
            self.player = data
            self.sprites.add(self.player)
            self.ui.monster = self.player

        elif state == "quit":
            self.run = False

        self.player_active = False
        self.timers["player end"].activate()


    def apply_attack(self,target,attack):
        attack_data = ability_data[attack]
        if attack_data == "Scratch" or "Ember" or "Splash" or "Tackle":
            base_damage = random.randint(8,16)
        if attack_data == "Slash" or "Explosion" or "Darkness" or "Tidal wave" or "Shock bolt" or "Throw rock" or "Tornado":
            base_damage = random.randint(10,25)
        if attack_data == "Ice shard" or "Earthquake" or "Flame burst" or "Radiance" or "Dark Thunder":
            base_damage = random.randint(13,30)
        target_element = target.element
        attack_element = attack_data["element"]
        attack_multiply = element_data[attack_element][target_element]
        AttackAnimation(target,self.attack_frames[attack_data["animation"]],self.sprites)
        self.audio[attack_data["animation"]].play()
        print(attack)
        print(base_damage * attack_multiply)
        damage = base_damage * attack_multiply
        target.health -= damage
        print(target.health,"/",target.maxhealth)

        if isinstance(target, Enemy):
            actor_name = self.player.name
        else:
            actor_name = self.enemy.name
        attack_text = f"{actor_name} used {attack}, dealt {int(damage)} damage!"
        self.ui.message = attack_text
        self.ui.message_timer.activate()


    def enemy_turn(self):

        if self.enemy.health <= 0:
            self.player_active = True
            self.enemy.kill()
            self.current_enemy_index += 1
            
            if self.current_enemy_index < len(self.selected_enemies):
                self.enemy = self.selected_enemies[self.current_enemy_index]
                self.enemy_ui.monster = self.enemy
                self.sprites.add(self.enemy)
            else:
                self.run = False
        else:
            attack = random.choice(self.enemy.abilities)
            self.apply_attack(self.player, attack)
            self.timers["enemy end"].activate()

    def player_turn(self):
        self.player_active = True
        if self.player.health <= 0:
            available_monsters = [monster for monster in self.player_monsters if monster.health >= 1]
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

    def handle_opening_input(self):
        keys = pygame.key.get_just_pressed()
        if any(keys):
            self.audio["switch"].play()
            self.state = "selection"

    def draw_opening_screen(self, dt):
        if not self.intro_music_started:
            self.audio["intro"].play()
            self.intro_music_started = True
        self.display_surface.blit(self.backgrounds["intro"], (0, 0))

    def handle_opening_input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.audio["intro"].stop()
            self.audio["switch"].play()
            self.audio["music"].play(-1)
            self.state = "selection"




    def draw_floor(self):
        for sprite in self.sprites:
            if hasattr(sprite, "name"):
                floor_rect = self.backgrounds["floor"].get_frect(center = sprite.rect.midbottom + pygame.Vector2(0,-10))
                self.display_surface.blit(self.backgrounds["floor"], floor_rect)

    def handle_selection_input(self):

        keys = pygame.key.get_just_pressed()
        monster_count = len(self.player_monsters)
        row_size = 4

        if keys[pygame.K_RIGHT]:
            self.audio["switch"].play()
            self.selection_index = (self.selection_index + 1) % monster_count
        if keys[pygame.K_LEFT]:
            self.audio["switch"].play()
            self.selection_index = (self.selection_index - 1) % monster_count
        if keys[pygame.K_DOWN]:
            self.audio["switch"].play()
            self.selection_index = (self.selection_index + row_size) % monster_count
        if keys[pygame.K_UP]:
            self.audio["switch"].play()
            self.selection_index = (self.selection_index - row_size) % monster_count

        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            self.audio["choose"].play()
            monster = self.player_monsters[self.selection_index]
            if monster not in self.selected_monsters:
                self.selected_monsters.append(monster)
                if len(self.selected_monsters) == 6:
                    self.start_battle()


    def start_battle(self):
        self.player_monsters = self.selected_monsters
        self.player_number = 0
        self.player = self.player_monsters[self.player_number]
        self.sprites.add(self.player)

        self.ui = UI(self.player, self.player_monsters, self.get_input)
        self.state = "battle"




    def start(self):
        while self.run:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            if self.state == "opening":
                self.handle_opening_input()
                self.draw_opening_screen(dt)

            elif self.state == "selection":
                self.handle_selection_input()
                self.draw_selection_screen()

            elif self.state == "battle":
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

        self.run = False


if __name__ == "__main__":
    game = Game()
    game.start()