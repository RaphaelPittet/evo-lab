# Creature — same simulation logic as exp 03
# Uses a Genome instead of a NeuralNetwork.
# The genome (network topology + weights) is the creature's DNA —
# it controls how the creature reacts to food and poison in its environment.

import random
import numpy as np
import pygame
from genome import Genome


class Creature:
    # Two construction modes:
    #   Generation 1: Creature(innovation_tracker=tracker)
    #     → creates a new random Genome internally
    #   Crossover child: Creature(genome=child_genome)
    #     → uses an already-built Genome from evolution.py
    def __init__(self, genome=None, pos_x=None, pos_y=None, innovation_tracker=None):
        self.energy = 100
        self.fitness = 0
        self.speed = 1
        self.vision_range = 150
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)

        if genome is None and innovation_tracker is None:
            raise ValueError("innovation_tracker required to create a new Creature")

        self.innovation_tracker = innovation_tracker

        if genome is None:
            self.genome = Genome(innovation_tracker=innovation_tracker)
        else:
            self.genome = genome

        if pos_x is None:
            self.pos_x = random.uniform(0, 800)
        else:
            self.pos_x = pos_x

        if pos_y is None:
            self.pos_y = random.uniform(0, 600)
        else:
            self.pos_y = pos_y

    def move(self):
        # Normalize direction to unit vector so speed has consistent meaning
        longueur = np.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        self.direction_x = self.direction_x / longueur if longueur > 0 else 0
        self.direction_y = self.direction_y / longueur if longueur > 0 else 0

        self.pos_x = self.pos_x + self.direction_x * self.speed
        self.pos_y = self.pos_y + self.direction_y * self.speed

        # Bounce off walls
        if self.pos_x > 800:
            self.pos_x = 800
            self.direction_x *= -1
        if self.pos_x < 0:
            self.pos_x = 0
            self.direction_x *= -1
        if self.pos_y > 600:
            self.pos_y = 600
            self.direction_y *= -1
        if self.pos_y < 0:
            self.pos_y = 0
            self.direction_y *= -1

        self.energy -= self.speed * 0.1
        self.fitness += 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos_x), int(self.pos_y)), 5)

    def detect_food(self, food_list):
        # Find nearest food within vision_range, return normalized direction toward it.
        # Returns [0, 0] if nothing visible.
        # Eats food (restores energy) if close enough.
        nearest_food = None
        nearest_dist = self.vision_range

        for food in food_list:
            dist = np.sqrt((food[0] - self.pos_x) ** 2 + (food[1] - self.pos_y) ** 2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_food = food

        if nearest_food is not None:
            direction_x = (nearest_food[0] - self.pos_x) / nearest_dist
            direction_y = (nearest_food[1] - self.pos_y) / nearest_dist
            if nearest_dist < 8:
                self.energy += 5
                self.fitness += 100
                food_list.remove(nearest_food)
            return [direction_x, direction_y]

        return [0, 0]

    def detect_poison(self, poison_list):
        # Find nearest poison within vision_range, return normalized direction away from it.
        # Returns [0, 0] if nothing visible.
        # Takes damage if too close.
        nearest_poison = None
        nearest_dist = self.vision_range

        for poison in poison_list:
            dist = np.sqrt((poison[0] - self.pos_x) ** 2 + (poison[1] - self.pos_y) ** 2)
            if dist < nearest_dist:
                nearest_poison = poison
                nearest_dist = dist

        if nearest_poison is not None:
            direction_x = -(nearest_poison[0] - self.pos_x) / nearest_dist
            direction_y = -(nearest_poison[1] - self.pos_y) / nearest_dist
            if nearest_dist < 8:
                self.energy -= 5
                self.fitness -= 50
                poison_list.remove(nearest_poison)
            return [direction_x, direction_y]

        return [0, 0]

    def think(self, food_list, poison_list):
        # Sense the environment, feed inputs into the genome's network, update direction.
        food_direction = self.detect_food(food_list)
        poison_direction = self.detect_poison(poison_list)
        inputs = food_direction + poison_direction

        # Nothing visible — keep current direction (exploration)
        if inputs == [0, 0, 0, 0]:
            return

        outputs = self.genome.forward_pass(inputs)

        # Ignore near-zero output to avoid freezing on a dead network
        if abs(outputs[0]) > 0.01 or abs(outputs[1]) > 0.01:
            self.direction_x = outputs[0]
            self.direction_y = outputs[1]