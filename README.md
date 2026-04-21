# Evo-Lab

A collection of evolutionary simulation experiments built from scratch in Python.
Each experiment explores a different concept — from basic natural selection to neural evolution.

> No machine learning frameworks. No datasets. Just a simulator, a fitness function, and time.

---

## Experiments

| # | Name | Concepts | Status |
|---|------|----------|--------|
| 01 | [Natural Selection](./01-natural-selection-basics/) | Genetic algorithm, fitness, elitism, mutation | Done |
| 02 | [Crossover](./02-crossover/) | Sexual reproduction, roulette wheel selection, uniform crossover | Done |
| 03 | [Neural Network](./03-neural-network/) | Neural network as genome, matrix crossover, ReLU | Done |
| 04 | [NEAT](./04-neat/) | Variable topology, innovation numbers, structural mutations, speciation | Done |
| 05 | Doodle Jump (NEAT) | Independent evaluation per agent, platform jumping | Coming soon |

---

## What is this?

These simulations are inspired by channels like **Code BH** and **Primer** — where simple rules and natural selection produce surprisingly complex behaviors.

The core idea is always the same:

1. Create a **population** of agents with random traits
2. Let them live in a **simulated environment**
3. The best survivors **reproduce** with small mutations
4. Repeat — and watch intelligence emerge

This is a **Genetic Algorithm**, a branch of **Evolutionary AI**.
It does not use deep learning, does not need a GPU or a dataset — just a simulator and a definition of "good enough".

---

## Evolutionary AI vs Deep Learning

| | Evolutionary AI (this repo) | Deep Learning |
|---|---|---|
| Needs data? | No | Yes (lots of it) |
| Needs GPU? | No | Usually |
| How it learns | Natural selection + mutation | Backpropagation |
| Best for | Simulations, behavior, control | Images, text, classification |

---

## Getting Started

### Requirements

- Python 3.11+
- pip

### Install dependencies

```bash
pip install pygame numpy matplotlib
```

### Run an experiment

```bash
cd 01-natural-selection-basics
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| `SPACE` | Toggle speed x1 / x10 |
| `UP` | Increase speed |
| `DOWN` | Decrease speed |
| Close window | Save fitness graph + show it |

---

## Global Docs

- [Core Concepts](./docs/concepts.md) — What is a genetic algorithm? Fitness? Mutation?
- [Getting Started](./docs/getting-started.md) — Python + Pygame setup guide

---

## Repo Structure

```
evo-lab/
├── README.md
├── docs/
│   ├── concepts.md
│   └── getting-started.md
├── 01-natural-selection-basics/
├── 02-crossover/
├── 03-neural-network/
└── 04-neat/
    ├── docs/
    │   ├── neat-theory.md
    │   ├── Architecture.md
    │   ├── Build-guide.md
    │   └── attempts/       ← saved fitness plots per run
    ├── innovation_tracker.py
    ├── genome.py
    ├── species.py
    ├── creature.py
    ├── evolution.py
    └── main.py
```