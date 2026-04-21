import random
from genome import Genome, Connection, Node
from creature import Creature
from species import genetic_distance, Species

# Evolution — NEAT selection, crossover, mutation, speciation


def new_generation(creature_list, innovation_tracker, species_list):
    # Full NEAT generation cycle:
    # 1. Reset species member lists (members are reassigned each generation)
    # 2. For each of the 20 children: select 2 parents, crossover, mutate, assign to species
    next_gen = []
    total_fitness = sum(c.fitness for c in creature_list)

    for species in species_list:
        species.members = []

    for _ in range(20):
        parent_1 = select_parent(creature_list, total_fitness)
        parent_2 = select_parent(creature_list, total_fitness)
        while parent_1 == parent_2:
            parent_2 = select_parent(creature_list, total_fitness)

        child_genome = crossover_neat(parent_1, parent_2)

        # Always mutate weights; structural mutations are rare (probabilistic)
        mutate_weight(child_genome)
        if random.random() < 0.05:
            mutate_add_connection(child_genome, innovation_tracker)
        if random.random() < 0.03:
            mutate_add_node(child_genome, innovation_tracker)

        child = Creature(genome=child_genome, innovation_tracker=innovation_tracker)
        next_gen.append(child)

        # Assign child to the first species whose representative is close enough
        # If no match, create a new species with this child as its first member
        assigned = False
        for species in species_list:
            if genetic_distance(child_genome, species.representative_genome) < 1.0:
                species.members.append(child)
                assigned = True
                break
        if not assigned:
            new_species = Species(representative_genome=child_genome)
            new_species.members.append(child)
            species_list.append(new_species)

    return next_gen


def select_parent(creature_list, total_fitness):
    # Roulette wheel selection: probability of being chosen is proportional to fitness.
    # A creature with fitness 400 is twice as likely to be selected as one with fitness 200.
    pick = random.uniform(0, total_fitness)
    current = 0
    for c in creature_list:
        current += c.fitness
        if current > pick:
            return c
    return creature_list[-1]


def crossover_neat(parent_1, parent_2):
    # NEAT crossover: align connections by innovation number.
    # parent_1 is assumed to be the fitter parent.
    #
    # Matching genes (same innovation number in both parents) → inherit 50/50
    # Disjoint/excess genes (only in parent_1) → always inherited
    # Genes only in parent_2 (weaker parent) → discarded
    #
    # Each connection is COPIED (not referenced) so mutations on the child
    # do not affect the parent's weights — a critical correctness requirement.

    dict_1 = {c.innovation_number: c for c in parent_1.genome.connection_list}
    dict_2 = {c.innovation_number: c for c in parent_2.genome.connection_list}

    child_connections = []
    for innov_num in dict_1:
        if innov_num in dict_2:
            c = dict_1[innov_num] if random.random() < 0.5 else dict_2[innov_num]
        else:
            c = dict_1[innov_num]
        # Copy the connection object — never share references between genomes
        child_connections.append(Connection(c.from_node, c.to_node, c.active, c.weight, c.innovation_number))

    # Build child node list from nodes actually referenced by child connections.
    # Avoids inheriting orphan nodes that have no connections in the child topology.
    all_nodes = {n.node_id: n for n in parent_1.genome.node_list + parent_2.genome.node_list}
    node_ids_added = set()
    node_to_add = []
    for connection in child_connections:
        if connection.from_node not in node_ids_added:
            node_ids_added.add(connection.from_node)
            node_to_add.append(all_nodes[connection.from_node])
        if connection.to_node not in node_ids_added:
            node_ids_added.add(connection.to_node)
            node_to_add.append(all_nodes[connection.to_node])

    return Genome(node_to_add, child_connections)


def mutate_weight(genome, mutation_rate=0.1, mutation_min=-0.1, mutation_max=0.1):
    # Perturb each connection weight independently with probability mutation_rate.
    # Same mechanism as exp 02-03, just applied to a connection list instead of a matrix.
    for connection in genome.connection_list:
        if random.random() < mutation_rate:
            connection.weight += random.uniform(mutation_min, mutation_max)


def mutate_add_connection(genome, innovation_tracker):
    # Pick two random nodes and add a connection between them if valid and not already present.
    # Valid: from_node is not an output, to_node is not an input.
    # Not guaranteed to succeed — if the random pair is invalid, nothing happens (intentional).
    # This keeps structural mutations rare and prevents networks from growing too fast.
    existing_connections = {(c.from_node, c.to_node) for c in genome.connection_list}
    from_node = random.choice(genome.node_list)
    to_node = random.choice(genome.node_list)

    if (from_node.node_type != 'output'
            and to_node.node_type != 'input'
            and (from_node.node_id, to_node.node_id) not in existing_connections):
        genome.connection_list.append(Connection(
            from_node=from_node.node_id,
            to_node=to_node.node_id,
            active=True,
            weight=random.uniform(-1, 1),
            innovation_number=innovation_tracker.get_innovation_number(from_node.node_id, to_node.node_id)
        ))


def mutate_add_node(genome, innovation_tracker):
    # Split an existing active connection A→B into A→X→B.
    # The original A→B is disabled (not deleted — preserved for crossover history).
    # A→X gets weight 1.0 and X→B gets the original weight so the network
    # behaves identically right after the mutation, giving the new node time to be optimized.
    active_connections = [c for c in genome.connection_list if c.active]
    if not active_connections:
        return

    selected_connection = random.choice(active_connections)
    selected_connection.active = False

    new_node = Node(
        node_id=max(n.node_id for n in genome.node_list) + 1,
        node_type='hidden'
    )

    genome.node_list.append(new_node)
    genome.connection_list.append(Connection(
        from_node=selected_connection.from_node,
        to_node=new_node.node_id,
        active=True,
        weight=1.0,
        innovation_number=innovation_tracker.get_innovation_number(selected_connection.from_node, new_node.node_id)
    ))
    genome.connection_list.append(Connection(
        from_node=new_node.node_id,
        to_node=selected_connection.to_node,
        active=True,
        weight=selected_connection.weight,
        innovation_number=innovation_tracker.get_innovation_number(new_node.node_id, selected_connection.to_node)
    ))