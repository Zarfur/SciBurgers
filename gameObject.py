import math
import random

import pygame

class GameObject:

    DRAG = 0.9
    MAX_SPEED = 18
    GRAVITY = 0.5

    def __init__(self, x, y, image):
        self.image = image
        self.image_right = image
        self.image_left = pygame.transform.flip(image, True, False)
        self.facing_right = True 
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.hitbox = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())


    def draw(self, screen, camera, none):
        screen.blit(self.image, camera.apply(self.position))
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def update(self,game_width, game_height):

        if self.velocity.length() > self.MAX_SPEED:
            self.velocity.scale_to_length(self.MAX_SPEED)

        if self.velocity.length() > 0.1:
            self.forward = self.velocity.normalize()

        self.position += self.velocity
        self.velocity *= self.DRAG

        if self.velocity.x > 0.1:  self.facing_right = True
        elif self.velocity.x < -0.1: self.facing_right = False

        if self.facing_right: self.image = self.image_right
        else: self.image = self.image_left

        self.position.x = max(0, min(self.position.x, game_width - self.hitbox.width))
        self.position.y = max(0, min(self.position.y, game_height - self.hitbox.height))

        self.hitbox.x = self.position.x
        self.hitbox.y = self.position.y

    def take_damage(self):
        x = random.randint(-4, 4) 
        y = random.randint(-12, -8) 
        self.velocity += pygame.Vector2(x, y)
        
