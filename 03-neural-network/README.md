# 03 — Neural Network

The third experiment. Creatures no longer have 4 fixed genes —
their behavior is now controlled by a neural network whose weights are the genes.

---

## What's new vs 02

| Feature | 02 — Crossover | 03 — Neural Network |
|---|---|---|
| Genome | 4 genes (speed, vision, etc.) | 36 weights (neural network) |
| Decision making | Genes directly steer direction | Network processes perception → outputs direction |
| Inputs | Hardcoded gene behavior | Distance to nearest food/poison (4 values) |
| Crossover | Per-gene 50/50 | Per-weight 50/50 on matrices |

---

## Architecture

```
INPUT (4)              HIDDEN (6)         OUTPUT (2)
dist_x_food    →
dist_y_food    →   [6 neurons + ReLU]  →  direction_x
dist_x_poison  →                       →  direction_y
dist_y_poison  →
```

**36 total weights = 36 genes**
- weights_1 : shape (4, 6) = 24 weights — input → hidden
- weights_2 : shape (6, 2) = 12 weights — hidden → output

---

## What happens

- **20 creatures** spawn with random neural network weights
- Each frame: perceive → think → move
- `think()` detects nearest food/poison, passes distances to the network,
  network outputs the new direction
- When no food or poison is visible, creature continues in its current direction (exploration)
- Fitness = frames survived
- Top 5 reproduce via roulette wheel + matrix crossover + mutation

---

## Results

![Fitness plot](./docs/plot.png)

The fitness curve shows a fast initial rise (gen 1-10), then a flat noisy plateau
oscillating between ~1020-1060 for 160 generations.

**Why it doesn't converge:**

1. Most of the time inputs are `[0, 0, 0, 0]` — the network rarely gets to make decisions
2. Creatures surviving ~1000 frames by random exploration alone is "good enough" —
   the fitness signal can't distinguish a creature that learned from one that got lucky
3. 36 weights optimized by blind evolution with only 20 creatures per generation
   is a very hard search problem — it needs many more generations or a smarter algorithm
4. Without backpropagation, the network has no direct signal about which weight
   caused a good or bad outcome

**This is exactly the problem NEAT solves** — by protecting new network topologies
long enough for them to develop useful behavior before being eliminated.

---

## Files

```
03-neural-network/
├── main.py            # Pygame loop (minimal changes from 02)
├── creature.py        # Creature with NeuralNetwork instead of 4 genes
├── neural_network.py  # NeuralNetwork class (forward pass, weights)
└── evolution.py       # Matrix crossover + mutation, roulette wheel
```

---

## Docs

- [Architecture](./docs/architecture.md) — Code structure and design decisions
- [Build Guide](./docs/build-guide.md) — Step-by-step tutorial
- [Neural Network Theory](./docs/neural-network-theory.md) — How neural networks work

---

## Tweak it

- Reduce `vision_range` in `creature.py` (currently 150) — forces more network activation
- Increase poison count in `main.py` — stronger selection pressure
- Increase `mutation_rate` in `evolution.py` — more exploration of weight space
- Add more food to reduce randomness in survival