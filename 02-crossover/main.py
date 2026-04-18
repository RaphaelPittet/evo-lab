import pygame
import random
import matplotlib.pyplot as plt

import evolution
from creature import Creature

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()

running = True
creatureList = [Creature() for _ in range(20)]
foodList = [ [random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10) ]
poisonList = [ [random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10) ]
dead_creature = []
speed_multiplier = 1
fitness_history = []

# define font
font = pygame.font.SysFont("Arial", 24)
generation = 1

while running:
    for event in pygame.event.get():
        # close and display fitness history graph
        if event.type == pygame.QUIT:
            running = False
            plt.plot(fitness_history)
            plt.title("Average fitness per generation")
            plt.xlabel("Generation")
            plt.ylabel("Avg fitness (frames survived)")
            plt.show()
        # change simulation speed detection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed_multiplier = 10 if speed_multiplier != 10 else 1
            if event.key == pygame.K_UP:
                speed_multiplier += speed_multiplier
            if event.key == pygame.K_DOWN:
                speed_multiplier = speed_multiplier - speed_multiplier if speed_multiplier - speed_multiplier > 0 else 1

    screen.fill((30, 30, 30))
    text = font.render(f"Generation: {generation}  |  Speed: x{speed_multiplier}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    for _ in range(speed_multiplier):
        if random.random() < 0.01:  # 1% de chance par frame
            foodList.append([random.uniform(0, 800), random.uniform(0, 600)])
        if random.random() < 0.005:
            poisonList.append([random.uniform(0, 800), random.uniform(0, 600)])
        for food in foodList:
            pygame.draw.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 1)
        for poison in poisonList:
            pygame.draw.circle(screen, (255, 0, 0), (int(poison[0]), int(poison[1])), 1)
        for creature in creatureList:
            creature.detect_food(foodList)
            creature.detect_poison(poisonList)
            creature.move();
            creature.draw(screen)

        dead_creature += [c for c in creatureList if c.energy <= 0]
        creatureList = [c for c in creatureList if c.energy > 0]
        if len(creatureList) == 0:
            creatureList = evolution.new_generation(dead_creature)
            foodList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10)]
            poisonList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10)]
            fitness_history.append(sum(c.fitness for c in dead_creature) / len(dead_creature))
            dead_creature = []
            generation += 1


    pygame.display.flip()
    clock.tick(60)

pygame.quit()