import os
import pygame
import random
import matplotlib.pyplot as plt

import evolution
from creature import Creature

print("=== Neural Network Evolution Simulation ===")
sim_name = input("Simulation name: ").strip() or "unnamed"
sim_notes = input("Notes (optional): ").strip()

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(f"Neural Network — {sim_name}")
clock = pygame.time.Clock()

running = True
creatureList = [Creature() for _ in range(20)]
foodList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10)]
poisonList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(20)]
dead_creature = []
speed_multiplier = 1
fitness_history = []
last_avg_fitness = 0

font = pygame.font.SysFont("Arial", 24)
font_small = pygame.font.SysFont("Arial", 18)
generation = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed_multiplier = 10 if speed_multiplier != 10 else 1
            if event.key == pygame.K_UP:
                speed_multiplier += speed_multiplier
            if event.key == pygame.K_DOWN:
                speed_multiplier = max(1, speed_multiplier // 2)

    screen.fill((30, 30, 30))
    text = font.render(f"Gen: {generation}  |  Speed: x{speed_multiplier}  |  Last avg fitness: {last_avg_fitness:.0f}", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    if sim_notes:
        screen.blit(font_small.render(sim_notes, True, (180, 180, 180)), (10, 38))

    for _ in range(speed_multiplier):
        if random.random() < 0.01:
            foodList.append([random.uniform(0, 800), random.uniform(0, 600)])
        if random.random() < 0.01:
            poisonList.append([random.uniform(0, 800), random.uniform(0, 600)])

        for food in foodList:
            pygame.draw.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 1)
        for poison in poisonList:
            pygame.draw.circle(screen, (255, 0, 0), (int(poison[0]), int(poison[1])), 1)

        for creature in creatureList:
            creature.think(foodList, poisonList)
            creature.move()
            creature.draw(screen)

        dead_creature += [c for c in creatureList if c.energy <= 0]
        creatureList = [c for c in creatureList if c.energy > 0]

        if len(creatureList) == 0:
            last_avg_fitness = sum(c.fitness for c in dead_creature) / len(dead_creature)
            fitness_history.append(last_avg_fitness)
            creatureList = evolution.new_generation(dead_creature)
            foodList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(10)]
            poisonList = [[random.uniform(0, 800), random.uniform(0, 600)] for _ in range(20)]
            dead_creature = []
            generation += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

if fitness_history:
    title = f"{sim_name} ({generation - 1} generations)"
    if sim_notes:
        title += f"\n{sim_notes}"

    plt.figure(figsize=(10, 5))
    plt.plot(fitness_history)
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Avg fitness (frames survived)")
    plt.tight_layout()

    attempts_dir = os.path.join(os.path.dirname(__file__), "docs", "attempts")
    os.makedirs(attempts_dir, exist_ok=True)
    existing = [f for f in os.listdir(attempts_dir) if f.endswith(".png")]
    next_num = len(existing) + 1
    filepath = os.path.join(attempts_dir, f"{next_num:03d}_{sim_name.replace(' ', '_')}.png")

    plt.savefig(filepath)
    print(f"\nPlot saved: {filepath}")
    plt.show()