# 🧬 Evo-Lab

A collection of evolutionary simulation experiments built from scratch in Python.  
Each experiment explores a different concept — from basic natural selection to neural evolution.

> No machine learning frameworks. No datasets. Just a simulator, a fitness function, and time.

---

## 🧪 Experiments

| # | Name | Concepts | Status |
|---|------|----------|--------|
| 01 | [Natural Selection](./01-natural-selection-basics/) | Genetic algorithm, fitness, mutation | ✅ Done |
| 02 | NEAT | Neuroevolution, neural networks as genes | 🔜 Soon |

---

## 💡 What is this?

These simulations are inspired by channels like **Code BH** and **Primer** — where simple rules and natural selection produce surprisingly complex behaviors.

The core idea is always the same:

1. Create a **population** of agents with random traits
2. Let them live in a **simulated environment**
3. The best survivors **reproduce** with small mutations
4. Repeat — and watch intelligence emerge

This is called a **Genetic Algorithm**, and it's a branch of **Evolutionary AI**.  
It's not deep learning. It doesn't need a GPU or a dataset.  
It just needs a simulator and a definition of "good enough".

---

## 🆚 Evolutionary AI vs Deep Learning

| | Evolutionary AI (this repo) | Deep Learning |
|---|---|---|
| Needs data? | ❌ No | ✅ Yes (lots of it) |
| Needs GPU? | ❌ No | ✅ Usually |
| How it learns | Natural selection + mutation | Backpropagation |
| Best for | Simulations, behavior, control | Images, text, classification |

---

## 🚀 Getting Started

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
| Close window | Show fitness history graph |

---

## 📚 Global Docs

- [Core Concepts](./docs/concepts.md) — What is a genetic algorithm? Fitness? Mutation?
- [Getting Started](./docs/getting-started.md) — Python + Pygame setup guide

---

## 🗂️ Repo Structure

```
evo-lab/
├── README.md
├── docs/
│   ├── concepts.md
│   └── getting-started.md
└── 01-natural-selection-basics/
    ├── README.md
    ├── docs/
    │   ├── architecture.md
    │   └── build-guide.md
    ├── main.py
    ├── creature.py
    └── evolution.py
```