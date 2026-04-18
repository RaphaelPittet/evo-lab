# Core Concepts

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
5. Create a new generation from the best, with crossover and mutation
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

After a generation ends, you **select** which agents get to reproduce.
This is where evolution's pressure comes from.

### Common strategies

**Elitism (truncation selection)**
Keep the top N agents. Simple and fast to converge, but can lose diversity quickly.
```
top 5 of 20 survive → 25% survival rate → high selection pressure
top 10 of 20 survive → 50% survival rate → lower selection pressure
```

**Tournament selection**
Randomly pick small groups (e.g. 3 agents), the best one in each group reproduces.
Used a lot in practice because it scales well and is easy to tune.

**Roulette wheel (fitness-proportional selection)**
Each agent's chance of being selected is proportional to its fitness.
An agent with fitness 400 is twice as likely to reproduce as one with fitness 200.
```
total_fitness = sum of all fitnesses
pick = random(0, total_fitness)
→ walk the list accumulating fitness until you exceed pick
```
More biologically realistic than elitism. Preserves diversity better.
Risk: if one agent dominates with a very high fitness, it crowds out everyone else.

### Selection pressure

**Selection pressure** = how strictly you reward the best and punish the rest.

High pressure → fast convergence, low diversity, risk of local optima
Low pressure → slow convergence, high diversity, better global search

In practice: start with moderate pressure, increase it if the population stagnates.

---

## 5. Crossover (Recombination)

**Crossover** is sexual reproduction — two parents combine their genes to produce a child.
It allows evolution to explore combinations that neither parent had alone.

> Parent A: speed=0.9, vision=20 — fast but blind
> Parent B: speed=0.2, vision=150 — slow but perceptive
> Child: speed=0.9, vision=150 — fast AND perceptive (impossible from one parent)

This is the key advantage over single-parent mutation: crossover explores the space of
*combinations*, not just local perturbations around a single solution.

### Types of crossover

**Uniform crossover**
Each gene is independently chosen from one of the two parents (50/50).
```
Parent 1: [0.9,  120,  0.8,  0.3]
Parent 2: [0.4,   40,  0.2,  0.9]
Child:    [0.9,   40,  0.8,  0.9]  ← each gene drawn independently
```
Most flexible. Maximum number of possible combinations. Used in this repo.

**One-point crossover**
A single cut point is chosen randomly. Everything before it comes from parent 1,
everything after from parent 2.
```
Parent 1: [0.9,  120  |  0.8,  0.3]
Parent 2: [0.4,   40  |  0.2,  0.9]
Child:    [0.9,  120,    0.2,  0.9]  ← cut after gene 2
```
Closer to biological reality (chromosomes physically break and rejoin).
Preserves gene "neighborhoods" — genes near each other tend to co-inherit.
Fewer possible combinations than uniform.

**Two-point crossover**
Two cut points. Segment between them comes from parent 2, rest from parent 1.
```
Parent 1: [0.9  |  120,  0.8  |  0.3]
Parent 2: [0.4  |   40,  0.2  |  0.9]
Child:    [0.9,     40,  0.2,    0.3]
```
Common in practice. Good balance between mixing and preserving structure.

### Which to use?

| Type | Combinations | Gene linkage | When to use |
|---|---|---|---|
| Uniform | Maximum | None | Small genomes, independent genes |
| One-point | Moderate | Preserved | Genes that work together |
| Two-point | Moderate | Partial | Default for most problems |

For simple flat gene lists (like our 4-gene creatures), uniform crossover is standard.
For structured genomes (like neural network weights), one/two-point is often better.

---

## 6. Mutation

**Mutation** introduces random variation in genes.
Without it, crossover can only recombine what's already in the population —
if a gene value never appeared, it can never emerge.

Two parameters control mutation:
- `mutation_rate` → probability that a gene mutates (typical: 0.01–0.1)
- `mutation_range` → how much it can change (typical: small relative to gene range)

Too much mutation → chaos, no learning
Too little mutation → stagnation, no new exploration

### Mutation vs crossover

Crossover **recombines** existing solutions → exploits what the population already found
Mutation **creates** new values → explores beyond what the population has seen

Both are necessary:
- Crossover alone gets stuck when the population converges (nothing new to recombine)
- Mutation alone is slow (random local search, no benefit from other agents)

The standard order: crossover first, then mutation. Apply mutation to the child, not the parent.

---

## 7. Tradeoffs

Good simulations have **tradeoffs** between genes — no single strategy dominates.
These tensions force evolution to find **balanced** solutions rather than just maximizing one trait.

If one gene is always better at any value, it's not interesting — it will just max out immediately.
The interesting behavior emerges when genes compete against each other.

---

## 8. Convergence and Diversity

**Convergence** = the population is settling on similar gene values
**Diversity** = the population still explores many different combinations

These are in tension. The art of genetic algorithms is managing both.

Signs of premature convergence:
- Fitness plateaus early and stops improving
- All agents look identical (same colors in our simulations)
- Increasing mutation rate doesn't help

Solutions:
- Lower selection pressure (keep more survivors)
- Increase mutation rate
- Add a diversity bonus to the fitness function
- Use speciation (NEAT's key innovation — groups similar agents together
  so niches can develop without competing directly)

---

## 9. Emergence

**Emergence** is when complex behavior arises from simple rules.

Agents are not told what to do. They have genes, a position, and a fitness signal.
Evolution figures out the rest.

This is the core idea behind all experiments in this repo.

---

## 10. Is this AI? Is this Machine Learning?

**Yes to AI. Partially to ML.**

Genetic algorithms are a branch of **Evolutionary Computation**, part of the broader AI field.

They are **not** deep learning:
- No neural networks (in basic GAs)
- No backpropagation
- No training data needed

| | Evolutionary AI | Deep Learning |
|---|---|---|
| Needs data? | No | Yes |
| Needs GPU? | No | Usually |
| How it learns | Selection + mutation | Backpropagation |
| Best for | Simulations, behavior, control | Images, text, classification |

Some experiments in this repo combine both — for example **NEAT**,
which evolves neural networks using a genetic algorithm.

---

## 11. Rules of thumb (field practice)

These are the defaults practitioners reach for when starting a new GA.
Adjust from here based on what you observe.

| Parameter | Typical starting value | If fitness stagnates | If fitness is chaotic |
|---|---|---|---|
| Population size | 20–100 | Increase | — |
| Survival rate | 20–30% | Decrease (more pressure) | Increase |
| Mutation rate | 0.01–0.1 per gene | Increase | Decrease |
| Mutation range | 5–10% of gene range | Increase | Decrease |
| Crossover type | Uniform (flat genomes) | Try two-point | — |

**When to use elitism vs roulette:**
- Elitism converges faster, good for simple problems or early prototyping
- Roulette preserves more diversity, better when the fitness landscape is complex
- In practice, many implementations combine both: keep top 1–2 via elitism,
  fill the rest via roulette

**Population size rule of thumb:**
Bigger populations explore more but are slower per generation.
For problems with N genes, a population of 10× N is a reasonable start.