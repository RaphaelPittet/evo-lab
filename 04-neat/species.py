# Species — groups genomes by structural similarity
#
# Speciation protects new structural innovations (new nodes, new connections) from
# being eliminated before their weights have time to be optimized. Without speciation,
# a mutant with a new node would compete against fully-optimized simpler networks
# and almost always lose — even if the new topology has long-term potential.
#
# Each genome is assigned to the first species whose representative is within
# a genetic distance threshold. If no match, a new species is created.


class Species:
    def __init__(self, representative_genome, members=None):
        # representative_genome: one genome used as reference for distance comparisons
        self.representative_genome = representative_genome
        self.members = members if members is not None else []
        self.best_fitness = 0
        # Tracks how many generations this species has gone without improvement.
        # Used to eliminate stagnant species (not yet implemented — placeholder).
        self.generation_without_improvement = 0


def genetic_distance(genome_1, genome_2):
    # Measures structural and weight similarity between two genomes.
    # Used to decide if they belong to the same species.
    #
    # Formula: coef_1 * (non_matching / N) + coef_2 * avg_weight_diff
    #   non_matching: connections that exist in only one genome (structural difference)
    #   avg_weight_diff: average |w1 - w2| on matching connections (weight difference)
    #   N: size of the larger genome (normalizes for network size)

    dict_1 = {c.innovation_number: c for c in genome_1.connection_list}
    dict_2 = {c.innovation_number: c for c in genome_2.connection_list}

    matching_connection = []     # list of (c1, c2) pairs with same innovation number
    non_matching_connection = [] # connections unique to one genome

    for innovation_number in dict_1:
        if innovation_number in dict_2:
            matching_connection.append((dict_1[innovation_number], dict_2[innovation_number]))
        else:
            non_matching_connection.append(dict_1[innovation_number])

    for innovation_number in dict_2:
        if innovation_number not in dict_1:
            non_matching_connection.append(dict_2[innovation_number])

    coef_1 = 1.0  # weight for structural difference
    coef_2 = 0.5  # weight for weight difference
    N = max(len(dict_1), len(dict_2))

    weight_diff_sum = 0
    for c1, c2 in matching_connection:
        weight_diff_sum += abs(c1.weight - c2.weight)
    avg_weight_diff = weight_diff_sum / len(matching_connection) if matching_connection else 0

    distance = coef_1 * len(non_matching_connection) / N + coef_2 * avg_weight_diff
    return distance