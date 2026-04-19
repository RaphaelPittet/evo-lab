import random

import numpy as np

from creature import Creature
from neural_network import NeuralNetwork


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

        new_creature = Creature(neural_network=crossover_netrwork(parent_1.neural_network, parent_2.neural_network, mutation_rate, mutation_min, mutation_max))
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

def crossover_netrwork(parent_1_neural_network, parent_2_neural_network, mutation_rate, mutation_min, mutation_max):
    weights_1 = np.where(np.random.rand(*parent_1_neural_network.weights_1.shape) < 0.5, parent_1_neural_network.weights_1, parent_2_neural_network.weights_1)
    weights_2 = np.where(np.random.rand(*parent_1_neural_network.weights_2.shape) < 0.5, parent_1_neural_network.weights_2, parent_2_neural_network.weights_2)

    # mutation
    mask = np.random.rand(*weights_1.shape) < mutation_rate
    noise = np.random.uniform(mutation_min, mutation_max, weights_1.shape)
    weights_1 = weights_1 + np.where(mask, noise, 0)

    mask = np.random.rand(*weights_2.shape) < mutation_rate
    noise = np.random.uniform(mutation_min, mutation_max, weights_2.shape)
    weights_2 = weights_2 + np.where(mask, noise, 0)

    new_neural_network = NeuralNetwork(weights_1=weights_1, weights_2=weights_2)

    return new_neural_network