# Architecture — Experiment 04: NEAT

## File overview

| File | Role |
|------|------|
| `innovation_tracker.py` | Global registry of connection innovations |
| `genome.py` | Node, Connection, and Genome classes |
| `species.py` | Species class and genetic distance function |
| `creature.py` | Simulation agent — uses a Genome instead of a NeuralNetwork |
| `evolution.py` | NEAT selection, crossover, structural mutations, speciation |
| `main.py` | Pygame simulation loop |

---

## innovation_tracker.py

### `InnovationTracker`
One instance shared across the entire population.

Every time a connection `A→B` appears via mutation, `get_innovation_number(A, B)` is called:
- If `A→B` was already seen: returns the existing number
- If new: assigns the next available number, stores it, returns it

This guarantees that the same structural connection always has the same ID across all genomes — which is what makes NEAT crossover possible.

---

## genome.py

### `Node`
A single neuron. Stores `node_id` (int) and `node_type` (`'input'`, `'hidden'`, or `'output'`).

Node IDs 0-3 are inputs, 4-5 are outputs. Hidden nodes get IDs starting from 6, assigned incrementally by `mutate_add_node`.

### `Connection`
A directed link between two nodes. Stores:
- `from_node`, `to_node`: node IDs (not objects)
- `weight`: float, initialized in [-1, 1]
- `innovation_number`: global ID for this connection
- `active`: bool — disabled connections are kept for crossover history, never deleted

### `Genome`
Replaces `NeuralNetwork` from exp 03. Stores variable-length lists of Nodes and Connections.

**Two construction modes:**
- `Genome(innovation_tracker=tracker)` → minimal network: 4 inputs + 2 outputs, 8 random connections
- `Genome(node_list=nodes, connection_list=conns)` → crossover child, built by `evolution.py`

**`forward_pass(inputs)`:**
1. Assign input values to input node IDs (0-3)
2. Initialize all other nodes to 0
3. For each active connection: `node_values[to] += node_values[from] * weight`
4. Apply `tanh` to output nodes → bounded [-1, 1], prevents oscillation from large weights
5. Return `[direction_x, direction_y]`

Note: connections are processed in list order, not topologically sorted. For multi-layer hidden networks this can cause signal propagation issues — acceptable for this experiment's complexity level.

---

## species.py

### `Species`
Stores a `representative_genome` (reference for distance comparisons), a `members` list, `best_fitness`, and `generation_without_improvement`.

Members are cleared at the start of each generation and reassigned after crossover.

### `genetic_distance(genome_1, genome_2)`
Computes structural + weight similarity:

```
distance = 1.0 * (non_matching / N) + 0.5 * avg_weight_diff
```

- `non_matching`: connections unique to one genome
- `avg_weight_diff`: mean |w1 - w2| on matching connections
- `N`: max genome size (normalizes for network length)

Threshold used in `new_generation`: `< 1.0` → same species.

---

## creature.py

Almost identical to exp 03. Key change: `self.genome` (Genome) replaces `self.neural_network` (NeuralNetwork).

`think()` calls `self.genome.forward_pass(inputs)` instead of `self.neural_network.forward(inputs)`.

Fitness tracking:
- `+1` per frame survived (base survival signal)
- `+100` when eating food (strong reward for food-seeking behavior)
- `-50` when touching poison (penalizes poison-seeking behavior)

The bonus/penalty are necessary because without them, all creatures survive ~1000 frames (energy/decay) regardless of behavior, making selection effectively random.

---

## evolution.py

### `new_generation(creature_list, innovation_tracker, species_list)`
Full NEAT generation cycle:
1. Reset species member lists
2. For 20 children: select 2 parents (roulette wheel), crossover, mutate, assign to species

### `select_parent(creature_list, total_fitness)`
Roulette wheel — same as exp 02-03.

### `crossover_neat(parent_1, parent_2)`
Aligns connections by innovation number:
- Matching (both parents): inherit 50/50
- Only in parent_1 (fitter): always keep
- Only in parent_2: discard

Each connection is **copied** (not referenced) so child mutations don't affect parent weights. This was a critical bug in early versions.

Nodes are derived from the child's connections — no orphan nodes.

### `mutate_weight(genome)`
10% chance per connection, ±0.1 perturbation. Same as exp 02-03.

### `mutate_add_connection(genome, innovation_tracker)`
Picks two random valid nodes, adds a connection if not already present. Not guaranteed to succeed (intentional — keeps structural mutations sparse).

### `mutate_add_node(genome, innovation_tracker)`
Splits an active connection A→B:
- Disables A→B
- Adds hidden node X
- Adds A→X (weight=1.0) and X→B (weight=original)

Initial weights preserve the network's behavior right after the mutation.

---

## main.py

Identical structure to exp 01-03. Key additions:
- `InnovationTracker` created once, shared across all generations
- `species_list` initialized empty, updated by `new_generation` each generation
- HUD shows generation, speed, last avg fitness, and species count
- Simulation name and notes entered at launch, used for auto-saved plot filenames in `docs/attempts/`