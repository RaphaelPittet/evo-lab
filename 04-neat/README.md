# Experiment 04 — NEAT

**NEAT** (NeuroEvolution of Augmenting Topologies) evolves both the **weights** and the **structure** of neural networks simultaneously.

Unlike experiment 03 where the architecture was fixed (4→6→2), NEAT starts with a minimal network and lets evolution decide when to add nodes and connections.

## Key concepts

- **Innovation numbers** — unique IDs for each connection, enabling crossover between different topologies
- **Structural mutations** — add node, add connection, toggle connection
- **Speciation** — groups structurally similar networks so new innovations have time to prove their value

## New files vs experiment 03

| File | Role |
|------|------|
| `innovation_tracker.py` | Global counter that assigns innovation numbers |
| `genome.py` | Replaces `neural_network.py` — stores Node and Connection lists |
| `species.py` | Groups genomes by structural similarity |
| `creature.py` | Uses a Genome instead of a NeuralNetwork |
| `evolution.py` | NEAT crossover, mutation, speciation |
| `main.py` | Pygame simulation loop |

## What evolves

- Connection weights (like exp 03)
- Network topology: new nodes, new connections, disabled connections

## Docs

- [`docs/neat-theory.md`](docs/neat-theory.md) — NEAT concepts and how it differs from simple neural network evolution
- [`docs/Architecture.md`](docs/Architecture.md) — code structure and design decisions
- [`docs/Build-guide.md`](docs/Build-guide.md) — step-by-step tutorial