# Build Guide — Experiment 04: NEAT

This guide walks through rebuilding experiment 04 from scratch, step by step.
Each step builds on the previous one. Read `neat-theory.md` first if you haven't already.

---

## Step 1 — InnovationTracker

Create `innovation_tracker.py`.

NEAT crossover requires that the same connection `A→B` always has the same ID across all genomes.
Build a class with:
- A counter starting at 0
- A dictionary mapping `(from_node, to_node)` → innovation number

Method `get_innovation_number(from_node, to_node)`:
- If the connection was already seen → return its existing number
- Otherwise → assign the next number, store it, return it

One instance is created at the start of `main.py` and passed everywhere.

---

## Step 2 — Node and Connection

Create `genome.py`. Start with two simple data classes.

**Node:** `node_id` (int), `node_type` (str: `'input'`, `'hidden'`, or `'output'`).

**Connection:** `from_node`, `to_node` (node IDs), `weight` (float), `innovation_number` (int), `active` (bool).

The `active` flag is critical — disabled connections are never deleted. They stay in the genome as evolutionary history and can be reactivated by future mutations.

---

## Step 3 — Genome

Add the `Genome` class to `genome.py`.

**Two construction modes:**

```python
# Generation 1 — minimal network
Genome(innovation_tracker=tracker)

# Crossover child — from evolution.py
Genome(node_list=nodes, connection_list=conns)
```

The minimal network has 6 nodes (4 inputs + 2 outputs) and 8 connections (every input to every output, random weights).

Node IDs:
- 0: food_dx, 1: food_dy, 2: poison_dx, 3: poison_dy (inputs)
- 4: direction_x, 5: direction_y (outputs)

**`forward_pass(inputs)`:**
1. Build `node_values` dict: inputs get their values, all others start at 0
2. For each active connection: `node_values[to] += node_values[from] * weight`
3. Return `[tanh(node_values[4]), tanh(node_values[5])]`

`tanh` bounds outputs to [-1, 1] and prevents oscillation from large accumulated weights.

---

## Step 4 — Creature

Copy `creature.py` from exp 03. Make two changes:
1. Replace `neural_network` parameter and attribute with `genome`
2. Replace `self.neural_network.forward(inputs)` with `self.genome.forward_pass(inputs)`
3. Add `innovation_tracker` as a constructor parameter (needed to create a new Genome)

Add explicit fitness rewards to strengthen the selection signal:
- `self.fitness += 100` when eating food (in `detect_food`)
- `self.fitness -= 50` when touching poison (in `detect_poison`)

Without these, all creatures survive ~1000 frames regardless of behavior, making selection blind.

---

## Step 5 — Evolution: selection and crossover

Create `evolution.py`. Start with `select_parent` (roulette wheel, same as exp 02-03).

Then write `crossover_neat(parent_1, parent_2)`:
1. Build `dict_1` and `dict_2` mapping `innovation_number → Connection` for each parent
2. For each innovation number in `dict_1`:
   - If also in `dict_2` → pick one connection randomly (50/50)
   - If only in `dict_1` → keep it (parent_1 is assumed fitter)
3. **Copy** each chosen connection into a new `Connection` object — never share references between genomes, or mutations on the child will corrupt the parent's weights
4. Build the child's node list from nodes referenced by child connections (no orphan nodes)
5. Return `Genome(node_list, connection_list)`

---

## Step 6 — Evolution: mutations

Add three mutation functions:

**`mutate_weight(genome)`**
For each connection, 10% chance to perturb weight by ±0.1. Same as exp 02-03.

**`mutate_add_connection(genome, innovation_tracker)`**
- Pick two random nodes
- Validate: `from_node` is not output, `to_node` is not input, connection doesn't already exist
- If valid: add new `Connection` with random weight, get innovation number from tracker
- If invalid: do nothing (intentional — keeps structural mutations sparse)

**`mutate_add_node(genome, innovation_tracker)`**
- Pick a random active connection A→B
- Disable it (set `active = False`)
- Create hidden node X with `id = max(existing ids) + 1`
- Add A→X (weight=1.0) and X→B (weight=original)
- Initial weights preserve the network's behavior so the new node starts neutral

---

## Step 7 — Species

Create `species.py`.

**`Species` class:** `representative_genome`, `members` list, `best_fitness`, `generation_without_improvement`.

**`genetic_distance(genome_1, genome_2)`:**
1. Build dicts of connections by innovation number for each genome
2. Separate into matching (same key in both) and non-matching (unique to one)
3. For matching pairs: compute `|w1 - w2|`, average them
4. Return `1.0 * (non_matching / N) + 0.5 * avg_weight_diff`

---

## Step 8 — Evolution: new_generation

Write `new_generation(creature_list, innovation_tracker, species_list)`:
1. Reset `species.members = []` for all species
2. Compute `total_fitness`
3. For 20 children:
   - Select two different parents via roulette wheel
   - `crossover_neat(parent_1, parent_2)`
   - `mutate_weight(child_genome)`
   - 5% chance: `mutate_add_connection`
   - 3% chance: `mutate_add_node`
   - Create `Creature(genome=child_genome, innovation_tracker=innovation_tracker)`
   - Assign to first species with `genetic_distance < 1.0`, or create new species
4. Return `next_gen`

---

## Step 9 — Main

Copy `main.py` from exp 03 and make these changes:
1. Add `InnovationTracker` import, create one instance
2. Add `species_list = []`
3. Pass `innovation_tracker` to each `Creature()` constructor
4. Pass `innovation_tracker, species_list` to `evolution.new_generation()`
5. Add `Species: {len(species_list)}` to the HUD
6. Add sim name/notes input at launch and auto-save plot to `docs/attempts/`

---

## Tuning parameters

| Parameter | Location | Default | Effect |
|-----------|----------|---------|--------|
| `mutation_rate` | `mutate_weight` | 0.1 | Higher = more weight noise per generation |
| `prob_add_connection` | `new_generation` | 0.05 | Higher = networks get more connections faster |
| `prob_add_node` | `new_generation` | 0.03 | Higher = networks get deeper faster |
| `species_threshold` | `new_generation` | 1.0 | Lower = more species (stricter grouping) |
| Food bonus | `creature.py` | +100 | Higher = stronger selection for food-seeking |
| Poison penalty | `creature.py` | -50 | Higher = stronger selection against poison |
| Food spawn rate | `main.py` | 3% | Higher = more food available, higher fitness ceiling |