import pygame
import sys
import worm
from settings import *
from pygame.math import Vector2 as vect
import map
import maps
import weapons
import random
import textures
import pandas


class Game(object):

    def __init__(self):
        # Config
        self.tps_max = FPS

        # Initialization
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.running = False
        self.teams = {0: worm.Team(self, "sorcerer", 1, "Player 1"),
                      1: worm.Team(self, "warlock", 2, "Player 2")}
        self.map = maps.MapForest()
        self.bullets = pygame.sprite.Group()
        self.grenades = pygame.sprite.Group()
        self.language = "PL"
        self.resources = pandas.read_csv(r"resources.txt", delimiter=";", dtype="str")
        self.sound = 1
        if self.sound == 0:
            pygame.mixer.music.pause()

    def new(self):

        if self.game_over():
            self.replay()
        self.turn = 0
        self.teams[1 - self.turn].active = 0
        self.turn_time = TURN_TIME
        self.start_pos()
        self.camera = map.Camera(WIDTH, HEIGHT)
        self.start_tick = pygame.time.get_ticks()
        self.run()

    def run(self):
        pygame.mixer.music.load('sound/battle.mp3')
        pygame.mixer.music.play(-1)
        while not self.game_over():

            # Ticking
            self.tps_delta += self.tps_clock.tick(self.tps_max) / 1000.0
            while self.tps_delta > 1 / self.tps_max:
                self.tps_delta -= 1 / self.tps_max
                self.take_turn()
                self.event()
                self.update()

            # Rendering
            pygame.display.flip()
            self.draw()

    def show_start_screen(self):
        waiting = True
        while waiting:
            self.tps_clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            background = pygame.transform.scale(textures.get_image("textures/background.png"), (1280, 720))
            menu = textures.get_image("textures/menu.png")
            title = textures.get_image("textures/wizards.png")
            copyright = "(C) 2018 Mateusz Kobyłka"
            self.screen.blit(background, (0, 0))
            self.screen.blit(menu, (WIDTH / 2 - 200, HEIGHT - 400))
            self.screen.blit(FONT_DETAIL.render(copyright, 1, WHITE),(WIDTH - 220,HEIGHT - 20))
            self.screen.blit(title, (WIDTH/2 - 850/2, 0) )

            textures.text_to_button(self, self.resources.loc[self.resources["K"] == "K_play"][self.language].values[0],
                                    WIDTH / 2 - 300 / 2, 340, 300, 50,
                                    FONT_MENU, BLACK, WHITE, "play")
            textures.text_to_button(self,
                                    self.resources.loc[self.resources["K"] == "K_options"][self.language].values[0],
                                    WIDTH / 2 - 300 / 2, 440, 300, 50, FONT_MENU, BLACK, WHITE, "options")
            textures.text_to_button(self,
                                    self.resources.loc[self.resources["K"] == "K_instructions"][self.language].values[
                                        0],
                                    WIDTH / 2 - 300 / 2, 540, 300, 50, FONT_MENU, BLACK, WHITE, "instructions")
            textures.text_to_button(self, self.resources.loc[self.resources["K"] == "K_quit"][self.language].values[0],
                                    WIDTH / 2 - 300 / 2, 640, 300, 50,
                                    FONT_MENU, BLACK, WHITE, "quit")

            pygame.display.flip()

    def options_screen(self):
        waiting = True

        team1_name = textures.Input_box(WIDTH / 4 - (186 / 2), 2 * HEIGHT / 10 - 10, 186, 40, self.teams[0].team_name,
                                        FONT_PLAYERS)
        team2_name = textures.Input_box(3 * WIDTH / 4 - (186 / 2), 2 * HEIGHT / 10 - 10, 186, 40,
                                        self.teams[1].team_name, FONT_PLAYERS)

        while waiting:
            self.tps_clock.tick(30)

            background = pygame.transform.scale(textures.get_image("textures/options.png"), (1280, 720))
            topinfo = textures.get_image("textures/hang.png")
            sign = pygame.transform.scale(textures.get_image("textures/arrow_back.png"), (100, 100))
            frame = pygame.transform.scale(textures.get_image("textures/frame.png"), (186, 238))
            character_1 = textures.get_character(self.teams[0].player_1.character)
            character_2 = textures.get_character(self.teams[1].player_1.character)
            switch_l1 = pygame.transform.scale(
                textures.get_image("textures/switch_l_" + self.teams[0].player_1.character + ".png"), (25, 25))
            switch_r1 = pygame.transform.scale(
                textures.get_image("textures/switch_r_" + self.teams[0].player_1.character + ".png"), (25, 25))
            switch_l2 = pygame.transform.scale(
                textures.get_image("textures/switch_l_" + self.teams[1].player_1.character + ".png"), (25, 25))
            switch_r2 = pygame.transform.scale(
                textures.get_image("textures/switch_r_" + self.teams[1].player_1.character + ".png"), (25, 25))
            language = pygame.transform.scale(textures.get_image("textures/" + self.language + ".png"), (64, 64))
            sound = pygame.transform.scale(textures.get_image("textures/megaphone" + str(self.sound) + ".png"),
                                           (64, 64))
            save = pygame.transform.scale(textures.get_image("textures/save.png"), (64, 64))
            versus = pygame.transform.scale(textures.get_image("textures/versus.png"), (120, 100))

            self.screen.blit(background, (0, 0))
            self.screen.blit(topinfo, (WIDTH / 2 - 200, 0))
            self.screen.blit(sign, (50, HEIGHT - 100))
            self.screen.blit(frame, (WIDTH / 4 - (186 / 2), HEIGHT / 4))
            self.screen.blit(frame, (3 * WIDTH / 4 - (186 / 2), HEIGHT / 4))
            self.screen.blit(character_1, (WIDTH / 4 - (186 / 2) + 25, HEIGHT / 4 + 30))
            self.screen.blit(character_2, (3 * WIDTH / 4 - (186 / 2) + 25, HEIGHT / 4 + 30))
            self.screen.blit(switch_l1, (WIDTH / 4 - (186 / 2) - 40, HEIGHT / 4 + 248))
            self.screen.blit(switch_r1, (WIDTH / 4 + (186 / 2) + 10, HEIGHT / 4 + 248))
            self.screen.blit(switch_l2, (3 * WIDTH / 4 - (186 / 2) - 40, HEIGHT / 4 + 248))
            self.screen.blit(switch_r2, (3 * WIDTH / 4 + (186 / 2) + 10, HEIGHT / 4 + 248))

            options = self.resources.loc[self.resources["K"] == "K_options"][self.language].values[0]

            self.screen.blit(FONT_MENU.render(options, 1, WHITE), (WIDTH / 2  - 55, 30))

            character_1_type = self.resources.loc[self.resources["K"] == "K_class"][self.language].values[0] + \
                               self.teams[0].player_1.character
            character_2_type = self.resources.loc[self.resources["K"] == "K_class"][self.language].values[0] + \
                               self.teams[1].player_1.character

            self.screen.blit(
                FONT_PLAYERS.render(character_1_type, 1, textures.get_team_color(self.teams[0].player_1.character)),
                (WIDTH / 4 - (186 / 2), HEIGHT / 4 + 250))
            self.screen.blit(
                FONT_PLAYERS.render(character_2_type, 1, textures.get_team_color(self.teams[1].player_1.character)),
                (3 * WIDTH / 4 - (186 / 2), HEIGHT / 4 + 250))
            self.screen.blit(language, (WIDTH / 2 - 32, 5 * HEIGHT / 7))
            self.screen.blit(sound, (WIDTH / 2 - 32, 6 * HEIGHT / 7))
            self.screen.blit(save, (WIDTH - 80, 6 * HEIGHT / 7 + 10))
            self.screen.blit(versus, (WIDTH / 2 - 60, HEIGHT / 2 - 100))

            self.screen.blit(FONT_OPTIONS.render(
                self.resources.loc[self.resources["K"] == "K_player"][self.language].values[0] + " 1",
                1, textures.get_team_color(self.teams[0].player_1.character)), (WIDTH / 4 - (186 / 2), HEIGHT / 10))
            self.screen.blit(FONT_OPTIONS.render(
                self.resources.loc[self.resources["K"] == "K_player"][self.language].values[0] + " 2",
                1, textures.get_team_color(self.teams[1].player_1.character)), (3 * WIDTH / 4 - (186 / 2), HEIGHT / 10))

            back_button = pygame.rect.Rect(vect(50, HEIGHT - 80), vect(100, 30))
            textures.text_to_button(self, self.resources.loc[self.resources["K"] == "K_back"][self.language].values[0],
                                    back_button.x, back_button.y, back_button.width, back_button.height,
                                    FONT_OPTIONS, BLACK, WHITE, "back")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    textures.switch_character_type_button(self, 0, WIDTH / 4 - (186 / 2) - 40, HEIGHT / 4 + 248,
                                                          25, 25, "backward")
                    textures.switch_character_type_button(self, 0, WIDTH / 4 + (186 / 2) + 10, HEIGHT / 4 + 248,
                                                          25, 25, "forward")
                    textures.switch_character_type_button(self, 1, 3 * WIDTH / 4 - (186 / 2) - 40,
                                                          HEIGHT / 4 + 248, 25, 25, "backward")
                    textures.switch_character_type_button(self, 1, 3 * WIDTH / 4 + (186 / 2) + 10,
                                                          HEIGHT / 4 + 248, 25, 25, "forward")
                    textures.switch_language_button(self, WIDTH / 2 - 32, 5 * HEIGHT / 7, 64, 64)
                    textures.switch_sound_button(self, WIDTH / 2 - 32, 6 * HEIGHT / 7, 64, 64)
                    textures.save_button(self, WIDTH - 80, 6 * HEIGHT / 7 + 10, 64, 64)

                team1_name.handle_event(event)
                team2_name.handle_event(event)

            team1_name.draw(self.screen)
            team2_name.draw(self.screen)
            self.teams[0].team_name = team1_name.text
            self.teams[1].team_name = team2_name.text

            pygame.display.flip()

    def instructions_screen(self):
        waiting = True

        while waiting:
            self.tps_clock.tick(30)

            background = pygame.transform.scale(textures.get_image("textures/instructions.jpg"), (1280,720))
            topinfo = textures.get_image("textures/hang.png")
            sign = pygame.transform.scale(textures.get_image("textures/arrow_back.png"), (100, 100))

            leftright = pygame.transform.scale(textures.get_image("textures/instructions/leftright.png"),(196,50))
            up = pygame.transform.scale(textures.get_image("textures/instructions/up.png"),(196,50))
            space = pygame.transform.scale(textures.get_image("textures/instructions/space.png"),(196,50))
            b = pygame.transform.scale(textures.get_image("textures/instructions/B.png"),(196,50))
            tab = pygame.transform.scale(textures.get_image("textures/instructions/tab.png"),(196,50))

            self.screen.blit(background, (0, 0))
            self.screen.blit(sign, (50, HEIGHT - 100))
            self.screen.blit(topinfo, (WIDTH / 2 - 200, 0))
            self.screen.blit(leftright, (40, 150))
            self.screen.blit(up, (40, 250))
            self.screen.blit(space, (40, 350))
            self.screen.blit(b, (40, 450))
            self.screen.blit(tab, (40, 550))

            leftright_info = self.resources.loc[self.resources["K"] == "K_move"][self.language].values[0]
            up_info = self.resources.loc[self.resources["K"] == "K_up"][self.language].values[0]
            space_info = self.resources.loc[self.resources["K"] == "K_space"][self.language].values[0]
            b_info = self.resources.loc[self.resources["K"] == "K_b"][self.language].values[0]
            tab_info = self.resources.loc[self.resources["K"] == "K_tab"][self.language].values[0]

            self.screen.blit(FONT_OPTIONS.render(leftright_info,1,WHITE), (340,150))
            self.screen.blit(FONT_OPTIONS.render(up_info,1,WHITE), (340,250))
            self.screen.blit(FONT_OPTIONS.render(space_info,1,WHITE), (340,350))
            self.screen.blit(FONT_OPTIONS.render(b_info,1,WHITE), (340,450))
            self.screen.blit(FONT_OPTIONS.render(tab_info,1,WHITE), (340,550))

            instructions = self.resources.loc[self.resources["K"] == "K_instructions"][self.language].values[0]

            self.screen.blit(FONT_MENU.render(instructions, 1, WHITE), (WIDTH / 2  - 110, 30))

            back_button = pygame.rect.Rect(vect(50, HEIGHT - 80), vect(100, 30))
            textures.text_to_button(self, self.resources.loc[self.resources["K"] == "K_back"][self.language].values[0],
                                    back_button.x, back_button.y, back_button.width, back_button.height,
                                    FONT_OPTIONS, BLACK, WHITE, "back")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            pygame.display.flip()

    def show_game_over_screen(self):
        waiting = True

        while waiting:
            self.tps_clock.tick(30)

            background = pygame.transform.scale(textures.get_image("textures/instructions.jpg"), (1280, 720))
            self.screen.blit(background, (0, 0))

            win = self.resources.loc[self.resources["K"] == "K_win"][self.language].values[0]
            info = str(self.teams[self.winner()-1].team_name) + win
            back = self.resources.loc[self.resources["K"] == "K_press"][self.language].values[0]

            self.screen.blit(FONT_MENU.render(info, 1, WHITE), (WIDTH / 2 - 300, 10))

            self.screen.blit(FONT_MENU.render(back, 1, WHITE), (WIDTH / 2 - 300, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

        pygame.display.flip()

    def update(self):
        self.map.update()
        self.bullets.update(self)
        self.grenades.update(self)
        for i in range(0, 2):
            self.teams[i].update()

            hitbullet = pygame.sprite.groupcollide(self.teams[1 - self.turn], self.bullets, False, True)
            for hit in hitbullet:
                hit.health -= random.randint(BULLET_DAMAGE, 2 * BULLET_DAMAGE)

            hitgrenade = pygame.sprite.groupcollide(self.teams[1 - self.turn], self.grenades, False, True)
            for hit in hitgrenade:
                hit.health -= random.randint(GRENADE_DAMAGE, 2 * GRENADE_DAMAGE)

            for j in range(0, 4):
                if self.teams[i].players[j].vel.y > 0:
                    hitmap = pygame.sprite.spritecollide(self.teams[i].players[j], self.map.platforms, False)
                    if hitmap:
                        self.teams[i].players[j].pos.y = hitmap[0].rect.top + 10
                        self.teams[i].players[j].vel.y = 0
        self.camera.update(self.teams[self.turn].players[self.teams[self.turn].chosen_player])

    def event(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.teams[self.turn].players[self.teams[self.turn].chosen_player].jump()
                if event.key == pygame.K_TAB:
                    self.teams[self.turn].switch_character()
                if event.key == pygame.K_SPACE and self.teams[self.turn].left_bullets != 0:
                    weapons.Wand(self, self.teams[self.turn].players[self.teams[self.turn].chosen_player])
                    self.teams[self.turn].left_bullets -= 1
                if event.key == pygame.K_b and self.teams[self.turn].left_grenades != 0:
                    weapons.Grenade(self, self.teams[self.turn].players[self.teams[self.turn].chosen_player])
                    self.teams[self.turn].left_grenades -= 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        for sprite in self.map.objects:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.teams[0]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.teams[1]:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.bullets:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.grenades:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

    def winner(self):
        if self.teams[0].get_team_health() <= 0:
            return self.teams[0].team_number
        elif self.teams[1].get_team_health() <= 0:
            return self.teams[0].team_number
        else:
            return 0

    def game_over(self):
        return self.winner() != 0

    def replay(self):
        for i in range(0,2):
            self.teams[i] = worm.Team(self, self.teams[i].character, i + 1, self.teams[i].team_name)

    def start_pos(self):
        for i in self.teams:
            for j in self.teams[i].players:
                self.teams[i].players[j].pos = vect(random.randint(0, 2 * WIDTH), 0)

    def take_turn(self):
        now = pygame.time.get_ticks() - self.start_tick
        seconds = TURN_TIME - int((now - self.turn_time) / 1000) - 1
        seconds_str = "0" + str(seconds)
        seconds_str = seconds_str[-2:]
        col = BLACK
        if now - self.turn_time > TURN_TIME * 1000 - 5000:
            col = RED
        scroll = pygame.transform.scale(textures.get_image("textures/scroll.png"), (60, 60))
        self.screen.blit(scroll, (50, HEIGHT - 100))
        self.screen.blit(FONT_TIME.render(seconds_str, 1, col), (65, HEIGHT - 82))
        if now - self.turn_time > TURN_TIME * 1000 or (
                self.teams[self.turn].left_bullets == 0 and self.teams[self.turn].left_grenades == 0
                and len(self.grenades) == 0 and len(self.bullets) == 0):
            self.turn_time = now
            self.teams[self.turn].left_grenades = 1
            self.teams[self.turn].left_bullets = 3
            self.turn = 1 - self.turn
            self.teams[self.turn].active = 1
            self.teams[1 - self.turn].active = 0
            self.teams[1 - self.turn].players[self.teams[1 - self.turn].chosen_player].vel = vect(0, 0)
            self.teams[1 - self.turn].players[self.teams[1 - self.turn].chosen_player].acc = vect(0, 0)

    def switch_language(self):
        languages = ["EN", "PL"]
        self.language = languages[(languages.index(self.language) + 1) % 2]

    def switch_sound(self):
        self.sound = 1 - self.sound

    def load_settings(self):
        settings = pandas.read_csv(r"settings.txt", delimiter=";", dtype="str")
        self.language = settings.loc[0][2]
        self.sound = int(settings.loc[1][2])
        self.teams[0].change_character_type(settings.loc[2][2])
        self.teams[1].change_character_type(settings.loc[3][2])
        self.teams[0].team_name = settings.loc[4][2]
        self.teams[1].team_name = settings.loc[5][2]

    def save_settings(self):
        settings = pandas.DataFrame({"Variable": ["language", "sound", "class1", "class2", "team1_name", "team2_name"],
                                     "Values": [self.language, self.sound, self.teams[0].character,
                                                self.teams[1].character,
                                                self.teams[0].team_name, self.teams[1].team_name]})
        settings.columns = ["Variable", "Value"]
        settings.to_csv("settings.txt", sep=";", encoding="utf-8")

    def play_music(self):
        if self.sound == 1:
            pygame.mixer.music.play(-1)


if __name__ == "__main__":
    g = Game()
    g.load_settings()
    g.show_start_screen()
    pygame.quit()
