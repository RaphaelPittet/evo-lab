# Architecture

How the code is structured and why each piece exists.

---

## Overview

```
main.py        → orchestrates everything (Pygame loop)       [unchanged from 01]
creature.py    → defines what a creature IS and what it can DO [unchanged from 01]
evolution.py   → defines how a new generation is created      [rewritten for 02]
```

Three files. Clear separation of responsibilities.
Only `evolution.py` changed — the simulation and creature logic are identical to 01.

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
        self.speed = max(1, min(5, speed)) # generation 2+: from parents (clamped)
```

The same constructor handles both random initialization and child creation.
Clamping (`max/min`) ensures genes never exceed their valid range after mutation.

---

## evolution.py

This is where all the new logic lives. Three functions, each with a single responsibility.

### crossover_gene()

```python
def crossover_gene(gene_parent_1, gene_parent_2, mutation_rate, mutation_min, mutation_max):
    gene = gene_parent_1 if random.random() < 0.5 else gene_parent_2
    gene = gene + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else gene
    return gene
```

**Step 1 — crossover**: pick one parent's gene at random (50/50).
**Step 2 — mutation**: independently, maybe nudge the value slightly.

Keeping these two operations separate and in sequence is deliberate:
crossover explores the existing genetic space; mutation expands it.

### select_parent()

```python
def select_parent(creatures, total_fitness):
    pick = random.uniform(0, total_fitness)
    current = 0
    for c in creatures:
        current += c.fitness
        if current > pick:
            return c
    return creatures[-1]  # float precision fallback
```

Roulette wheel selection: a creature with fitness 400 occupies twice as much
of the wheel as one with fitness 200. The fallback `return creatures[-1]`
guards against floating-point rounding where `pick` narrowly exceeds `total_fitness`.

### new_generation()

```python
def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    creature_list.sort(key=lambda c: c.fitness, reverse=True)
    best = creature_list[:5]

    total_fitness = sum(c.fitness for c in best)
    new_gen = []
    for _ in range(20):
        parent_1 = select_parent(best, total_fitness)
        parent_2 = select_parent([c for c in best if c != parent_1], total_fitness - parent_1.fitness)
        new_gen.append(Creature(
            speed           = crossover_gene(parent_1.speed,           parent_2.speed,           ...),
            vision_range    = crossover_gene(parent_1.vision_range,    parent_2.vision_range,    ...),
            food_attraction = crossover_gene(parent_1.food_attraction, parent_2.food_attraction, ...),
            poison_fear     = crossover_gene(parent_1.poison_fear,     parent_2.poison_fear,     ...),
        ))
    return new_gen
```

**Sort by fitness** → best survivors first
**Take top 5** → breeding pool
**20 × roulette pairs** → 20 children, population stays stable
**parent_1 excluded from parent_2 pool** → prevents self-crossover

Why exclude parent_1 from the second draw?
A child with two identical parents is just a mutated clone — no crossover benefit.
Excluding parent_1 forces genetic mixing every time.

---

## main.py

Unchanged from experiment 01. See [01 architecture](../../01-natural-selection-basics/docs/architecture.md) for details.

The simulation loop, speed multiplier, dead creature accumulation, and fitness graph
are all identical — only the `evolution.new_generation()` call produces different results.
