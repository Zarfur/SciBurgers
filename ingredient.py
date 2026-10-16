import enum

import pygame
from gameObject import GameObject

class ingType(enum.Enum):
    bun = ("BUN", 1, 1)
    patty = ("PATTY", 20, 2)
    cheese = ("CHEESE", 10, 1)
    onion = ("ONION", 20, 3)
    lettuce = ("LETTUCE", 15, 1)
    ketchup = ("KETCHUP", 10, 1)
    mustard = ("MUSTARD", 15, 2)
    osu = ("OSU", 15, 3)

    def __init__(self, label, offset, damage):
        self.label = label
        self.offset = offset
        self.damage = damage


class Ingredient(GameObject):

    THROW_SPEED = 3
    THROW_UP = -5
    y_offset = pygame.Vector2(0, -10)
    
    def __init__(self, x, y, img, ingType):
        super().__init__(x, y, img)
        self.ingredient_stack = [ingType]
        self.carrying = False
        self.parent = None
        self.inAir = False
        self.defaultY = self.position.y 
        self.damage = 0

    def draw(self, screen, camera, images):
        height = 0
        for ingredient in self.ingredient_stack:
            ingredient_image = images[ingredient]
            draw_y = self.position.y - height - ingredient_image.get_height()
            screen.blit(ingredient_image, camera.apply(pygame.Vector2(self.position.x, draw_y)))
            height += ingredient.offset


    def collide(self, other):
        if not isinstance(other, Ingredient) or self.carrying or other.carrying: return False
        if self.hitbox.colliderect(other.hitbox):
            self.ingredient_stack.extend(other.ingredient_stack)
            #self.print_ingredients()
            self.update_hitbox() 
            return True
        return False

    def carry(self, player):
        self.parent = player
        self.carrying = True
        self.inAir = False

    def throw(self, player):
        self.carrying = False
        self.parent = None
        self.inAir = True
        self.defaultY = player.position.y + player.image.get_height()
        throw_velocity = pygame.Vector2(player.velocity.x * 0.75, 0)
        self.velocity = throw_velocity * self.THROW_SPEED + pygame.Vector2(0, self.THROW_UP)
    
    def update_hitbox(self):
        height = sum(i.offset for i in self.ingredient_stack)  
        self.hitbox.width = self.image.get_width()
        self.hitbox.height = height
        self.hitbox.x = self.position.x
        self.hitbox.y = self.position.y - height


    def update(self, game_width, game_height):
        self.damage = sum(i.damage for i in self.ingredient_stack)
        if self.carrying:
            self.position = self.parent.position - self.y_offset
            self.velocity = pygame.Vector2(0, 0)

        elif self.inAir:
            self.velocity.y += self.GRAVITY
            self.position += self.velocity
            if self.position.y >= self.defaultY:
                self.position.y = self.defaultY
                self.velocity = pygame.Vector2(0, 0)
                self.inAir = False

        self.position.x = max(0, min(self.position.x, game_width - self.hitbox.width))
        self.position.y = max(0, min(self.position.y, game_height))

        self.update_hitbox()

    def print_ingredients(self):
        print("-------------")
        for i, ingredient in enumerate(self.ingredient_stack):
            print(f"{i}: {ingredient}")

