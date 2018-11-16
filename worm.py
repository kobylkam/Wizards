import pygame
import textures
import map
from pygame.math import Vector2 as vect
from settings import *
from os import path


class Player(pygame.sprite.Sprite):
    def __init__(self, game, character):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.character = character
        self.facing = 1
        self.faces = textures.get_faces(self.character)
        self.image = self.faces[self.facing]
        self.rect = self.image.get_rect()
        self.pos = vect(0, 0)
        self.vel = vect(0, 0)
        self.acc = vect(0, 0)

        self.health = PLAYER_HEALTH
        self.dead = 0

        self.explosion = {}
        for i in range(1, 25):
            e = "0" + str(i)
            e = e[-2:] + ".png"
            self.explosion[i] = pygame.transform.scale(textures.get_image(path.join("textures", self.character, "explosion", e)), (60, 60))
        self.current_frame = 0
        self.last_update = 0
        self.health_bar = pygame.rect.Rect(self.rect.midtop + vect(-30, -10), vect(self.rect.width, 5))

    def update(self):

        self.acc.y = PLAYER_GRAVITY

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        if self.health <= 0:
            if self.dead == 0:
                self.explode()
                if self.current_frame == 6:
                    map.Grave(self.game, self)

        if self.rect.top > HEIGHT:
            self.health = 0

    def move(self):

        self.acc = vect(0, PLAYER_GRAVITY)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.facing = -1
            self.image = self.faces[self.facing]
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.facing = 1
            self.image = self.faces[self.facing]

    def jump(self):
        self.rect.y += 1
        hitsmap = pygame.sprite.spritecollide(self, self.game.map, False)
        self.rect.y -= 1
        if hitsmap:
            self.vel.y = -10

    def explode(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > 25:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.explosion)
            self.image = self.explosion[self.current_frame]
        if self.current_frame == 23:
            self.kill()
            self.dead = 1

    def draw_health(self):
        if self.health > 90:
            col = GREEN
        elif self.health > 60:
            col = LIGHTGREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        if self.health > 0:
            width = (self.rect.width * self.health / 100)
            height = 3
            self.health_bar = pygame.rect.Rect(self.rect.midtop + vect(-30, -10), vect(width, height))
            pygame.draw.rect(self.game.screen, col, self.game.camera.apply_rect(self.health_bar))


class Team(pygame.sprite.Group):
    def __init__(self, game, character, number, name):
        self.game = game
        pygame.sprite.Group.__init__(self)

        self.team_number = number
        self.team_name = name
        self.character = character

        self.player_1 = Player(game, self.character)
        self.player_2 = Player(game, self.character)
        self.player_3 = Player(game, self.character)
        self.player_4 = Player(game, self.character)

        self.add(self.player_1)
        self.add(self.player_2)
        self.add(self.player_3)
        self.add(self.player_4)

        self.players = { 0: self.player_1,
                         1: self.player_2,
                         2: self.player_3,
                         3: self.player_4}

        self.chosen_player = 0
        self.active = 1  # active or passive turn
        self.team_health = self.get_team_health()

        self.left_bullets = 3
        self.left_grenades = 1

        self.team_health_bar = pygame.rect.Rect(vect(10, 10), vect(100, 10))

    def update(self):

        if self.players[self.chosen_player].dead == 1:
            self.switch_character()

        for i in range(0, 4):
            self.players[i].update()
            self.players[i].draw_health()

        if self.active == 1:
            self.players[self.chosen_player].move()

        self.get_team_health()
        self.draw_team_health()

    def switch_character(self):
        for i in range(0, 4):
            self.players[i].vel = vect(0, 0)
            self.players[i].acc = vect(0, 0)

        self.chosen_player = (self.chosen_player + 1) % 4
        while self.players[self.chosen_player].dead == 1:
            self.chosen_player = (self.chosen_player+1)%4

    def switch_character_type(self, character, action):
        character_types = ["sorcerer", "warlock", "wizard", "witch"]

        a = character_types.index(character)

        if action == "forward":
            a = (a + 1) % 4
        else:
            a = (a - 1) % 4

        for e in range(0, 4):
            self.players[e].character = character_types[a]
            self.players[e].faces = textures.get_faces(self.players[e].character)
            self.players[e].image = self.players[e].faces[self.players[e].facing]

    def change_character_type(self, character):
        character_types = ["sorcerer", "warlock", "wizard", "witch"]

        a = character_types.index(character)

        for e in range(0, 4):
            self.players[e].character = character_types[a]
            self.players[e].faces = textures.get_faces(self.players[e].character)
            self.players[e].image = self.players[e].faces[self.players[e].facing]

    def get_team_health(self):
        self.team_health = 0
        for i in range(0, 4):
            if self.players[i].health >= 0:
                self.team_health += self.players[i].health
        return self.team_health

    def draw_team_health(self):
        col = textures.get_team_color(self.players[0].character)
        if self.team_number == 1:
            pos = 30
        else:
            pos = WIDTH - 230
        width = self.get_team_health()/400
        self.team_health_bar = pygame.rect.Rect(vect(pos, 30), vect(width * 200, 20))
        pygame.draw.rect(self.game.screen, col, self.team_health_bar)
        message = self.team_name + ": " + str(self.get_team_health()) + "/400"
        self.game.screen.blit(FONT_PLAYERS.render(message, 1, col), vect(pos, 30 + 20 + 10))





