# How a Neural Network Works

A visual primer before coding.

---

## 1. A single neuron

A neuron receives several values, multiplies each by its weight, and sums everything up.

```
input_1 = 0.5   weight_1 = 0.8
input_2 = 0.3   weight_2 = -0.4

output = (0.5 × 0.8) + (0.3 × -0.4)
       = 0.4 - 0.12
       = 0.28
```

That's it. A neuron = a weighted sum.

---

## 2. A layer of neurons

Now imagine 3 neurons all receiving the same 2 inputs.
Each neuron has ITS OWN weights.

```
                   neuron A : (0.5 × 0.8)  + (0.3 × -0.4) = 0.28
inputs [0.5, 0.3] → neuron B : (0.5 × -0.2) + (0.3 × 0.9)  = 0.17
                   neuron C : (0.5 × 0.5)  + (0.3 × 0.3)  = 0.34

layer output = [0.28, 0.17, 0.34]
```

---

## 3. Why a matrix?

Instead of coding each neuron separately, we group all weights
into a 2D array — a **matrix**.

Example: 2 inputs, 3 hidden neurons → matrix of shape (2, 3)

```
         neuron A  neuron B  neuron C
input_1 [  0.8      -0.2      0.5  ]
input_2 [ -0.4       0.9      0.3  ]
```

Each column = the weights of one neuron.
Each row = the weights connected to one input.

The entire layer computed in one numpy line:
```python
output = inputs @ weights   # matrix product
# [0.5, 0.3] @ matrix(2,3) → [0.28, 0.17, 0.34]
```

This is why we use matrices: it computes all neurons at once.

---

## 4. Our full network: 4 → 6 → 2

We have two layers of weights:

**Layer 1 — input to hidden**
```
shape : (4 inputs, 6 hidden neurons)
→ 4 × 6 = 24 weights
```

**Layer 2 — hidden to output**
```
shape : (6 hidden neurons, 2 outputs)
→ 6 × 2 = 12 weights
```

**Total: 36 weights = 36 genes**

---

## 5. The full computation (forward pass)

```
inputs = [dist_x_food, dist_y_food, dist_x_poison, dist_y_poison]

# Layer 1
hidden = inputs @ weights_1     # shape (4,) @ (4,6) → shape (6,)
hidden = relu(hidden)           # activation

# Layer 2
output = hidden @ weights_2     # shape (6,) @ (6,2) → shape (2,)

→ output = [direction_x, direction_y]
```

---

## 6. The ReLU activation function

Without activation, stacking layers is pointless — everything stays linear.
ReLU introduces non-linearity:

```
relu(x) = max(0, x)

relu(-0.5) = 0      ← silent neuron
relu(0.28) = 0.28   ← active neuron
relu(0.9)  = 0.9    ← active neuron
```

ReLU is applied after the hidden layer — not after the output.
Why not after the output? Because `direction_x` can legitimately be negative
(go left) — ReLU would cut all negative directions.

---

## 7. Weights = genes

In classic deep learning, weights are adjusted by backpropagation.
In our simulation, weights ARE the genes — inherited, crossed, and mutated
just like any other gene.

```
Experiment 01-02 :  4 genes   [speed, vision, food_attraction, poison_fear]
Experiment 03    : 36 genes   [all network weights]
```

Evolution has no idea these are network weights.
It just sees 36 numbers to optimize.

---

## 8. The zero-output problem

The network can produce outputs very close to `[0, 0]` when weights cancel each other out.
If `direction_x ≈ 0` and `direction_y ≈ 0`, the normalization in `move()` sets both to 0
and the creature freezes — even when food is nearby.

Fix: in `think()`, only apply the network output if it's large enough:

```python
outputs = self.neural_network.forward(inputs)
if abs(outputs[0]) > 0.01 or abs(outputs[1]) > 0.01:
    self.direction_x = outputs[0]
    self.direction_y = outputs[1]
# otherwise: keep current direction
```

---

## 9. Summary

```python
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_1 = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.weights_2 = np.random.uniform(-1, 1, (hidden_size, output_size))

    def forward(self, inputs):
        hidden = np.array(inputs) @ self.weights_1
        hidden = np.maximum(0, hidden)   # ReLU
        output = hidden @ self.weights_2
        return output                    # [direction_x, direction_y]
```

That's the entire network. Everything else (evolution, mutation, crossover)
works exactly the same — it just manipulates weights instead of simple gene values.
