<<<<<<< HEAD
import numpy as np
import scipy

class GeneticNeuralNetwork():

    def __init__(self, inodes, hnodes, onodes=4, activation='relu', eta=0.01,
                 classifier={'activation' : 'softmax'}):
        '''
        inodes : int
        hnodes : list (the number of each ith hidden nodes)
        onodes : int (default 4)
        activation : string
        eta : float (learning rate)
        classifier : dict
        '''
        assert type(inodes) is int, 'inodes must be int type'
        assert type(hnodes) is list and ([True] * len(hnodes) == [type(val) is int for val in hnodes]),\
               'hnodes must be list of integer'
        assert type(onodes) is int, 'onodes must be int type'
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes
        self.eta = eta
        self.weight = np.array([], dtype=np.float64)

        if activation=='relu':
            self.activation = lambda x: np.maximum(0, x)
        elif activation=='sigmoid':
            self.activation = lambda x: scipy.special.expit(x)
        else :
            assert False, 'invalid activation'
        
        if classifier['activation'] == 'softmax':
            self.activation_clf = lambda x: scipy.special.softmax(x)
        else:
            self.activation_clf = self.activation

    def compile(self):
        pass
    
    def fit(self):
        pass

    def predict(self):
        pass
    
    def crossover(self):
        pass
    
    def mutation(self):
        pass
    
=======
import numpy as np
import scipy

class GeneticNeuralNetwork():

    def __init__(self, inodes, hnodes, onodes=4, activation='relu', eta=0.01,
                 classifier={'activation' : 'softmax'}):
        '''
        inodes : int
        hnodes : list (the number of each ith hidden nodes)
        onodes : int (default 4)
        activation : string
        eta : float (learning rate)
        classifier : dict
        '''
        assert type(inodes) is int, 'inodes must be int type'
        assert type(hnodes) is list and ([True] * len(hnodes) == [type(val) is int for val in hnodes]),\
               'hnodes must be list of integer'
        assert type(onodes) is int, 'onodes must be int type'
        self.inodes = inodes
        self.hnodes = hnodes
        self.onodes = onodes
        self.eta = eta
        self.weight = np.array([], dtype=np.float64)

        if activation=='relu':
            self.activation = lambda x: np.maximum(0, x)
        elif activation=='sigmoid':
            self.activation = lambda x: scipy.special.expit(x)
        else :
            assert False, 'invalid activation'
        
        if classifier['activation'] == 'softmax':
            self.activation_clf = lambda x: scipy.special.softmax(x)
        else:
            self.activation_clf = self.activation

    def compile(self):
        pass
    
    def fit(self):
        pass

    def predict(self):
        pass
    
    def crossover(self):
        pass
    
    def mutation(self):
        pass
    
>>>>>>> ff35870c235c677bd6e367cfedf2974cac4a6e8a
