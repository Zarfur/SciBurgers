import pygame
import json

class Orderlist:

    
    def __init__(self, x, y, customer):
        self.x = x
        self.y = y
        self.customer = customer
        self.font = pygame.font.SysFont("Arial", 36)



    def load_orders(self, filename):
        if self.order is not None:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.order = None
                for order in data['orders']:
                    if order['customer'] == self.customer:
                        self.order = order['order']
                        break

    def draw(self, screen):
        for i, ingredient in enumerate(self.order):
            text_pos = text_surface.get_rect(center=(self.x, self.y + i * 40))
            text_surface = self.font.render(f"{i}). {ingredient}", True, (255, 255, 255))
            screen.blit(text_surface, text_pos)