import enum

import pygame
from gameObject import GameObject
from orderlist import Orderlist
from ingredient import Ingredient
import random

class state(enum.Enum):
    idle = 1 
    patrol = 2
    pursuit = 3
    

class Customer(GameObject):

    distance_threshold = 200
    FOV_threshold = 90

    def __init__(self, x, y, image, name, hp):
        super().__init__(x, y, image)
        self.state = state.idle
        self.name = name
        self.hp = hp
        self.order = None
        self.MAX_SPEED = self.MAX_SPEED - 2
        self.target = None


    def update(self, ues, les):
        if self.state == state.idle:
            self.idle()
        elif self.state == state.patrol:
            self.patrol()
        elif self.state == state.pursuit:
            self.pursuit()

    def give_order(self, other, orderLists):
        if self.hitbox.colliderect(other.hitbox):
            new_order = Orderlist(0, 0, self.name)
            
            orderLists.append(new_order)
            new_order.load_orders("SciBurgers/orders.json")
            self.order = new_order.order


    def take_order(self, other, player):
        if self.hitbox.colliderect(other.hitbox):
            if not isinstance(other, Ingredient): return False
            stack = other.ingredient_stack
            if len(stack) < 2: return
            if len(stack) != len(self.order): 
                self.state = state.patrol
                self.target = player
                return False
            for i, order_ing in enumerate(self.order):
                if stack[i] != order_ing: 
                    self.state = state.patrol
                    self.target = player
                    return False
            return True
        



    def ascend(self, customers, all_objects):
        all_objects.remove(self)
        customers.remove(self)

    def idle(self):
        self.velocity = pygame.Vector2(0,0)

    def patrol(self):
        self.target = self.target
        distance = (self.target.position - self.position).length()

        if distance < self.distance_threshold and self.forward.dot((self.target.position - self.position).normalize()) > self.FOV_threshold:
                self.state = state.pursuit
        else:
            self.state = state.patrol
            if random.randint(0, 100) <= 1:
                self.dx = random.randint(-2, 2)
                self.dy = random.randint(-2, 2)
                self.velocity += pygame.math.Vector2(self.dx, self.dy) * 0.25



    def pursuit(self):
        to_target = self.target.position - self.position
        if to_target.length() > 0:
            self.velocity += to_target.normalize() * 0.5

        if self.velocity.length() > self.MAX_SPEED:
            self.velocity.scale_to_length(self.MAX_SPEED)

        self.velocity *= self.DRAG
        self.position += self.velocity


    