import math
import random

class NeuralNetwork:
    def __init__(self, layers, weights = None):
        self.layers = layers

        self.nodes = self.init_nodes()
        self.weights = self.init_weights() if weights is None else weights
        self.biases = self.init_biases()

    def feed_forward(self, input_data):
        for i in range(len(self.nodes[0])):
            self.nodes[0][i] = input_data[i]

        for i in range(len(self.weights)):
            previous_nodes = self.nodes[i]
            layer_values = []

            for j in range(len(self.weights[i])):
                value = 0

                for k in range(len(self.weights[i][j])):
                    value += self.weights[i][j][k] * previous_nodes[k] + self.biases[i][j]

                layer_values.append(self.sigmoid(value))

            self.nodes[i + 1] = layer_values

    def get_output_values(self):
        return self.nodes[-1]

    def sigmoid(self, value):
        if value > 700:
            value = 700

        return 1 / (1 + math.exp(value))

    def init_nodes(self):
        nodes = []
        for layer in self.layers:
            nodes.append([ 0 for i in range(layer) ])
        return nodes

    def init_weights(self):
        weights = []

        for i in range(len(self.layers) - 1):
            current_layer = self.layers[i]
            next_layer = self.layers[i + 1]

            layer_weights = []

            for j in range(next_layer):
                layer = [ random.random() for k in range(current_layer) ]
                layer_weights.append(layer)

            weights.append(layer_weights)

        return weights

    def init_biases(self):
        biases = []
        for i in range(len(self.layers) - 1):
            layer = self.layers[i + 1]
            biases.append([ 0 for i in range(layer) ])
        return biases