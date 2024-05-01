import math
import pygame
import collections
import os
import copy

from luckplusplus import *

class Animations():
    MISSING_TEXTURE = None
    LOADING_AAA_TEXTURE = None
        
    def load_all_animations(self):
        pygame.init()

        bound = min(self.X, self.Y)
        print("Loading all animations and textures.")
        Animations.MISSING_TEXTURE = pygame.Surface.convert(pygame.image.load(os.path.join('assets', 'miss.png')))
        print("MISSING_TEXTURE", Animations.MISSING_TEXTURE)
        Animations.LOADING_AAA_TEXTURE = pygame.Surface.convert(pygame.transform.smoothscale(pygame.image.load(os.path.join('assets', 'aaa.png')), (bound/2.5, bound/2.5)))
        print("LOADING_AAA_TEXTURE", Animations.LOADING_AAA_TEXTURE)
        Animations.DOT_TEXTURE = pygame.Surface.convert_alpha(pygame.transform.smoothscale(pygame.image.load(os.path.join('assets', 'dot.png')), (bound/50, bound/50)))
        print("DOT_TEXTURE", Animations.DOT_TEXTURE)


    def __init__(self, attributes, screen):
        self.screen = screen
        self.animations = []
        self.FPS, self.X, self.Y = attributes

        self.load_all_animations()
        
    def tick(self):
        for animation in self.animations:
            animation_return = animation.tick()
            if animation_return == None:
                animation.active = False
            else:
                self.screen.blit(animation_return[0], animation_return[1])

        animations_length = len(self.animations)
        i = 0
        while i < animations_length:
            if not self.animations[i].active:
                self.animations.pop(i)
                animations_length -= 1
                i -= 1
            i += 1
            
    def enqueue(self, animation):
        self.animations.append(animation)
    
class GenericAnimation():
    def __init__(self, info):
        self.active = True
        self.info = info
        self.time = 0
        self.rot = 0
        self.pos = [0, 0]
        self.scale = [1, 1]
        self.sprite = Animations.MISSING_TEXTURE
        self.target_rot = None
        self.target_scale = None
        self.target_pos = None
        self.target_rot_time = None
        self.target_scale_time = None
        self.target_pos_time = None
        print("Generic Animation Created with Sprite: ", self.sprite, ".")
        
    def adjust_position(self):
        y_distance = self.target_pos[1] - self.pos[1]
        x_distance = self.target_pos[0] - self.pos[0]
        delta_time = self.target_pos_time - self.time
        self.pos[0] += x_distance / delta_time ** 0.7
        self.pos[1] += y_distance / delta_time ** 0.7

    def adjust_scale(self):
        y_distance = self.target_scale[1] - self.scale[1]
        x_distance = self.target_scale[0] - self.scale[0]
        delta_time = self.target_scale_time - self.time
        self.scale[0] += x_distance / delta_time ** 0.7
        self.scale[1] += y_distance / delta_time ** 0.7
        
    def tick(self):
        if self.target_rot == None and self.info.has_next_rotation():
            self.target_rot_time, self.target_rot = self.info.pop_next_rotation()
        if self.target_scale == None and self.info.has_next_scale():
            self.target_scale_time, self.target_scale = self.info.pop_next_scale()
        if self.info.has_next_image() and self.time >= self.info.peek_next_image()[0]:
            self.sprite = self.info.pop_next_image()[1]
        if self.target_pos == None and self.info.has_next_position():
            self.target_pos_time, self.target_pos = self.info.pop_next_position()

        if self.time > self.info.health:
            return None

        computed_surface = copy.copy(self.sprite)
        if not self.target_pos == None:
            if self.time >= self.target_pos_time:
                self.pos[0], self.pos[1] = self.target_pos
                self.target_pos_time = None
                self.target_pos = None
            else:
                self.adjust_position()

        if not self.target_scale == None:
            if self.time >= self.target_scale_time:
                self.scale[0], self.scale[1] = self.target_scale
                self.target_scale_time = None
                self.target_scale = None
            else:
                self.adjust_scale()
        computed_surface = pygame.transform.smoothscale_by(computed_surface, self.scale)
                
        #computed_surface = pygame.Surface.convert(computed_surface)

        self.time += 1
        return (computed_surface, self.pos)
        
class AnimationInfo():
    def __init__(self):
        self._position_sequence = collections.deque()
        self._scale_sequence = collections.deque()
        self._rotation_sequence = collections.deque()
        self.health = 0
        self._image_sequence = collections.deque()

    def scale(self, time, amount):
        self._scale_sequence.append((time, amount))
        return self

    def position(self, time, location):
        self._position_sequence.append((time, location))
        return self

    def rotate(self, time, angle):
        self._rotation_sequence.append((time, angle))
        return self

    def set_health(self, health):
        self.health = health
        return self

    def image(self, time, image):
        self._image_sequence.append((time, image))
        return self

    def pop_next_scale(self):
        return self._scale_sequence.popleft()

    def pop_next_position(self):
        return self._position_sequence.popleft()

    def pop_next_rotation(self):
        return self._rotation_sequence.popleft()

    def pop_next_image(self):
        return self._image_sequence.popleft()

    def has_next_scale(self):
        return len(self._scale_sequence) > 0

    def has_next_position(self):
        return len(self._position_sequence) > 0

    def has_next_rotation(self):
        return len(self._rotation_sequence) > 0

    def has_next_image(self):
        return len(self._image_sequence) > 0

    def peek_next_image(self):
        return self._image_sequence[0]
