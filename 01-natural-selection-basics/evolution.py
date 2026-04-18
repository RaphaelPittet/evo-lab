import random

from creature import Creature


def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    creature_list.sort(key=lambda c: c.fitness, reverse=True)
    best = creature_list[:5]  # top 5
    new_generation = []
    for creature in best:
        for _ in range(4):# 4 copies
            new_creature = Creature(
                speed=creature.speed + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.speed,
                vision_range=creature.vision_range + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.vision_range,
                food_attraction=creature.food_attraction + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.food_attraction,
                poison_fear=creature.poison_fear + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.poison_fear
            )
            new_generation.append(new_creature)
    return new_generation
