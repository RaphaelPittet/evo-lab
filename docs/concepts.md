# 🧠 Core Concepts

The theory behind all experiments in this repo.  
No math required — just intuition.

---

## 1. What is a Genetic Algorithm?

A **Genetic Algorithm (GA)** is a way to find good solutions to a problem by mimicking natural evolution.

Instead of programming the solution directly, you:
- Define what a "solution" looks like → the **genome**
- Define what "good" means → the **fitness function**
- Let evolution find the answer for you

### The loop

```
1. Create a random population of agents
2. Let them live in a simulated environment
3. Measure how well each one performed (fitness)
4. Select the best ones
5. Create a new generation from the best, with small mutations
6. Repeat
```

After enough generations, the population converges toward good solutions —  
without anyone explicitly programming the behavior.

---

## 2. Genes

A **gene** is a numeric parameter that defines an agent's behavior or traits.  
It is fixed at birth and inherited from parents (with possible mutation).

Genes are different from **state** — values that change during the simulation (like energy or position).  
Genes define *who the agent is*. State defines *where it is right now*.

---

## 3. Fitness Function

The **fitness function** measures how well an agent performed during its lifetime.  
It's the only signal evolution has — so it must reflect what you actually want.

> "You get what you measure."

Choosing the right fitness function is often the hardest part of building a simulation.  
A poorly designed fitness function will produce agents that game the metric  
without doing what you actually intended.

---

## 4. Selection

After a generation ends, you **select** the best performers to reproduce.  
Common strategies:

- **Elitism** — keep the top N agents
- **Tournament** — randomly pick pairs, the better one reproduces
- **Roulette** — probability of reproducing is proportional to fitness

Each strategy has tradeoffs between diversity and convergence speed.

---

## 5. Mutation

**Mutation** introduces random variation in genes.  
Without it, evolution would just clone the best agent forever and get stuck in a local optimum.

Two parameters control mutation:
- `mutation_rate` → probability that a gene mutates
- `mutation_range` → how much it can change

Too much mutation → chaos, no learning  
Too little mutation → stagnation, no exploration

---

## 6. Tradeoffs

Good simulations have **tradeoffs** between genes — no single strategy dominates.  
These tensions force evolution to find **balanced** solutions rather than just maximizing one trait.

If one gene is always better at any value, it's not interesting — it will just max out immediately.  
The interesting behavior emerges when genes compete against each other.

---

## 7. Emergence

**Emergence** is when complex behavior arises from simple rules.

Agents are not told what to do. They have genes, a position, and a fitness signal.  
Evolution figures out the rest.

This is the core idea behind all experiments in this repo.

---

## 8. Is this AI? Is this Machine Learning?

**Yes to AI. Partially to ML.**

Genetic algorithms are a branch of **Evolutionary Computation**, part of the broader AI field.

They are **not** deep learning:
- No neural networks (in basic GAs)
- No backpropagation
- No training data needed

| | Evolutionary AI | Deep Learning |
|---|---|---|
| Needs data? | ❌ No | ✅ Yes |
| Needs GPU? | ❌ No | ✅ Usually |
| How it learns | Selection + mutation | Backpropagation |
| Best for | Simulations, behavior, control | Images, text, classification |

Some experiments in this repo may combine both — for example **NEAT**,  
which evolves neural networks using a genetic algorithm.