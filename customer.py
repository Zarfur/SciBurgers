import enum

import pygame
from gameObject import GameObject

class state(enum.Enum):
    idle = 1 
    waiting = 2 
    # 
    patrol = 3 
    pursuit = 4 



class Customer(GameObject):

    distance_threshold = 200
    FOV_threshold = 90

    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.state = state.idle


    def update(self):
        if self.state == state.idle:
            self.idle()
        elif self.state == state.waiting:
            self.waiting()
        elif self.state == state.patrol:
            self.patrol()
        elif self.state == state.pursuit:
            self.pursuit()

    def give_order(self, other):
        return

    def take_order(self, other):
        return

    def ascend(self, customers):
        customers.remove(self)

    def idle():
        return

    def waiting():
        return

    def patrol():
        return

    def pursuit():
        return

    