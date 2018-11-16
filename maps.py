import pygame
from settings import *
from pygame.math import Vector2 as vect
import map


class MapForest(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

        # Platforms

        self.platforms = pygame.sprite.Group()
        self.bottomplatform = map.Platform(vect(0, HEIGHT-50), vect(2560,40))
        self.castleplatform1 = map.Platform(vect(3*WIDTH/2 + 5, HEIGHT-225), vect(512,350))
        self.castleplatform2 = map.Platform(vect(200 + 5, HEIGHT-225), vect(512,350))
        self.tree1platform = map.Platform(vect(40, HEIGHT-300), vect(150,50))
        self.tree2platform = map.Platform(vect(2*WIDTH - 160, HEIGHT-300), vect(150,50))
        self.tree3platform = map.Platform(vect(3*WIDTH/2 - 160, HEIGHT-300), vect(150,50))
        self.tree4platform = map.Platform(vect(650, HEIGHT-300), vect(150,50))
        self.shootingtowerplatform1 = map.Platform(vect(330, 300), vect(70,22))
        self.shootingtowerplatform2 = map.Platform(vect(530, 300), vect(70,22))
        self.shootingtowerplatform3 = map.Platform(vect(2050, 300), vect(70,22))
        self.shootingtowerplatform4 = map.Platform(vect(2250, 300), vect(70,22))
        self.platforms.add(self.bottomplatform)
        self.platforms.add(self.castleplatform1)
        self.platforms.add(self.castleplatform2)
        self.platforms.add(self.tree1platform)
        self.platforms.add(self.tree2platform)
        self.platforms.add(self.tree3platform)
        self.platforms.add(self.tree4platform)
        self.platforms.add(self.shootingtowerplatform1)
        self.platforms.add(self.shootingtowerplatform2)
        self.platforms.add(self.shootingtowerplatform3)
        self.platforms.add(self.shootingtowerplatform4)
        self.bottomplatformsprite = pygame.sprite.Group()
        self.bottomplatformsprite.add(self.bottomplatform)

        # Objects

        self.objects = pygame.sprite.Group()
        self.castle1 = map.Object(vect(3*WIDTH /2, 250 ), "textures/castle.png")
        self.castle2 = map.Object(vect(200, 250 ), "textures/castle.png" )
        self.bottom = map.Object(vect(0, HEIGHT-50), "textures/grass.png")
        self.tree1 = map.Object(vect(0, HEIGHT-350), "textures/tree.png")
        self.tree2 = map.Object(vect(2*WIDTH - 200, HEIGHT-350), "textures/tree.png")
        self.tree3 = map.Object(vect(3*WIDTH/2 - 200, HEIGHT-350), "textures/tree.png")
        self.tree4 = map.Object(vect(650, HEIGHT-350), "textures/tree.png")
        self.objects.add(self.bottom)
        self.objects.add(self.castle1)
        self.objects.add(self.castle2)
        self.objects.add(self.tree1)
        self.objects.add(self.tree2)
        self.objects.add(self.tree3)
        self.objects.add(self.tree4)

        self.add(self.platforms)
        self.add(self.objects)



