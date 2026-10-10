import enum

import pygame
from gameObject import GameObject

class type(enum.Enum):
    bun = "BUN"
    ketchup = "KETCHUP"
    mustard = "MUSTARD"
    patty = "PATTY"
    cheese = "CHEESE"
    lettuce = "LETTUCE"
    onion = "ONION"
    osu = "OSU"


class Ingredient(GameObject):

    THROW_SPEED = 3
    THROW_UP = -5
    y_offset = pygame.Vector2(0, -10)
    
    def __init__(self, x, y, type):
        super().__init__(x, y, self.get_ingredient_image(type))
        self.ingredient_stack = [type]
        self.carrying = False
        self.parent = None
        self.inAir = False
        self.defaultY = self.position.y 

    def add_ingredient(self, type):
        self.ingredient_stack.append(type)


    def draw(self, screen, camera):
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        for i, ingredient in enumerate(self.ingredient_stack):
            ingredient_image = self.get_ingredient_image(ingredient)
            draw_y  = self.position.y - (i+1) * ingredient_image.get_height()

            screen.blit(ingredient_image, camera.apply(pygame.Vector2(self.position.x, draw_y)))

    def get_ingredient_image(self, ingredient_type):
        image_path = f"SciBurgers/{ingredient_type.value}.png"
        image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (70, 50))

        return image

    def collide(self, other):
        # just add enemy hit to this collide 
        if not isinstance(other, Ingredient) or self.carrying or other.carrying: return False
        if self.hitbox.colliderect(other.hitbox):
            self.ingredient_stack.extend(other.ingredient_stack)
            self.update_hitbox() 
            return True

    def carry(self, player):
        self.parent = player
        self.carrying = True
        self.inAir = False

    def throw(self, player):
        self.carrying = False
        self.parent = None
        self.inAir = True
        self.defaultY = player.position.y + player.image.get_height()
        throw_velocity = pygame.Vector2(player.velocity.x, 0)
        self.velocity = throw_velocity * self.THROW_SPEED + pygame.Vector2(0, self.THROW_UP)

    def update_hitbox(self):
        self.hitbox.width = self.image.get_width()
        self.hitbox.height = len(self.ingredient_stack) * self.image.get_height()

        self.hitbox.x = self.position.x
        self.hitbox.y = self.position.y - len(self.ingredient_stack) * self.image.get_height()

    def update(self, game_width, game_height):
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

