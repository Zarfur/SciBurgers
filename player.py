import math
import pygame
from gameObject import GameObject
from ingredient import Ingredient
from customer import Customer, state

class Player(GameObject):

    def __init__(self, x, y, image, speed):
        super().__init__(x,y,image)
        self.current_ingredient = None
        self.speed = speed
        self.hp = 100

    def inputs(self, keys):

        if keys[pygame.K_a]: self.velocity.x -= self.speed
        if keys[pygame.K_d]: self.velocity.x += self.speed
        if keys[pygame.K_w]: self.velocity.y -= self.speed
        if keys[pygame.K_s]: self.velocity.y += self.speed
        if keys[pygame.K_SPACE]: self.throw()

    def check_collision(self, other):
        if self.hitbox.colliderect(other.hitbox):
            if other is Customer:
                if other.state == state.idle: return True
                else:
                    self.hp -= 1
                    return False

            if self.current_ingredient is not None and not isinstance(other, Ingredient): return False
            
            self.pick_up(other)
            return False


    def pick_up(self, ingredient):
        if self.current_ingredient is None and isinstance(ingredient, Ingredient):
            self.current_ingredient = ingredient
            ingredient.carry(self)
            ingredient.carrying = True
    
    def throw(self):
        if self.current_ingredient is not None:
            self.current_ingredient.carrying = False
            self.current_ingredient.throw(self)
            self.current_ingredient = None