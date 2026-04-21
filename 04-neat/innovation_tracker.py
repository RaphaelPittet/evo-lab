# InnovationTracker — global registry of connection innovations
#
# One instance shared across the entire population.
# Every time a new connection (A→B) appears via mutation, it receives a unique
# innovation number. If the same connection appears again later (in any genome),
# it gets the SAME number — not a new one.
# This allows crossover between genomes with different topologies: connections
# with matching innovation numbers are equivalent and can be combined 50/50.

class InnovationTracker:
    def __init__(self):
        self.innovation_count = 0       # next number to assign
        self.innovation_dict = {}       # (from_node, to_node) → innovation_number

    def get_innovation_number(self, from_node, to_node):
        # Return existing number if this connection was already seen
        if (from_node, to_node) in self.innovation_dict:
            return self.innovation_dict[(from_node, to_node)]

        # Otherwise assign a new number and record it
        self.innovation_dict[(from_node, to_node)] = self.innovation_count
        result = self.innovation_count
        self.innovation_count += 1
        return result