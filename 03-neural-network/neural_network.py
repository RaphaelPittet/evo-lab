import numpy as np


class NeuralNetwork:
    def __init__(self, input_size=4, hidden_size=6, output_size=2, weights_1=None, weights_2=None):
        if weights_1 is None:
            self.weights_1 = np.random.uniform(-1, 1, (input_size, hidden_size))
        else:
            self.weights_1 = weights_1

        if weights_2 is None:
            self.weights_2 = np.random.uniform(-1, 1, (hidden_size, output_size))
        else:
            self.weights_2 = weights_2

    def forward(self, inputs):
        hidden = np.array(inputs) @ self.weights_1
        hidden = np.maximum(0, hidden)
        output = hidden @ self.weights_2
        return output