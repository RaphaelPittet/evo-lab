# Genome — replaces NeuralNetwork from exp 03
#
# Instead of fixed-size weight matrices, a Genome stores explicit lists of
# Node and Connection objects. This allows the topology (number of nodes and
# connections) to vary between individuals and evolve over generations.
import random
import numpy as np

class Node:
    # A single neuron. node_type is 'input', 'hidden', or 'output'.
    # Processing order during forward pass: input → hidden → output.
    def __init__(self, node_id, node_type):
        self.node_id = node_id
        self.node_type = node_type


class Connection:
    # A directed link between two nodes.
    # innovation_number: global ID that identifies this connection across all genomes,
    #   enabling crossover between different topologies (see InnovationTracker).
    # active: False means the connection is disabled but kept in the genome —
    #   it can be reactivated by mutation and preserves evolutionary history.
    def __init__(self, from_node, to_node, active, weight, innovation_number):
        self.from_node = from_node
        self.to_node = to_node
        self.active = active
        self.weight = weight
        self.innovation_number = innovation_number


class Genome:
    # Two construction modes:
    #   Generation 1: Genome(innovation_tracker=tracker)
    #     → creates minimal network: 4 inputs + 2 outputs, all connected, random weights
    #   Crossover child: Genome(node_list=nodes, connection_list=conns)
    #     → uses already-computed nodes and connections from evolution.py
    def __init__(self, node_list=None, connection_list=None, innovation_tracker=None):
        if connection_list is None and innovation_tracker is None:
            raise ValueError("innovation_tracker required to create a new Genome")

        # Node IDs 0-3: inputs (food_dx, food_dy, poison_dx, poison_dy)
        # Node IDs 4-5: outputs (direction_x, direction_y)
        if node_list is None:
            self.node_list = [
                Node(node_id=0, node_type='input'),
                Node(node_id=1, node_type='input'),
                Node(node_id=2, node_type='input'),
                Node(node_id=3, node_type='input'),
                Node(node_id=4, node_type='output'),
                Node(node_id=5, node_type='output'),
            ]
        else:
            self.node_list = node_list

        # Minimal network: every input connected to every output (4×2 = 8 connections)
        if connection_list is None:
            self.connection_list = [
                Connection(from_node=0, to_node=4, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(0, 4)),
                Connection(from_node=1, to_node=4, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(1, 4)),
                Connection(from_node=2, to_node=4, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(2, 4)),
                Connection(from_node=3, to_node=4, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(3, 4)),
                Connection(from_node=0, to_node=5, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(0, 5)),
                Connection(from_node=1, to_node=5, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(1, 5)),
                Connection(from_node=2, to_node=5, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(2, 5)),
                Connection(from_node=3, to_node=5, active=True, weight=random.uniform(-1, 1), innovation_number=innovation_tracker.get_innovation_number(3, 5)),
            ]
        else:
            self.connection_list = connection_list

        self.innovation_tracker = innovation_tracker

    def forward_pass(self, inputs):
        # Map each node_id to its current activation value
        # Inputs are assigned directly; hidden and output nodes start at 0
        node_values = {
            0: inputs[0],   # food_dx
            1: inputs[1],   # food_dy
            2: inputs[2],   # poison_dx
            3: inputs[3],   # poison_dy
            4: 0,           # output: direction_x
            5: 0,           # output: direction_y
        }

        # Also initialise any hidden nodes that may have been added by mutation
        for node in self.node_list:
            if node.node_type == 'hidden' and node.node_id not in node_values:
                node_values[node.node_id] = 0

        # Propagate signals: for each active connection, add weighted source value to destination
        for connection in self.connection_list:
            if connection.active:
                node_values[connection.to_node] += node_values[connection.from_node] * connection.weight

        # tanh bounds outputs to [-1, 1] and stabilizes direction —
        # without it, large weights produce unbounded values that cause erratic oscillation
        return [np.tanh(node_values[4]), np.tanh(node_values[5])]