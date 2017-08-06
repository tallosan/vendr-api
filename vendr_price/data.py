#
# Loads in a dataset, parses and shuffles it, then converts each element into
# a Theano shared variable.
# 
# We can also preprocess data with 'pre_process()'. Currently supports both
# zero-centering, and normalization.
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
        shuffle: Toggle to shuffle the dataset. Only really necessary on first run.
'''
def load_dataset(path='data/data.pkl', shuffle=False):
    
    # Unpickle the dataset, and shuffle it if specified.
    with open(path, 'rb') as fp:
        data = pickle.load(fp)

    if shuffle:
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

    # Split the data into training and validation sets. We'll use a 75-25% split.
    split_percentage = 0.75
    split            = int( len(x_values) * split_percentage )
    
    x_train, y_train = shared_dataset(x_values[:split], y_values[:split])
    x_val, y_val     = shared_dataset(x_values[split:], y_values[split:])

    return [ (x_train, y_train), (x_val, y_val) ]


''' Preprocesses dataset according to given specifications. N.B. -- It is
    crucial that any preprocessing statistics (e.g. mean) are computed on the
    training set only, then applied to the validation set.
    Args:
        data: A list of tuples, where each tuple contains the inputs and the
              corresponding labels.
'''
def pre_process(data, zero_center=True, normalize=True):
    
    x_train = data[0][0].eval()
    x_val   = data[1][0].eval()
    
    # Perform zero-centering via mean subtraction.
    if zero_center:
        tmean    = np.mean(x_train, axis=0)
        x_train -= tmean
        x_val   -= tmean
    
    # Normalize the data by dividing it by its standard deviation. Note, we can
    # only perform this operation if the data is already zero-centered.
    if zero_center and normalize:
        std_dev  = np.std(x_train, axis=0)
        x_train /= std_dev
        x_val   /= std_dev
    
    # Set labels accordingly. No preprocessing necessary.
    y_train, y_val = data[0][1], data[1][1]
    
    return [ (x_train, y_train), (x_val, y_val) ]

