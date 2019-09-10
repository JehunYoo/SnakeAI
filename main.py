'''
main module
'''
import snake
from snake import Snake
import genetic_neural_network
from genetic_neural_network import GeneticNeuralNetwork

gnn = GeneticNeuralNetwork(inodes=24, hnodes=[16, 8], onodes=4, activation='relu', eta=0.01)
boa = Snake(gnn)
boa.play()