<<<<<<< HEAD
'''
main module
'''
import snake
from snake import Snake
import genetic_neural_network
from genetic_neural_network import GeneticNeuralNetwork

gnn = GeneticNeuralNetwork(inodes=24, hnodes=[16, 8], onodes=4, activation='relu', eta=0.01)
boa = Snake(gnn)
=======
'''
main module
'''
import snake
from snake import Snake
import genetic_neural_network
from genetic_neural_network import GeneticNeuralNetwork

gnn = GeneticNeuralNetwork(inodes=24, hnodes=[16, 8], onodes=4, activation='relu', eta=0.01)
boa = Snake(gnn)
>>>>>>> ff35870c235c677bd6e367cfedf2974cac4a6e8a
boa.play()