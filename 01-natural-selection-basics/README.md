# 🟢 01 — Natural Selection

The first experiment. Creatures evolve to find food and avoid poison using a basic genetic algorithm.

No neural networks. No deep learning. Just genes, selection, and mutation.

---

## What happens

- **20 creatures** spawn with random genes
- Each frame, they move, detect food/poison within their vision range, and lose energy
- When a creature's energy hits 0, it dies
- When all creatures are dead, the **top 5** reproduce → 20 new creatures with mutated genes
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
- 🔴 Red channel → `food_attraction`
- 🟢 Green channel → `poison_fear`
- 🔵 Blue channel → `speed`

---

## Fitness

```
fitness = number of frames survived
```

Simple. A creature that survives longer has a higher fitness.  
Eating food increases energy → longer survival → higher fitness.  
Touching poison decreases energy → shorter survival → lower fitness.

---

## Results

After ~10 generations, average fitness typically plateaus at a higher level than generation 1.  
The fitness graph (shown on close) should show a rising curve that flattens out.

This is the classic **evolutionary convergence** pattern.

---

## Docs

- [Architecture](./docs/architecture.md) — How the code is structured and why
- [Build Guide](./docs/build-guide.md) — Step-by-step tutorial to rebuild from scratch

---

## Files

```
01-natural-selection/
├── main.py        # Pygame loop, simulation orchestration
├── creature.py    # Creature class (genes, movement, detection, drawing)
└── evolution.py   # Selection, mutation, new generation
```

---

## Tweak it

Open `main.py` and experiment with these values:

```python
creatureList = [Creature() for _ in range(20)]   # population size
foodList     = [...for _ in range(10)]            # initial food count
poisonList   = [...for _ in range(10)]            # initial poison count

if random.random() < 0.01:   # food spawn rate
if random.random() < 0.005:  # poison spawn rate
```

Open `evolution.py` to adjust:

```python
def new_generation(creature_list, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
```

Try increasing `mutation_rate` to 0.5 and see what happens to the fitness curve.