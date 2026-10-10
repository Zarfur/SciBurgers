import pygame
from gameObject import GameObject
class Enemy(GameObject):

    distance_threshold = 200
    FOV_threshold = 90
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    