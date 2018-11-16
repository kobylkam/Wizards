import pygame
import textures
from pygame.math import Vector2 as vect
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(pos, size)
        self.rect.x = pos.x
        self.rect.y = pos.y


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = textures.get_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos.x
        self.rect.y = pos.y


class Grave(pygame.sprite.Sprite):
    def __init__(self, game, player):
        self.game = game
        self.group = self.game.map.objects
        pygame.sprite.Sprite.__init__(self, self.group)
        self.image = pygame.transform.scale(textures.get_image("textures/grave.png"), (60, 60))
        self.player = player
        self.rect = self.image.get_rect()
        self.pos = vect(self.player.rect.center)
        self.rect.center = self.player.rect.center - vect(0, -5)


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = self.camera.centerx
        self.y = self.camera.centery

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = 0
        self.camera = pygame.Rect(x, y, self.width, self.height)
        self.x = self.camera.x
        self.y = self.camera.y



