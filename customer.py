import enum

import pygame
from gameObject import GameObject
from orderlist import Orderlist
from ingredient import Ingredient
import random
import math

class state(enum.Enum):
    idle = 1 
    patrol = 2
    pursuit = 3
    

class Customer(GameObject):

    distance_threshold = 500
    FOV_threshold = 0.01

    def __init__(self, x, y, image, name, hp):
        super().__init__(x, y, image)
        self.image = pygame.transform.scale(image, (70, 200)) 
        self.state = state.idle
        self.name = name
        self.hp = hp
        self.order = None
        self.MAX_SPEED -= 2
        self.target = None
        self.radians = 0
        self.forward = pygame.math.Vector2(math.cos(self.radians), -math.sin(self.radians))
        self.given = False
        self.orderList = None

    def update(self, game_width, game_height):
        if self.velocity.length() > 0.1:
            self.forward = self.velocity.normalize()
        if self.state == state.idle:
            self.idle()
        elif self.state == state.patrol:
            self.patrol()
        elif self.state == state.pursuit:
            self.pursuit()

        super().update(game_width, game_height)


    def give_order(self, orderLists):
        if self.given == False:
            self.given = True
            new_order = Orderlist(0, 0, self.name)

            new_order.load_orders("SciBurgers/orders.json")
            self.order = new_order.order
            self.orderList = new_order
            orderLists.append(new_order)
            #self.print_order(new_order.order)

    def print_order(self, order):
        print("my order: ")
        for i, ingredient in enumerate(order):
            print(f"{i}, {ingredient}")
        


    def take_order(self, other, player, ingredients, orderLists):
        if self.hitbox.colliderect(other.hitbox) and self.order is not None:
            if isinstance(other, Ingredient) and other.carrying == False:

                stack = other.ingredient_stack

                if len(stack) < 2: return -1

                ingredients.remove(other)
                if self.orderList in orderLists: orderLists.remove(self.orderList)

                if stack != self.order: 
                    #print("invalid!")
                    self.state = state.patrol
                    self.target = player
                    if player.current_ingredient is other:
                        player.current_ingredient = None

                    return 1
                #print("valid order!")
                return 0
        



    def ascend(self, customers, score):
        if self.hp <= 0:
            score += 5
        else:
            score += 30
        if self in customers:
            customers.remove(self)


    def idle(self):
        self.velocity = pygame.Vector2(0,0)

    def patrol(self):
        if self.target is None: return

        distance = (self.target.position - self.position).length()

        if distance < self.distance_threshold and self.forward.dot((self.target.position - self.position).normalize()) > self.FOV_threshold:
                self.state = state.pursuit
                return
        if random.randint(0, 100) <= 1:
            self.dx = random.randint(-2, 2)
            self.dy = random.randint(-2, 2)
            self.velocity += pygame.math.Vector2(self.dx, self.dy) * 0.25



    def pursuit(self):
        to_target = (self.target.position - self.position)
        distance = to_target.length()

        if distance > self.distance_threshold:
            self.state = state.patrol
            return

        self.velocity += to_target.normalize() * 0.5
