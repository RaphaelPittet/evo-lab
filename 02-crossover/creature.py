import random

import numpy as np
import pygame


class Creature:
    def __init__(self, speed=None, vision_range=None, food_attraction=None, poison_fear=None, pos_x=None, pos_y=None):
        self.energy = 100
        self.fitness = 0
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)

        if speed is None:
            self.speed = random.uniform(1, 5)
        else:
            self.speed = max(1, min(5, speed))

        if vision_range is None:
            self.vision_range = random.uniform(20, 150)
        else:
            self.vision_range = max(20, min(150, vision_range))

        if food_attraction is None:
            self.food_attraction = random.uniform(0, 1)
        else:
            self.food_attraction = max(0, min(1, food_attraction))

        if poison_fear is None:
            self.poison_fear = random.uniform(0, 1)
        else:
            self.poison_fear = max(0, min(1, poison_fear))

        if pos_x is None:
            self.pos_x = random.uniform(0, 800)
        else:
            self.pos_x = pos_x

        if pos_y is None:
            self.pos_y = random.uniform(0, 600)
        else:
            self.pos_y = pos_y

    def move(self):
        # normilize direction vector to always be -1 to 1
        longueur = np.sqrt(self.direction_x ** 2 + self.direction_y ** 2)
        self.direction_x = self.direction_x / longueur if longueur > 0 else 0
        self.direction_y = self.direction_y / longueur if longueur > 0 else 0

        # define self next position
        self.pos_x = self.pos_x + self.direction_x * self.speed
        self.pos_y = self.pos_y + self.direction_y * self.speed
        if (self.pos_x > 800):
            self.pos_x = 800
            self.direction_x = self.direction_x * -1
        if (self.pos_x < 0):
            self.pos_x = 0
            self.direction_x = self.direction_x * -1
        if (self.pos_y > 600):
            self.pos_y = 600
            self.direction_y = self.direction_y * -1
        if (self.pos_y < 0):
            self.pos_y = 0
            self.direction_y = self.direction_y * -1

        # update energy and fitness
        self.energy = self.energy - self.speed * 0.1
        self.fitness += 1

    def draw(self, screen):
        color = (self.food_attraction * 255, self.poison_fear * 255, self.speed * 51)
        pygame.draw.circle(screen, color, (int(self.pos_x), int(self.pos_y)), 5)


    def detect_food(self, food_list):
        nearest_food = None
        nearest_dist = self.vision_range  # max

        for food in food_list:
            dist =  np.sqrt((food[0] - self.pos_x)**2 + (food[1] - self.pos_y )**2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_food = food

        if nearest_food is not None:
            self.direction_x += (nearest_food[0] - self.pos_x) / nearest_dist * self.food_attraction
            self.direction_y += (nearest_food[1] - self.pos_y) / nearest_dist * self.food_attraction

            if nearest_dist < 8:
                self.energy = self.energy + 5
                food_list.remove(nearest_food)

    def detect_poison(self, poison_list):
        nearest_poison = None
        nearest_dist = self.vision_range
        for poison in poison_list:
            dist = np.sqrt((poison[0] - self.pos_x)**2 + (poison[1] - self.pos_y)**2)
            if dist < nearest_dist:
                nearest_poison = poison
                nearest_dist = dist

        if nearest_poison is not None:
            self.direction_x += -(nearest_poison[0] - self.pos_x) / nearest_dist * self.poison_fear
            self.direction_y += -(nearest_poison[1] - self.pos_y) / nearest_dist * self.poison_fear

            if nearest_dist < 8:
                self.energy = self.energy - 5
                poison_list.remove(nearest_poison)


