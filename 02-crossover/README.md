# 🟡 02 — Crossover

The second experiment. Same world as 01, but creatures now reproduce sexually —
two parents combine their genes to produce each child.

No neural networks. No deep learning. Just genes, selection, crossover, and mutation.

---

## What's new vs 01

| Feature | 01 — Natural Selection | 02 — Crossover |
|---|---|---|
| Reproduction | 1 parent → 4 copies | 2 parents → 1 child |
| Parent selection | Top 5, equal weight | Roulette wheel (fitness-proportional) |
| Gene inheritance | Copy from single parent | 50/50 from either parent |
| Mutation | Applied after copy | Applied after crossover |

---

## What happens

- **20 creatures** spawn with random genes
- Each frame, they move, detect food/poison within their vision range, and lose energy
- When a creature's energy hits 0, it dies
- When all creatures are dead, the **top 5** are selected as the breeding pool
- **20 children** are produced: each child gets two parents chosen by roulette wheel
- After enough generations, creatures become noticeably better at surviving

---

## Genes

Each creature has 4 genes, fixed at birth:

| Gene | Range | Effect |
|------|-------|--------|
| `speed` | 1 – 5 | Movement speed per frame. Faster = finds food quicker, but burns more energy |
| `vision_range` | 20 – 150 | Detection radius in pixels. Larger = sees food/poison earlier |
| `food_attraction` | 0 – 1 | How strongly it steers toward detected food |
| `poison_fear` | 0 – 1 | How strongly it steers away from detected poison |

### Color encoding

Creature color reflects their genes at a glance:
- Red channel → `food_attraction`
- Green channel → `poison_fear`
- Blue channel → `speed`

---

## Fitness

```
fitness = number of frames survived
```

Simple. A creature that survives longer has a higher fitness.
Eating food increases energy → longer survival → higher fitness.
Touching poison decreases energy → shorter survival → lower fitness.

---

## Roulette Wheel Selection

Parents are chosen proportionally to their fitness. A creature with fitness 400
gets twice as many "slots" as one with fitness 200.

```
total_fitness = sum of all top 5 fitnesses
pick = random(0, total_fitness)
→ walk the list, accumulating fitness until you exceed pick
```

This means the best survivors reproduce more often — but all survivors have a chance.

---

## Uniform Crossover

Each gene is independently inherited from one of the two parents (50/50):

```
child.speed = parent_1.speed  ← if random() < 0.5
            = parent_2.speed  ← otherwise
```

This can produce combinations that neither parent had — the core power of crossover.

---

## Results

The fitness curve typically shows:
- A fast initial rise (easy gains from selection)
- A brief plateau (population exploring gene combinations)
- A second rise (a winning combination emerges and propagates)
- Final convergence

This plateau-then-rise pattern is the signature of crossover working —
it's absent in single-parent reproduction.

---

## Docs

- [Architecture](./docs/architecture.md) — How the code is structured and why
- [Build Guide](./docs/build-guide.md) — Step-by-step tutorial to rebuild from scratch

---

## Files

```
02-crossover/
├── main.py        # Pygame loop, simulation orchestration (unchanged from 01)
├── creature.py    # Creature class (unchanged from 01)
└── evolution.py   # Roulette wheel selection, crossover, mutation
```

---

## Tweak it

Open `evolution.py` to adjust:

```python
def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
```

- Increase `mutation_rate` to 0.3 — does convergence slow down or speed up?
- Change the breeding pool from top 5 to top 3 — what happens to diversity?
- Change 20 children to 30 — does a larger population explore more combinations?
