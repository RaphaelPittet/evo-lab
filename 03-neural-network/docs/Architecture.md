# Architecture

How the code is structured and why each piece exists.

---

## Overview

```
main.py            → orchestrates everything (minimal changes from 02)
creature.py        → Creature with NeuralNetwork instead of 4 genes
neural_network.py  → NeuralNetwork class (weights, forward pass)
evolution.py       → matrix crossover + mutation, roulette wheel (unchanged)
```

The key change from 02: `creature.py` lost its 4 genes and gained a `NeuralNetwork`.
`evolution.py` now crosses matrices instead of scalar values.

---

## neural_network.py

### Why two weight matrices?

The network has two layers of connections:

```
[inputs] --weights_1--> [hidden] --weights_2--> [output]
```

Each layer is a separate matrix because the shapes are different:
- `weights_1` : (4, 6) — connects 4 inputs to 6 hidden neurons
- `weights_2` : (6, 2) — connects 6 hidden neurons to 2 outputs

They can't be merged into one matrix — they have different dimensions.

### The constructor

```python
def __init__(self, input_size=4, hidden_size=6, output_size=2, weights_1=None, weights_2=None):
    if weights_1 is None:
        self.weights_1 = np.random.uniform(-1, 1, (input_size, hidden_size))
    else:
        self.weights_1 = weights_1
    # same for weights_2
```

Same pattern as `Creature` — optional parameters allow both random init (gen 1)
and construction from existing weights (crossover children).

Weights initialized in [-1, 1] because negative weights allow inhibition —
a neuron can signal "go the opposite direction."

### forward()

```python
def forward(self, inputs):
    hidden = np.array(inputs) @ self.weights_1   # (4,) @ (4,6) → (6,)
    hidden = np.maximum(0, hidden)               # ReLU
    output = hidden @ self.weights_2             # (6,) @ (6,2) → (2,)
    return output
```

`@` is the matrix product operator in numpy. It computes all 6 hidden neurons at once.
ReLU (`np.maximum(0, hidden)`) sets negative neuron outputs to 0 — neurons either
fire or stay silent. Without it, stacking layers adds no expressive power.

ReLU is only applied after the hidden layer, not after the output —
because `direction_x` and `direction_y` can legitimately be negative (go left/up).

---

## creature.py

### What changed from 02

**Removed:**
- `self.speed` (gene) → replaced by constant `self.speed = 1`
- `self.vision_range` (gene) → replaced by constant `self.vision_range = 150`
- `self.food_attraction`, `self.poison_fear` → removed entirely

**Added:**
- `self.neural_network` → a `NeuralNetwork` instance
- `think(food_list, poison_list)` → the perception-decision loop

### detect_food() and detect_poison()

In experiments 01-02, these methods did two things: perceive AND steer.
In 03, they only **perceive** — they return `[dx, dy]` toward the target,
or `[0, 0]` if nothing is in range.

The network makes the steering decision, not these methods.

### think()

```python
def think(self, food_list, poison_list):
    food_direction   = self.detect_food(food_list)    # [dx, dy] or [0, 0]
    poison_direction = self.detect_poison(poison_list) # [dx, dy] or [0, 0]
    inputs = food_direction + poison_direction         # [dx_f, dy_f, dx_p, dy_p]

    if inputs == [0, 0, 0, 0]:
        return  # nothing visible → keep current direction (exploration)

    outputs = self.neural_network.forward(inputs)
    self.direction_x = outputs[0]
    self.direction_y = outputs[1]
```

When inputs are all zero, we skip the network and keep the current direction.
This prevents creatures from freezing when nothing is visible.

---

## evolution.py

### crossover_netrwork()

```python
def crossover_netrwork(p1_nn, p2_nn, mutation_rate, mutation_min, mutation_max):
    # crossover — per-weight 50/50
    weights_1 = np.where(np.random.rand(*p1_nn.weights_1.shape) < 0.5,
                         p1_nn.weights_1, p2_nn.weights_1)
    weights_2 = np.where(np.random.rand(*p1_nn.weights_2.shape) < 0.5,
                         p1_nn.weights_2, p2_nn.weights_2)

    # mutation — add small noise to randomly selected weights
    mask  = np.random.rand(*weights_1.shape) < mutation_rate
    noise = np.random.uniform(mutation_min, mutation_max, weights_1.shape)
    weights_1 = weights_1 + np.where(mask, noise, 0)
    # same for weights_2

    return NeuralNetwork(weights_1=weights_1, weights_2=weights_2)
```

**Crossover:** `np.where(mask, A, B)` picks element-wise from matrix A or B based on a random boolean mask. Same uniform crossover as 02, applied to every weight in both matrices.

**Mutation:** A random mask selects which weights mutate. `np.where(mask, noise, 0)` creates a sparse noise matrix — only selected weights get a nudge. This is added to the existing weights, not replacing them. This preserves what's already working while introducing small variations.

### Why matrices and not loops?

One `np.where` call processes all 24 or 12 weights simultaneously.
A Python loop doing the same would be ~10-50x slower. Numpy operations
run in optimized C code — always prefer them over loops for array operations.