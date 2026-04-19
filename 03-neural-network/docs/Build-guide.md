# Build Guide

Step-by-step tutorial to rebuild experiment 03 from scratch.
Assumes experiments 01 and 02 are understood. Focuses only on what's new.

---

## What you're adding

Three changes from experiment 02:

1. **`neural_network.py`** — new file, the NeuralNetwork class
2. **`creature.py`** — replace 4 genes with a NeuralNetwork, add `think()`
3. **`evolution.py`** — replace scalar crossover with matrix crossover

`main.py` barely changes — just replace `detect_food/detect_poison` calls with `think()`.

---

## Step 1 — Design the network architecture

Before coding, decide:

**What are the inputs?**
What the creature perceives each frame — not what it IS.
```
dist_x to nearest food    (0 if none visible)
dist_y to nearest food    (0 if none visible)
dist_x to nearest poison  (0 if none visible)
dist_y to nearest poison  (0 if none visible)
→ 4 inputs
```

**What are the outputs?**
What the creature controls each frame:
```
direction_x
direction_y
→ 2 outputs
```

**How many hidden neurons?**
Rule of thumb: between N_inputs and N_outputs, often 1.5-2x the inputs.
With 4 inputs and 2 outputs → 6 hidden neurons is a good start.

**Total weights:**
- Layer 1: 4 × 6 = 24 weights
- Layer 2: 6 × 2 = 12 weights
- Total: **36 weights = 36 genes**

---

## Step 2 — Build neural_network.py

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size=4, hidden_size=6, output_size=2,
                 weights_1=None, weights_2=None):
        # random init for gen 1, accept existing weights for crossover children
        self.weights_1 = np.random.uniform(-1, 1, (input_size, hidden_size)) \
                         if weights_1 is None else weights_1
        self.weights_2 = np.random.uniform(-1, 1, (hidden_size, output_size)) \
                         if weights_2 is None else weights_2

    def forward(self, inputs):
        hidden = np.array(inputs) @ self.weights_1  # (4,) @ (4,6) → (6,)
        hidden = np.maximum(0, hidden)              # ReLU activation
        output = hidden @ self.weights_2            # (6,) @ (6,2) → (2,)
        return output
```

Weights in [-1, 1] allow both excitatory (positive) and inhibitory (negative) signals.
The `weights_1/weights_2` optional params mirror the pattern from `Creature` genes.

---

## Step 3 — Update creature.py

**Remove:** `speed`, `vision_range`, `food_attraction`, `poison_fear` genes

**Add:** `self.neural_network = NeuralNetwork()` (or accept one as parameter)

**Rewrite detect_food() and detect_poison():**
They no longer steer — they only perceive and return `[dx, dy]` or `[0, 0]`:

```python
def detect_food(self, food_list):
    nearest, nearest_dist = None, self.vision_range
    for food in food_list:
        dist = np.sqrt((food[0]-self.pos_x)**2 + (food[1]-self.pos_y)**2)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest = food
    if nearest is not None:
        if nearest_dist < 8:
            self.energy += 5
            food_list.remove(nearest)
        return [(nearest[0]-self.pos_x)/nearest_dist,
                (nearest[1]-self.pos_y)/nearest_dist]
    return [0, 0]
```

**Add think():**

```python
def think(self, food_list, poison_list):
    food_dir   = self.detect_food(food_list)
    poison_dir = self.detect_poison(poison_list)
    inputs = food_dir + poison_dir  # [dx_f, dy_f, dx_p, dy_p]

    if inputs == [0, 0, 0, 0]:
        return  # nothing visible → keep current direction

    outputs = self.neural_network.forward(inputs)
    self.direction_x = outputs[0]
    self.direction_y = outputs[1]
```

The `[0,0,0,0]` check prevents the network from zeroing out the direction
when the creature has nothing to react to. Without it, creatures freeze.

---

## Step 4 — Update evolution.py

Replace `crossover_gene()` with `crossover_netrwork()`:

```python
def crossover_netrwork(p1_nn, p2_nn, mutation_rate, mutation_min, mutation_max):
    # uniform crossover — per-weight 50/50
    w1 = np.where(np.random.rand(*p1_nn.weights_1.shape) < 0.5,
                  p1_nn.weights_1, p2_nn.weights_1)
    w2 = np.where(np.random.rand(*p1_nn.weights_2.shape) < 0.5,
                  p1_nn.weights_2, p2_nn.weights_2)

    # mutation — add noise to randomly selected weights
    mask = np.random.rand(*w1.shape) < mutation_rate
    w1 = w1 + np.where(mask, np.random.uniform(mutation_min, mutation_max, w1.shape), 0)

    mask = np.random.rand(*w2.shape) < mutation_rate
    w2 = w2 + np.where(mask, np.random.uniform(mutation_min, mutation_max, w2.shape), 0)

    return NeuralNetwork(weights_1=w1, weights_2=w2)
```

**np.where explained:**
```
np.where(condition, value_if_true, value_if_false)
```
Applied element-wise on entire matrices — no Python loops needed.

**Mutation pattern:**
- `mask` : boolean matrix, True where a weight should mutate (~10% of weights)
- `noise` : matrix of small random values
- `np.where(mask, noise, 0)` : noise where mask=True, 0 elsewhere
- `w1 + ...` : add the sparse noise to existing weights (don't replace them)

Update `new_generation()` to use it:
```python
new_creature = Creature(
    neural_network=crossover_netrwork(
        parent_1.neural_network, parent_2.neural_network,
        mutation_rate, mutation_min, mutation_max
    )
)
```

---

## Step 5 — Update main.py

Replace the per-creature loop:
```python
# before (02)
creature.detect_food(foodList)
creature.detect_poison(poisonList)
creature.move()

# after (03)
creature.think(foodList, poisonList)
creature.move()
```

---

## Step 6 — Run and observe

```bash
python main.py
```

**What to expect:**
- Fast rise gen 1-10 (best random walkers selected)
- Flat noisy plateau after gen 10 — no clear convergence

**Why it stagnates:**

This is expected and instructive. 36 weights optimized by blind evolution
with 20 creatures per generation is a very hard search problem. The fitness signal
(frames survived) doesn't clearly distinguish "learned to find food" from "got lucky
with starting position." The network rarely gets activated because creatures spend
most of their time seeing nothing (inputs = [0,0,0,0]).

This is exactly the limitation that NEAT addresses in experiment 04:
- Speciation protects new network topologies long enough to develop
- The topology itself evolves (adding neurons and connections over time)
- Starting simple and growing complexity gradually avoids the search space explosion

---

## Ideas to explore

- Reduce `vision_range` to 50 — forces more network activation
- Add more poison — stronger selection pressure
- Track how often inputs are non-zero — measure how much the network actually contributes
- Try 500+ generations — does it ever converge?