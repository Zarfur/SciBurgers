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
    # images...
    player_image = pygame.transform.scale(player_image, (70, 100)) 



    # init stuff

    player = Player(GAME_WIDTH/2, GAME_HEIGHT/2, player_image, 0.5)
    camera = Camera(GAME_WIDTH/2, GAME_HEIGHT/2, WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT)

    ingredients = [Ingredient(50, 50, type.osu), Ingredient(200, 600, type.osu)]

    all_objects = [player] + ingredients


    # update 
    def update(objects, camera):
        camera.update(player)
        for obj in objects: obj.update(GAME_WIDTH, GAME_HEIGHT)


    # draw
    def draw_stuff(objects, camera):
        screen.fill((0, 0, 0))
        for obj in objects: obj.draw(screen, camera)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
        keys = pygame.key.get_pressed()

        player.inputs(keys)
        update(all_objects, camera)
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

        draw_stuff(all_objects, camera)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())