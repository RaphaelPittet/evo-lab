# 🔨 Build Guide

A step-by-step tutorial to rebuild this experiment from scratch.  
Follow this to understand how each piece is built and why.

---

## Prerequisites

- Python 3.11+
- `pip install pygame numpy matplotlib`
- Basic Python knowledge (classes, loops, functions)

---

## Step 1 — Verify Pygame works

Create `main.py` and paste:

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

You should see a dark gray window. That's your canvas.

---

## Step 2 — Design the Creature

Before writing code, answer these questions:

**What are its genes?** (fixed at birth, inherited)
- `speed` → 1 to 5
- `vision_range` → 20 to 150
- `food_attraction` → 0 to 1
- `poison_fear` → 0 to 1

**What is its state?** (changes during simulation)
- `pos_x`, `pos_y` → position
- `direction_x`, `direction_y` → normalized movement vector
- `energy` → starts at 100, dies at 0
- `fitness` → frames survived, used for selection

**What does it do?**
- `move()` → update position, bounce off walls, consume energy, increment fitness
- `detect_food(food_list)` → steer toward nearest food, eat if close
- `detect_poison(poison_list)` → steer away from nearest poison, take damage if close
- `draw(screen)` → render itself as a colored circle

---

## Step 3 — Build creature.py

Create `creature.py`:

```python
import random
import numpy as np
import pygame

class Creature:
    def __init__(self, speed=None, vision_range=None, food_attraction=None, poison_fear=None, pos_x=None, pos_y=None):
        self.energy = 100
        self.fitness = 0
        self.direction_x = random.uniform(-1, 1)
        self.direction_y = random.uniform(-1, 1)

        # Genes: random for gen 1, clamped value from parent for gen 2+
        self.speed           = random.uniform(1, 5)      if speed is None           else max(1,  min(5,   speed))
        self.vision_range    = random.uniform(20, 150)   if vision_range is None    else max(20, min(150, vision_range))
        self.food_attraction = random.uniform(0, 1)      if food_attraction is None else max(0,  min(1,   food_attraction))
        self.poison_fear     = random.uniform(0, 1)      if poison_fear is None     else max(0,  min(1,   poison_fear))

        self.pos_x = random.uniform(0, 800) if pos_x is None else pos_x
        self.pos_y = random.uniform(0, 600) if pos_y is None else pos_y
```

> **Why `max/min` clamping?**  
> After mutation, a gene could exceed its valid range. Clamping prevents invalid values  
> (e.g. color > 255 crashing Pygame, or speed < 0 moving backward).

---

## Step 4 — Add move()

```python
def move(self):
    # Always normalize direction so speed is the only velocity control
    length = np.sqrt(self.direction_x**2 + self.direction_y**2)
    if length > 0:
        self.direction_x /= length
        self.direction_y /= length

    self.pos_x += self.direction_x * self.speed
    self.pos_y += self.direction_y * self.speed

    # Bounce off walls
    if self.pos_x > 800: self.pos_x = 800; self.direction_x *= -1
    if self.pos_x < 0:   self.pos_x = 0;   self.direction_x *= -1
    if self.pos_y > 600: self.pos_y = 600; self.direction_y *= -1
    if self.pos_y < 0:   self.pos_y = 0;   self.direction_y *= -1

    # Energy cost proportional to speed (tradeoff!)
    self.energy -= self.speed * 0.1
    self.fitness += 1
```

> **Why normalize?**  
> Without it, steering toward food adds to the direction vector's magnitude,  
> making the creature accelerate uncontrollably. Normalization keeps length = 1  
> so only `speed` determines how far it moves each frame.

---

## Step 5 — Add detect_food() and detect_poison()

```python
def detect_food(self, food_list):
    nearest, nearest_dist = None, self.vision_range

    for food in food_list:
        dist = np.sqrt((food[0] - self.pos_x)**2 + (food[1] - self.pos_y)**2)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest = food

    if nearest is not None:
        # Steer toward food, weighted by food_attraction gene
        self.direction_x += (nearest[0] - self.pos_x) / nearest_dist * self.food_attraction
        self.direction_y += (nearest[1] - self.pos_y) / nearest_dist * self.food_attraction
        if nearest_dist < 8:
            self.energy += 5
            food_list.remove(nearest)

def detect_poison(self, poison_list):
    nearest, nearest_dist = None, self.vision_range

    for poison in poison_list:
        dist = np.sqrt((poison[0] - self.pos_x)**2 + (poison[1] - self.pos_y)**2)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest = poison

    if nearest is not None:
        # Steer AWAY from poison (note the minus sign), weighted by poison_fear gene
        self.direction_x -= (nearest[0] - self.pos_x) / nearest_dist * self.poison_fear
        self.direction_y -= (nearest[1] - self.pos_y) / nearest_dist * self.poison_fear
        if nearest_dist < 8:
            self.energy -= 5
            poison_list.remove(nearest)
```

