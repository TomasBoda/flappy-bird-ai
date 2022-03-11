# Flappy Bird AI using Genetic Algorithm
by [Tomáš Boďa](https://github.com/TomasBoda)

## About
The aim of this project was to create a Flappy Bird game that learns to play itself using a **Neural Network** based on the **Genetic Algorithm**.

## Technical details
The project is written entirely in Python. The game uses the **PyGame** package for rendering and game logic. The Neural Network and the Genetic Algorithm is written entirely from scratch without the usage of any external libraries and packages.

## Neural Network
The Neural Network consists of neurons, weights and biases all represented by Python lists. The Neural Network is scalable and flexible, designed to take the `layers` parameter representing individual layers of the network and the number of neurons in each layer. The Feed Forward algorithm takes values from the input neurons, feeds them into the network and forwards them through the network all the way to the output neurons. I opted for the **Sigmoid** function to normalize neuron values into the interval of `[0, 1]`. Below is the implementation of the Neural Network.

```python
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
```

## Genetic Algorithm
The Genetic Algorithm is a heuristic algorithm inspired by the Charles Darwin's theory of evolution. It is based on the principle of natural selection, where the strongest individuals are chosen for producing offsprings, which result in a better generation of individuals. The algorithm takes all dead birds as its input and returns a new generation of birds. One of the main steps in producing a new generation is the **Crossover** function, that takes two individuals and based on their neural networks produces a new individual with genes inhereted from both parents. Below is the implementation of the Genetic Algorithm.

```python
def crossover(brain_1, brain_2) -> Bird:
    new_weights = copy.deepcopy(brain_1.weights)

    for i in range(len(brain_1.weights)):
        for j in range(len(brain_1.weights[i])):
            for k in range(len(brain_1.weights[i][j])):
                chosen_weights = random.choice([ brain_1.weights, brain_2.weights ])

                new_weights[i][j][k] = copy.deepcopy(chosen_weights[i][j][k])

    return Bird(0, "Crossover", NeuralNetwork([ 2, 6, 1 ], new_weights))

def spawn_new_generation(dead) -> list:
    brains = [ bird.brain for bird in dead ]
    next_gen = []

    for i in range(4):
        next_gen.append(Bird(0, "Copy of winner",  brains[-i]))

    next_gen.append(crossover(brains[-1], brains[-2]))

    for i in range(3):
        winners = [ brains[-1], brains[-2], brains[-3], brains[-4] ]
        winner_1 = random.choice(winners)
        winner_2 = random.choice(winners)

        next_gen.append(crossover(winner_1, winner_2))

    next_gen.append(Bird(0, "Random"))
    next_gen.append(Bird(0, "Random"))

    for i in range(10):
        next_gen[i].y = 25 + (50 * i)
        next_gen[i].set_image(bird_colors[i])

    return next_gen
```
## How it works
In each frame, each bird feeds the neural networks two parameters: the horizontal and the vertical distance from the closest pipe. Each bird then decides whether to jump or not based on the output of the Neural Network. If the ouput is larger or equal to 0.5, the bird jumps, otherwise not.

```python
def predict(self, closest_pipe):
        closest_pipe_horizontal_distance = closest_pipe.x + pipe_width - self.x
        closest_pipe_vertical_distance = self.y - closest_pipe.y

        self.brain.feed_forward([ closest_pipe_horizontal_distance, closest_pipe_vertical_distance ])
        
        output = self.brain.get_output_values()[0]

        if output >= 0.5:
            self.jump()
```

## Result
After running the game, the birds start to jump randomly, some dying at the very beginning, some passing a few pipes, but eventually, all of them dying soon. Then, a new generation is created, being much better that the last one. Letting the game run a few generations, few birds manage to play for minutes, even hours.