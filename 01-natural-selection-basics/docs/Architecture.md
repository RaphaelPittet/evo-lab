# 🏗️ Architecture

How the code is structured and why each piece exists.

---

## Overview

```
main.py        → orchestrates everything (Pygame loop)
creature.py    → defines what a creature IS and what it can DO
evolution.py   → defines how a new generation is created
```

Three files. Clear separation of responsibilities.

---

## creature.py

### The Creature class

A creature has two types of data:

**Genes** — fixed at birth, inherited from parents, define behavior:
```python
self.speed           # movement speed
self.vision_range    # detection radius
self.food_attraction # steering strength toward food
self.poison_fear     # steering strength away from poison
```

**State** — changes during simulation, not inherited:
```python
self.pos_x, self.pos_y    # position in the window
self.direction_x, self.direction_y  # normalized movement vector
self.energy               # current energy (starts at 100)
self.fitness              # frames survived (used for selection)
```

### Why Optional gene parameters?

```python
def __init__(self, speed=None, ...):
    if speed is None:
        self.speed = random.uniform(1, 5)  # generation 1: random
    else:
        self.speed = max(1, min(5, speed)) # generation 2+: from parent (clamped)
```

The same constructor handles both random initialization and child creation.  
Clamping (`max/min`) ensures genes never exceed their valid range after mutation.

### Movement and direction

The direction vector `(direction_x, direction_y)` is always **normalized** (length = 1).  
This means `speed` is the only thing that controls actual movement speed.

```python
# normalize before moving
length = sqrt(dx² + dy²)
direction_x /= length
direction_y /= length

# then move
pos_x += direction_x * speed
```

Without normalization, steering toward food would accelerate the creature,  
making `speed` meaningless as a gene.

### Detection logic

```python
def detect_food(self, food_list):
    # find nearest food within vision_range
    # steer toward it (weighted by food_attraction gene)
    # eat it if distance < 8px
```

The direction is updated with `+=` so food and poison influences combine:

```python
self.direction_x += (food_x - self.pos_x) / dist * self.food_attraction
self.direction_x -= (poison_x - self.pos_x) / dist * self.poison_fear  # opposite
```

If food and poison are both visible, the stronger gene wins.

---

## evolution.py

### new_generation()

```python
def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    creature_list.sort(key=lambda c: c.fitness, reverse=True)
    best = creature_list[:5]

    new_gen = []
    for creature in best:
        for _ in range(4):  # 4 children per parent = 20 total
            child = Creature(
                speed = mutate(creature.speed, ...),
                ...
            )
            new_gen.append(child)
    return new_gen
```

**Sort by fitness** → best survivors first  
**Take top 5** → elitism selection  
**4 children each** → 5 × 4 = 20, same population size  
**Mutation per gene** → each gene mutates independently

### Why per-gene mutation?

```python
speed = creature.speed + random.uniform(-0.1, 0.1) if random.random() < mutation_rate else creature.speed
```

Each gene has its own independent chance to mutate.  
A child might inherit `speed` unchanged but get a different `vision_range`.  
This creates more genetic diversity than mutating everything at once.

---

## main.py

### The simulation loop

```python
while running:
    handle_events()         # quit, keypress

    screen.fill(...)        # clear screen

    for _ in range(speed_multiplier):   # run N ticks per frame
        spawn_food_poison()
        for creature in creatures:
            creature.detect_food()
            creature.detect_poison()
            creature.move()
            creature.draw()

        filter_dead()       # remove energy <= 0
        if all_dead():
            next_generation()

    pygame.display.flip()
    clock.tick(60)
```

### Why speed_multiplier?

Running multiple simulation ticks per rendered frame allows fast-forwarding  
without changing the simulation logic. Everything inside the loop scales correctly:
- Food/poison spawn rates scale with ticks
- Creature movement and energy consumption scale with ticks
- Drawing also happens inside the loop — in fast mode, creatures draw multiple times per frame, creating a slight trail effect on the same buffer before `display.flip()`.

### Why dead_creature accumulates?

```python
dead_creature += [c for c in creatureList if c.energy <= 0]
creatureList   = [c for c in creatureList if c.energy > 0]
```

We need **all** dead creatures from the generation to rank them by fitness.  
If we only kept the last ones to die, we'd lose data about early deaths.