> **Why `+=` on direction?**  
> Food and poison can both be visible at the same time. Using `+=` lets both influences  
> combine — the dominant gene wins. The direction is renormalized in `move()` anyway.

---

## Step 6 — Add draw()

```python
def draw(self, screen):
    color = (
        self.food_attraction * 255,  # red
        self.poison_fear * 255,      # green
        self.speed * 51              # blue (51 = 255/5)
    )
    pygame.draw.circle(screen, color, (int(self.pos_x), int(self.pos_y)), 5)
```

Color reflects genes visually — you can spot high-speed or food-loving creatures at a glance.

---

## Step 7 — Build evolution.py

```python
import random
from creature import Creature

def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    # Sort by fitness descending (best survivors first)
    creature_list.sort(key=lambda c: c.fitness, reverse=True)
    best = creature_list[:5]  # keep top 5

    new_gen = []
    for creature in best:
        for _ in range(4):  # 4 children each = 20 total
            new_gen.append(Creature(
                speed           = creature.speed           + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.speed,
                vision_range    = creature.vision_range    + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.vision_range,
                food_attraction = creature.food_attraction + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.food_attraction,
                poison_fear     = creature.poison_fear     + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else creature.poison_fear,
            ))
    return new_gen
```

> **Why 5 parents × 4 children?**  
> Keeps population size stable at 20. Adjust these numbers to experiment —  
> more parents = more diversity, fewer parents = faster convergence.

---

## Step 8 — Wire everything in main.py

```python
import pygame, random, matplotlib.pyplot as plt
from creature import Creature
import evolution

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 24)

creatures       = [Creature() for _ in range(20)]
food_list       = [[random.uniform(0,800), random.uniform(0,600)] for _ in range(10)]
poison_list     = [[random.uniform(0,800), random.uniform(0,600)] for _ in range(10)]
dead_creatures  = []
fitness_history = []
generation      = 1
speed_mult      = 1
running         = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            plt.plot(fitness_history)
            plt.title("Average fitness per generation")
            plt.xlabel("Generation")
            plt.ylabel("Avg fitness (frames survived)")
            plt.show()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            speed_mult = 10 if speed_mult == 1 else 1

    screen.fill((30, 30, 30))
    screen.blit(font.render(f"Generation: {generation}  |  Speed: x{speed_mult}", True, (255,255,255)), (10, 10))

    for _ in range(speed_mult):
        if random.random() < 0.01:  food_list.append([random.uniform(0,800), random.uniform(0,600)])
        if random.random() < 0.005: poison_list.append([random.uniform(0,800), random.uniform(0,600)])

        for food   in food_list:   pygame.draw.circle(screen, (0,255,0),   (int(food[0]),   int(food[1])),   3)
        for poison in poison_list: pygame.draw.circle(screen, (255,0,0),   (int(poison[0]), int(poison[1])), 3)
        for c      in creatures:
            c.detect_food(food_list)
            c.detect_poison(poison_list)
            c.move()
            c.draw(screen)

        dead_creatures += [c for c in creatures if c.energy <= 0]
        creatures       = [c for c in creatures if c.energy  > 0]

        if len(creatures) == 0:
            fitness_history.append(sum(c.fitness for c in dead_creatures) / len(dead_creatures))
            creatures    = evolution.new_generation(dead_creatures)
            food_list    = [[random.uniform(0,800), random.uniform(0,600)] for _ in range(10)]
            poison_list  = [[random.uniform(0,800), random.uniform(0,600)] for _ in range(10)]
            dead_creatures = []
            generation  += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## Step 9 — Run and observe

```bash
python main.py
```

- Press `SPACE` to speed up
- Watch colors shift over generations (gene pool converging)
- Close the window to see the fitness graph

If the graph trends upward → **evolution is working**.

---

## Ideas to explore next

- Change `mutation_rate` to 0.5 — does it help or hurt?
- Add a crossover step (mix genes from two parents instead of one)
- Visualize `vision_range` as a faint circle around each creature
- Add obstacles that creatures must navigate around
- Track and display the best gene values per generation