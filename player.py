import math
import pygame
from gameObject import GameObject
from ingredient import Ingredient

class Player(GameObject):
    TURN_SPEED = 6

    def __init__(self, x, y, image, speed):
        super().__init__(x,y,image)
        self.current_ingredient = None
        self.speed = speed

    def inputs(self, keys):

        if keys[pygame.K_a]: self.velocity.x -= self.speed
        if keys[pygame.K_d]: self.velocity.x += self.speed
        if keys[pygame.K_w]: self.velocity.y -= self.speed
        if keys[pygame.K_s]: self.velocity.y += self.speed
        if keys[pygame.K_SPACE]: self.throw()

    def check_collision(self, other):
        if self.current_ingredient is not None and other is not Ingredient: return
        elif self.hitbox.colliderect(other.hitbox):
            self.pick_up(other)


    def pick_up(self, ingredient):
        if self.current_ingredient is None:
            self.current_ingredient = ingredient
            ingredient.carry(self)
            ingredient.carrying = True
    
    def throw(self):
        if self.current_ingredient is not None:
            self.current_ingredient.carrying = False
            self.current_ingredient.throw(self)
            self.current_ingredient = None