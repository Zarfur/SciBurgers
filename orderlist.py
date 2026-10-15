import pygame
import json
from ingredient import ingType

class Orderlist:

    
    def __init__(self, x, y, customer):
        self.x = x
        self.y = y
        self.customer = customer
        self.font = pygame.font.SysFont("Arial", 12)
        self.order = []



    def load_orders(self, filename):
        if len(self.order) <= 0:
            with open(filename, 'r') as file:
                data = json.load(file)
                for order in data['orders']:
                    if order['customer'] == self.customer:
                        for i in order['ingredients']:
                            self.order.append(ingType[i])

    def draw(self, screen, x, y):
        height = len(self.order) * 20
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 200, height))
        
        name = self.font.render(self.customer, True, (0, 0, 0))
        screen.blit(name, (x + 5, y))

        for i, ingredient in enumerate(self.order):
            text_surface = self.font.render(f"{i}). {ingredient.name}", True, (0, 0, 0))
            screen.blit(text_surface, (x + 5, y + i * 15 + 15))