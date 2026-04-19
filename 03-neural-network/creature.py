import random

import numpy as np
import pygame
from neural_network import NeuralNetwork

class Creature:
    def __init__(self, neural_network=None, pos_x=None, pos_y=None):
        self.energy = 100
        self.fitness = 0
        self.speed = 1
        self.vision_range = 50
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)

        if neural_network is None:
            self.neural_network = NeuralNetwork()
        else:
            self.neural_network = neural_network

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
        if self.pos_x > 800:
            self.pos_x = 800
            self.direction_x = self.direction_x * -1
        if self.pos_x < 0:
            self.pos_x = 0
            self.direction_x = self.direction_x * -1
        if self.pos_y > 600:
            self.pos_y = 600
            self.direction_y = self.direction_y * -1
        if self.pos_y < 0:
            self.pos_y = 0
            self.direction_y = self.direction_y * -1

        # update energy and fitness
        self.energy = self.energy - self.speed * 0.1
        self.fitness += 1

    def draw(self, screen):
        color = ( 255, 255, 255)
        pygame.draw.circle(screen, color, (int(self.pos_x), int(self.pos_y)), 5)


    def detect_food(self, food_list):
        nearest_food = None
        nearest_dist = self.vision_range # max
        food_direction = []

        for food in food_list:
            dist =  np.sqrt((food[0] - self.pos_x)**2 + (food[1] - self.pos_y )**2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_food = food

        if nearest_food is not None:
            direction_x = (nearest_food[0] - self.pos_x) / nearest_dist
            direction_y = (nearest_food[1] - self.pos_y) / nearest_dist
            food_direction = [direction_x, direction_y]

            if nearest_dist < 8:
                self.energy = self.energy + 5
                food_list.remove(nearest_food)
                return food_direction

            return food_direction
        else:
            food_direction = [0, 0]
            return food_direction



    def detect_poison(self, poison_list):
        nearest_poison = None
        nearest_dist = self.vision_range
        poison_direction = []
        for poison in poison_list:
            dist = np.sqrt((poison[0] - self.pos_x)**2 + (poison[1] - self.pos_y)**2)
            if dist < nearest_dist:
                nearest_poison = poison
                nearest_dist = dist

        if nearest_poison is not None:
            direction_x = -(nearest_poison[0] - self.pos_x) / nearest_dist
            direction_y = -(nearest_poison[1] - self.pos_y) / nearest_dist
            poison_direction = [direction_x, direction_y]

            if nearest_dist < 8:
                self.energy = self.energy - 5
                poison_list.remove(nearest_poison)

            return poison_direction
        else:
            poison_direction = [0, 0]
            return poison_direction


    def think(self, food_list, poison_list):
        food_direction = self.detect_food(food_list)
        poison_direction = self.detect_poison(poison_list)
        inputs = food_direction + poison_direction

        # no input then continue in the same direction
        if inputs == [0, 0, 0, 0]:
            return

        outputs = self.neural_network.forward(inputs)
        if abs(outputs[0]) > 0.01 or abs(outputs[1]) > 0.01:
            self.direction_x = outputs[0]
            self.direction_y = outputs[1]
