import pygame
import os
import sys
from settings import *
from pygame.math import Vector2 as vect
import copy

_image_library = {}


def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image


def get_faces(character):
        faces = {}

        texturespath = "textures/"
        leftface = "/l"
        rightface = "/r"
        extension = ".png"

        face_r = get_image(texturespath + character + rightface + extension)
        face_l = get_image(texturespath + character + leftface + extension)

        faces[1] = pygame.transform.scale(face_r, (60, 60))
        faces[-1] = pygame.transform.scale(face_l, (60,60))
        return faces


def get_character(character):

    texturespath = "textures/"
    rightface = "/r"
    extension = ".png"

    return pygame.transform.scale(get_image(texturespath + character + rightface + extension), (135,180))


def get_team_color(character):
        if character == "wizard":
                col = BLUE
        elif character == "sorcerer":
                col = LIGHTBLUE
        elif character == "witch":
                col = GREEN
        else:
                col = RED
        return col


def text_to_button(game, message, buttonx, buttony, buttonwidth, buttonheight, font, active_col, inactive_col, action = None):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if buttonx + buttonwidth > cur[0] > buttonx and buttony + buttonheight > cur[1] > buttony:
                col = active_col
                if click[0] == 1 and action != None:
                        if action == "play":
                                game.new()
                        elif action == "options":
                                game.options_screen()
                        elif action == "instructions":
                                game.instructions_screen()
                        elif action == "back":
                                game.show_start_screen()
                        elif action == "quit":
                                sys.exit(0)
        else:
                col = inactive_col

        text_surf = font.render(message, 1, col)
        text_rect = text_surf.get_rect()
        text_rect.center = vect(buttonx + (buttonwidth/2), buttony + (buttonheight/2))
        game.screen.blit(text_surf, text_rect)


def switch_character_type_button(game, team_id, buttonx, buttony, buttonwidth, buttonheight, action):
    cur = pygame.mouse.get_pos()

    if buttonx + buttonwidth > cur[0] > buttonx and buttony + buttonheight > cur[1] > buttony:
            game.teams[team_id].switch_character_type(game.teams[team_id].player_1.character, action)


def switch_language_button(game, buttonx, buttony, buttonwidth, buttonheight):
    cur = pygame.mouse.get_pos()

    if buttonx + buttonwidth > cur[0] > buttonx and buttony + buttonheight > cur[1] > buttony:
            game.switch_language()


def switch_sound_button(game, buttonx, buttony, buttonwidth, buttonheight):
    cur = pygame.mouse.get_pos()

    if buttonx + buttonwidth > cur[0] > buttonx and buttony + buttonheight > cur[1] > buttony:
            game.switch_sound()
    if game.sound == 1:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()


def save_button(game, buttonx, buttony, buttonwidth, buttonheight):
    cur = pygame.mouse.get_pos()

    if buttonx + buttonwidth > cur[0] > buttonx and buttony + buttonheight > cur[1] > buttony:
            game.save_settings()


class Input_box:
    def __init__(self, x, y, width, height, text, font):
        self.box = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('darkgrey')
        self.text = text
        self.txt_surface = font.render(self.text, True, self.color)
        self.active = False
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.box.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('white') if self.active else pygame.Color('darkgrey')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = pygame.Color('white') if self.active else pygame.Color('darkgrey')
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) <= 15:
                    self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.box.x+10, self.box.y+10))
        pygame.draw.rect(screen, self.color, self.box, 2)