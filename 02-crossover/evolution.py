import random

from creature import Creature


def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    creature_list.sort(key=lambda c: c.fitness, reverse=True)
    best = creature_list[:5]  # top 5
    new_generation = []

    # Crossover and mutation
    total_fitness = sum(c.fitness for c in best)
    for _ in range(20):
        # getting parent
        parent_1 = select_parent(best, total_fitness)
        parent_2 = select_parent([c for c in best if c != parent_1], total_fitness-parent_1.fitness)

        new_creature = Creature(
            speed=crossover_gene(parent_1.speed, parent_2.speed, mutation_rate, mutation_min, mutation_max),
            vision_range= crossover_gene(parent_1.vision_range, parent_2.vision_range, mutation_rate, mutation_min, mutation_max),
            food_attraction= crossover_gene(parent_1.food_attraction, parent_2.food_attraction, mutation_rate, mutation_min, mutation_max),
            poison_fear= crossover_gene(parent_1.poison_fear, parent_2.poison_fear, mutation_rate, mutation_min, mutation_max)
        )
        new_generation.append(new_creature)
    return new_generation

def select_parent(creature, total_fitness):
    pick = random.uniform(0, total_fitness)
    current = 0
    for c in creature:
        current += c.fitness
        if current > pick:
            return c
    return creature[-1]

def crossover_gene(gene_parent_1, gene_parent_2, mutation_rate, mutation_min, mutation_max):
    gene = gene_parent_1 if random.random() < 0.5 else gene_parent_2
    gene = gene + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else gene
    return gene