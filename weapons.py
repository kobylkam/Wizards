import pygame
import worm
import math
import textures
from pygame.math import Vector2 as vect
from settings import *
from os import path


class Wand(pygame.sprite.Sprite):
    def __init__ (self, game, player):
        self.game = game
        self.group = game.bullets
        pygame.sprite.Sprite.__init__(self, self.group)
        self.player = player
        self.image = textures.get_image("textures/weapons/bullet_" + self.player.character + ".png")
        self.pos = vect(self.player.rect.center) + vect(-30, -15)
        self.rect = pygame.rect.Rect(self.pos, (1, 1))
        self.vel = vect(self.player.facing, 0) * BULLET_SPEED
        self.spawn_time = pygame.time.get_ticks()

    def update(self, game):
        self.pos += self.vel
        self.rect.center = self.pos
        if pygame.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()
        if pygame.sprite.spritecollideany(self, self.game.map.platforms):
            self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__ (self, game, player):
        self.game = game
        self.group = game.grenades
        pygame.sprite.Sprite.__init__(self, self.group)
        self.player = player
        self.image = textures.get_image("textures/weapons/tome_" + self.player.character + ".png")
        self.pos = vect(self.player.rect.center) + vect(-30, -15)
        self.rect = pygame.rect.Rect(self.pos, (1, 1))
        dir = pygame.mouse.get_pos()
        rel_x, rel_y = dir[0] - (self.pos.x + game.camera.x), dir[1] - (self.pos.y + game.camera.y)
        rel_n = math.sqrt(rel_x * rel_x + rel_y * rel_y)
        self.vel = vect(rel_x/rel_n, rel_y/rel_n) * GRENADE_SPEED
        self.last_update = 0

        self.explosion = {}
        for i in range(1, 25):
            e = "0" + str(i)
            e = e[-2:] + ".png"
            self.explosion[i] = pygame.transform.scale(textures.get_image(path.join("textures/weapons/explode", e)), (60, 60))
        self.current_frame = 0
        self.last_update = 0
        self.health_bar = pygame.rect.Rect(self.rect.midtop + vect(-30, -10), vect(self.rect.width, 5))



    def update(self, game):
        self.acc = vect(0, PLAYER_GRAVITY/2)

        self.acc.x += self.vel.x * PLAYER_FRICTION/10
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.pos += self.vel
        self.rect.center = self.pos

        hit_bottom = pygame.sprite.spritecollide(self, self.game.map.bottomplatformsprite, False)
        if hit_bottom:
            self.vel = vect(0,0)
            self.pos.y = hit_bottom[0].rect.top
            self.explode()

        if self.pos.y > HEIGHT:
            self.kill()

    def explode(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > 25:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.explosion)
            self.image = self.explosion[self.current_frame]
        if self.current_frame == 23:
            self.kill()

