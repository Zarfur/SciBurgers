import random
import math
import pygame
import asyncio 
from player import Player
from ingredient import Ingredient
from camera import Camera
from orderlist import Orderlist
from ingredient import type
from customer import Customer

async def main():

    GAME_WIDTH = 2600
    GAME_HEIGHT = 1800
    WIDTH = 800
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SciBurger's Burgeria")
    clock = pygame.time.Clock()

    player_image = pygame.image.load("Sciburgers/SciBee.png").convert_alpha()
    background_image = pygame.image.load("Sciburgers/BronxScience.png").convert_alpha()
    # images...
    player_image = pygame.transform.scale(player_image, (70, 100)) 



    # init stuff

    player = Player(50,  50, player_image, 1.7)
    camera = Camera(GAME_WIDTH/2, GAME_HEIGHT/2, WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT)

    # rng ts later
    ingredients = [Ingredient(50, 50, type.osu), Ingredient(100, 100, type.ketchup), Ingredient(160, 160, type.bun),
                   Ingredient(200, 200, type.cheese), Ingredient(300, 300, type.lettuce), Ingredient(400, 400, type.patty)
                   , Ingredient(500, 500, type.bun), Ingredient(600, 600, type.onion), Ingredient(700, 700, type.mustard)]

    customers = [Customer(600, 100, player_image, "Ankit", 100 )]
    

    all_objects = [player] + ingredients + customers

    orderlist = []

    # update 
    def update(objects, camera):
        camera.update(player)
        for obj in objects: obj.update(GAME_WIDTH, GAME_HEIGHT)

        i = 0
        while i < len(ingredients):
            player.check_collision(ingredients[i])
            j = i + 1
            while j < len(ingredients):
                if ingredients[i].collide(ingredients[j]):
                    all_objects.remove(ingredients[j])
                    ingredients.remove(ingredients[j])   
                else: j += 1
            i += 1

        for customer in customers[:]:                    
            if player.check_collision(customer):
                customer.give_order(player, orderlist)

        for customer in customers[:]:
            for ingredient in ingredients[:]:
                if customer.take_order(ingredient, player):
                    ingredients.remove(ingredient)
                    customer.ascend(customers, all_objects)


    # draw
    def draw_stuff(objects, camera):
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        for obj in objects: obj.draw(screen, camera)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
        keys = pygame.key.get_pressed()

        player.inputs(keys)
        update(all_objects, camera)

        draw_stuff(all_objects, camera)
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())