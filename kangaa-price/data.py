#
# Loads in a dataset, parses and shuffles it, then converts each element into
# a Theano shared variable.
# 
# The main function here is 'load_dataset()'.
#
# ==========================================================================

import cPickle as pickle
import numpy as np

import theano
import theano.tensor as T


''' Load in a dataset from the given file. The data should be a pickled numpy
    array, containing tuples in the format (x_values, y_value).
    Args:
        path: The name of the data file.
'''
def load_dataset(path='../data.pkl'):
    
    # Unpickle the dataset, and shuffle it.
    with open(path, 'rb') as fp:
        data = pickle.load(fp)

    import random
    random.shuffle(data)

    # Unpack the data values.
    x_values, y_values = zip(*data)
    
    ''' (Helper Function) Converts the x & y values into Theano shared variables.
        Args:
            data_x: A list of 1-d numpy ararys.
            data_y: A list of the corresponding price labels.
    '''
    def shared_dataset(data_x, data_y):

        shared_x = theano.shared(np.asarray(data_x, dtype=theano.config.floatX),
                    borrow=True)
        shared_y = theano.shared(np.asarray(data_y, dtype=theano.config.floatX),
                    borrow=True)

        return shared_x, T.cast(shared_y, 'float64')

    # Split the data into training and validation sets. We'll use a 75-25% slit.
    x_train, y_train = shared_dataset(x_values[:], y_values[:])
    x_val, y_val     = shared_dataset(x_values[:], y_values[:])

    return [ (x_train, y_train), (x_val, y_val) ]

