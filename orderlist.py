import pygame
import json

class Orderlist:

    def __init__(self, x, y, customer):
        self.x = x
        self.y = y
        self.customer = customer


    def load_orders(self, filename):

        with open(filename, 'r') as file:
            data = json.load(file)
            self.order = None
            for order in data['orders']:
                if order['customer'] == self.customer:
                    self.order = order['order']
                    break

    def draw(self, screen, font):
        return