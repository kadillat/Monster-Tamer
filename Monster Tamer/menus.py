from settings import *
from support import *
from timer import Timer


class UI:
    def __init__(self, monster,player_monsters,get_input):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.left = 1280 / 2 - 100
        self.top = 720 / 2 + 50
        self.monster = monster
        self.get_input = get_input
        self.message = ""
        self.message_timer = Timer(2000, func=self.clear_message)
        self.audio = audio_import("audio")

        self.general_options = ["attack","switch","rest","quit"]
        self.general_index = {"col" : 0, "row": 0}
        self.attack_index = {"col" : 0, "row": 0}
        self.state = "general"
        self.rows, self.cols = 2,2
        self.visible_monsters = 5
        self.player_monsters = player_monsters
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]
        self.switch_index = 0


    def clear_message(self):
        self.message = ""
    
    def input(self):
        keys = pygame.key.get_just_pressed()
        if self.state == "general":
            self.general_index["row"] = (self.general_index["row"] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
            self.general_index["col"] = (self.general_index["col"] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.audio["switch"].play()
                self.state = self.general_options[self.general_index["col"] + self.general_index["row"] * 2]
        
        elif self.state == "attack":
            self.attack_index["row"] = (self.attack_index["row"] + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % self.rows
            self.attack_index["col"] = (self.attack_index["col"] + int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) % self.cols
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                self.audio["switch"].play()
                attack = (self.monster.abilities[self.attack_index["col"] + self.attack_index["row"] * 2])
                self.get_input(self.state,attack)
                self.state = "general"
            if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                self.state = "general"
                self.audio["switch"].play()
                self.switch_index = 0
                self.general_index = {"col" : 0, "row": 0}
                self.attack_index = {"col" : 0, "row": 0}

        elif self.state == "quit":
            self.get_input("quit")

        elif self.state == "switch":
            if self.available_monsters:
                self.switch_index = (self.switch_index + int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) % len(self.available_monsters)
                if keys[pygame.K_BACKSPACE] or keys[pygame.K_ESCAPE]:
                    self.state = "general"
                    self.audio["switch"].play()
                    self.switch_index = 0
                    self.general_index = {"col" : 0, "row": 0}
                    self.attack_index = {"col" : 0, "row": 0}
                if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                    self.audio["switch"].play()
                    self.get_input(self.state,self.available_monsters[self.switch_index])
                    self.state = "general"
            if not self.available_monsters:
                self.state = "general"
                self.general_index = {"col": 0, "row": 0}
                self.attack_index = {"col": 0, "row": 0}
                self.switch_index = 0
                return
            
        elif self.state == "rest":
            self.get_input("rest")
            self.state = "general"

    def quad_select(self,index,options):
        rect = pygame.FRect(self.left + 60,self.top + 100,600,200)
        pygame.draw.rect(self.display_surface, colors["white"],rect,0,4)
        pygame.draw.rect(self.display_surface, colors["black"],rect,4,4)

        for col in range(self.cols):
            for row in range(self.rows):
                x = rect.left + rect.width / (self.cols * 2) + (rect.width / self.cols) * col
                y = rect.top + rect.height / (self.rows * 2) + (rect.height / self.rows) * row
                i = col + 2 * row
                color = colors["red"] if col == index["col"] and row == index["row"] else colors["black"]
                text_surf = self.font.render(options[i], True, color)
                text_rect = text_surf.get_frect(center = (x,y))
                self.display_surface.blit(text_surf,text_rect)


    def switch(self):
        rect = pygame.FRect(self.left + 40, self.top + -100,250,400)
        pygame.draw.rect(self.display_surface, colors["white"],rect,0,4)
        pygame.draw.rect(self.display_surface, colors["black"],rect,4,4)

        if self.switch_index < self.visible_monsters:
            voffset = 0
        else:
            voffset = -(self.switch_index - self.visible_monsters + 1) * rect.height / self.visible_monsters
        for i in range(len(self.available_monsters)):
            x = rect.centerx
            y = rect.top + rect.height / (self.visible_monsters * 2) + rect.height / self.visible_monsters * i + voffset
            if i == self.switch_index:
                color = colors["red"]
            else:
                color = colors["black"]
            name = self.available_monsters[i].name
            text_surf = self.font.render(name, True,color)
            text_rect = text_surf.get_frect(center = (x,y))
            if rect.collidepoint(text_rect.center):
                self.display_surface.blit(text_surf,text_rect)

    def stats(self):
        rect = pygame.FRect(self.left,self.top,250,80)
        pygame.draw.rect(self.display_surface, colors["white"],rect,0,4)
        pygame.draw.rect(self.display_surface, colors["grey"],rect,4,4)

        name_surf = self.font.render(self.monster.name,True,colors["black"])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.40,12))
        self.display_surface.blit(name_surf,name_rect)

        health_rect = pygame.FRect(550, name_rect.bottom + 10, rect.width * 0.9, 20)
        pygame.draw.rect(self.display_surface,colors["grey"],health_rect)
        self.bar(health_rect,self.monster.health,self.monster.maxhealth)

        health_text = f"{int(self.monster.health)}/{int(self.monster.maxhealth)}"
        health_surf = self.font.render(health_text, True, colors["black"])
        health_rect_text = health_surf.get_frect(center=health_rect.center)
        self.display_surface.blit(health_surf, health_rect_text)

    def bar(self,rect,value,max_value):
        ratio = rect.width / max_value
        p_rect = pygame.FRect(rect.topleft, (value * ratio,rect.height))
        pygame.draw.rect(self.display_surface, colors["red"],p_rect)

    def draw_player_monster_lives(self):
        x = 20
        y = 580
        size = 14
        spacing = 6

        for i in range(6):
            if i < len(self.player_monsters):
                monster = self.player_monsters[i]
                color = colors["green"] if monster.health > 0 else colors["grey"]
            else:
                color = colors["black"]

            rect = pygame.Rect(x, y + i * (size + spacing), size, size)
            pygame.draw.rect(self.display_surface, color, rect)
            pygame.draw.rect(self.display_surface, colors["black"], rect, 2)



    def update(self):
        self.input()
        self.available_monsters = [monster for monster in self.player_monsters if monster != self.monster and monster.health > 0]
        self.message_timer.update()
        
    def draw(self):
        match self.state:
            case "general":
                self.quad_select(self.general_index,self.general_options)
            case "attack":
                self.quad_select(self.attack_index, self.monster.abilities)
            case "switch":
                self.switch()

        if self.state != "switch":
            self.stats()

        if self.message:
            message_rect = pygame.FRect(340, 310, 600, 50)
            pygame.draw.rect(self.display_surface, colors["white"], message_rect, 0, 4)
            pygame.draw.rect(self.display_surface, colors["black"], message_rect, 2, 4)
            text_surf = self.font.render(self.message, True, colors["black"])
            text_rect = text_surf.get_frect(center=message_rect.center)
            self.display_surface.blit(text_surf, text_rect)
            
        self.draw_player_monster_lives()





class EnemyUI:
    def __init__(self, monster, selected_enemies=None):
        self.display_surface = pygame.display.get_surface()
        self.monster = monster
        self.font = pygame.font.Font(None,30)
        self.selected_enemies = selected_enemies or []

    def draw_enemy_monster_lives(self):
        x = 1240
        y = 30
        size = 14
        spacing = 6

        for i in range(3):
            if i < len(self.selected_enemies):
                monster = self.selected_enemies[i]
                color = colors["green"] if monster.health > 0 else colors["grey"]
            else:
                color = colors["black"]

            rect = pygame.Rect(x, y + i * (size + spacing), size, size)
            pygame.draw.rect(self.display_surface, color, rect)
            pygame.draw.rect(self.display_surface, colors["black"], rect, 2)

        
    def draw(self):
        rect = pygame.FRect((0,0), (250,80)).move_to(midleft = (450, self.monster.rect.centery))
        pygame.draw.rect(self.display_surface, colors["white"],rect,0,4)
        pygame.draw.rect(self.display_surface, colors["grey"],rect,4,4)

        name_surf = self.font.render(self.monster.name,True,colors["black"])
        name_rect = name_surf.get_frect(topleft = rect.topleft + pygame.Vector2(rect.width * 0.40,12))
        self.display_surface.blit(name_surf,name_rect)

        health_rect = pygame.FRect(460,name_rect.bottom +10,rect.width * 0.9,20)
        ratio = health_rect.width / self.monster.maxhealth
        p_rect = pygame.FRect(health_rect.topleft,(self.monster.health * ratio,health_rect.height))
        pygame.draw.rect(self.display_surface,colors["grey"],health_rect)
        pygame.draw.rect(self.display_surface,colors["red"],p_rect)

        health_text = f"{int(self.monster.health)}/{int(self.monster.maxhealth)}"
        health_surf = self.font.render(health_text, True, colors["black"])
        health_rect_text = health_surf.get_frect(center=health_rect.center)
        self.display_surface.blit(health_surf, health_rect_text)
        self.draw_enemy_monster_lives()