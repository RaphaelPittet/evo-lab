# Build Guide

A step-by-step tutorial to rebuild experiment 02 from scratch.
This guide assumes you have completed experiment 01 and focuses only on what's new.

---

## Prerequisites

- Experiment 01 completed and understood
- Python 3.11+
- `pip install pygame numpy matplotlib`

---

## What you're adding

Experiment 02 only modifies `evolution.py`. The creature and simulation are identical to 01.
You'll implement three things:

1. **Roulette wheel selection** — parents chosen proportionally to fitness
2. **Uniform crossover** — each gene independently inherited from one of two parents
3. **Two-parent reproduction** — 20 children, each from a unique pair

---

## Step 1 — Copy experiment 01

```
02-crossover/
├── main.py        ← copy from 01, no changes needed
├── creature.py    ← copy from 01, no changes needed
└── evolution.py   ← copy from 01, then rewrite
```

---

## Step 2 — Design the selection strategy

Before touching code, answer:

**Why not equal-weight selection?**
A creature that survived 500 frames has better genes than one that survived 100.
Equal weight throws that information away.

**What is roulette wheel selection?**
Each creature gets a slice of a wheel proportional to its fitness.
You spin the wheel (pick a random number 0 → total_fitness) and see where it lands.

```
total = 800  (sum of all fitnesses)
creature A: fitness 400  →  slots 0–400    (50%)
creature B: fitness 200  →  slots 400–600  (25%)
creature C: fitness 200  →  slots 600–800  (25%)

pick = random(0, 800)
→ walk the list, accumulate fitness, stop when you exceed pick
```

---

## Step 3 — Implement select_parent()

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

The fallback `return creatures[-1]` exists because floating-point arithmetic can make
`pick` very slightly exceed `total_fitness`, causing the loop to complete without returning.
Returning the last creature is correct — it's the one whose slot we're inside.

---

## Step 4 — Implement crossover_gene()

Each child gene comes from one of two parents (50/50), then gets an independent chance to mutate:

```python
def crossover_gene(gene_parent_1, gene_parent_2, mutation_rate, mutation_min, mutation_max):
    gene = gene_parent_1 if random.random() < 0.5 else gene_parent_2
    gene = gene + random.uniform(mutation_min, mutation_max) if random.random() < mutation_rate else gene
    return gene
```

Crossover and mutation are separate operations applied in sequence.
This lets you tune them independently — lower mutation, higher crossover, or vice versa.

---

## Step 5 — Rewrite new_generation()

Replace the old `for creature in best` loop with a `for _ in range(20)` loop:

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
            speed           = crossover_gene(parent_1.speed,           parent_2.speed,           mutation_rate, mutation_min, mutation_max),
            vision_range    = crossover_gene(parent_1.vision_range,    parent_2.vision_range,    mutation_rate, mutation_min, mutation_max),
            food_attraction = crossover_gene(parent_1.food_attraction, parent_2.food_attraction, mutation_rate, mutation_min, mutation_max),
            poison_fear     = crossover_gene(parent_1.poison_fear,     parent_2.poison_fear,     mutation_rate, mutation_min, mutation_max),
        ))
    return new_gen
```

Key decisions:
- `[c for c in best if c != parent_1]` — excludes parent_1 from parent_2 selection
- `total_fitness - parent_1.fitness` — recalculates the total for the reduced pool
- Each gene calls `crossover_gene` independently — different genes can come from different parents

---

## Step 6 — Run and observe

```bash
python main.py
```

- Press `SPACE` to speed up
- Watch the fitness curve — look for the plateau-then-rise pattern
- Compare the convergence speed with experiment 01

**What to look for:**
- Slower convergence than 01 (more exploration)
- A brief plateau followed by a second rise (crossover finding a winning combination)
- More varied colors in early generations (higher diversity)

---

## Ideas to explore next

- Change the breeding pool from top 5 to top 3 — does the roulette become less useful?
- Try `mutation_rate=0` — what happens when crossover is the only source of change?
- Add a crossover rate parameter (currently 50/50) — what if it's 70/30 toward the better parent?
- Plot not just average fitness but also best fitness per generation
