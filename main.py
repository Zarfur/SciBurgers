import random
import math
import pygame
import asyncio 
from player import Player
from ingredient import Ingredient
from camera import Camera
from ingredient import ingType
from customer import Customer,state

async def main():

    GAME_WIDTH = 2600
    GAME_HEIGHT = 1800
    WIDTH = 800
    HEIGHT = 600


    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SciBurger's Burgeria")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 24)
    score_txt = "Points: 0"

    player_image = pygame.image.load("Sciburgers/SciBee.png").convert_alpha()
    background_image = pygame.image.load("Sciburgers/BronxScience.png").convert_alpha()

    player_image = pygame.transform.scale(player_image, (70, 100)) 


    player = Player(50,  50, player_image, 1.7)
    camera = Camera(GAME_WIDTH/2, GAME_HEIGHT/2, WIDTH, HEIGHT, GAME_WIDTH, GAME_HEIGHT)


    def get_image(customer):
        image_path = f"SciBurgers/{customer}.png"
        image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (100, 50))
        return image
    
    def generate_objects(list, runtime_objs):
        for i in list:
            x = random.randint(0, GAME_WIDTH)
            y = random.randint(0, GAME_HEIGHT)
            if isinstance(i, str):
                runtime_objs.append(Customer(x, y, get_image(i), i, 100))
            else:
                runtime_objs.append(Ingredient(x, y, i))

    
    possible_customers = ["Ennio", "Stephanie", "Joseph", "Alex", "Ethan", "Sunay", "Henry", "Ankit"]
    possible_ingredients = [ingType.bun, ingType.cheese, ingType.ketchup, ingType.lettuce, ingType.mustard, ingType.onion, ingType.osu, ingType.patty, ingType.bun]

    customers = []
    ingredients = []
    all_objects = [player]
    orderlists = []

    score = 0
    

    # update 
    def update(objects, camera):
        nonlocal score_txt, score
        score_txt = f"Points: {score}"
        #if len(customers) <= 0: generate_objects(possible_customers, customers)
        if len(ingredients) <= 1: generate_objects(possible_ingredients, ingredients)

        camera.update(player)
        for obj in objects: obj.update(GAME_WIDTH, GAME_HEIGHT)

        i = 0
        while i < len(ingredients):
            player.check_collision(ingredients[i])
            j = i + 1
            while j < len(ingredients):
                if ingredients[i].collide(ingredients[j]):
                    ingredients.remove(ingredients[j])   
                else: j += 1
            i += 1

        for customer in customers[:]:                    
            if player.check_collision(customer):
                customer.give_order(orderlists)
                if customer.state != state.idle:
                    score -= 1
            if customer.hp <= 0:
                customer.ascend(customers)

        for customer in customers[:]:
            for ingredient in ingredients[:]:
                if customer.take_order(ingredient, player, ingredients, orderlists):
                    customer.ascend(customers)


    # draw
    def draw_stuff(objects, camera):

        screen.fill((0, 0, 0))

        text_surface = font.render(score_txt, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(40, HEIGHT - 30))


        screen.blit(background_image, (0, 0))
        screen.blit(text_surface, text_rect)
        for obj in objects: obj.draw(screen, camera)

        for i, order in enumerate(orderlists):
            order.draw(screen, 10 + i * 200, 10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
        keys = pygame.key.get_pressed()

        player.inputs(keys)
        all_objects = [player] + ingredients + customers
        update(all_objects, camera)
        all_objects = [player] + ingredients + customers

        draw_stuff(all_objects, camera)
        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())