#
#   Neural Net.
#
# ==============================================================================

import numpy as np

import theano
import theano.tensor as T

import lasagne as nnet

import data


class KNet(object):

    ''' We'll start off using a simple architecture.
        arch 0: IN --> L0 --> OUT
        arch 1: IN --> L0 --> D0 --> L1 --> D1 --> OUT
    '''
    def __init__(self, inpt_shape):

        self.inpt = T.dmatrix('inpt')
        self.out  = T.dmatrix('out')

        self.network_in = nnet.layers.InputLayer(shape=inpt_shape, input_var=self.inpt)
        self.l0         = nnet.layers.DenseLayer(self.network_in, num_units=100,
                            nonlinearity=nnet.nonlinearities.tanh
        )
        self.l1         = nnet.layers.DenseLayer(self.l0, num_units=50,
                            nonlinearity=nnet.nonlinearities.tanh)
        self.network    = nnet.layers.DenseLayer(self.l0, num_units=1,
                            nonlinearity=nnet.nonlinearities.linear
        )

    ''' Train the network given a dataset, and a series of hyperparameters.
        Args:
            dataset: The dataset to train on, in a dict. e.g. -- { train: (xs, ys) }
            epochs: The number of epochs to train for.
            batch_size: The size of each batch.
            eta: The learning rate.
            rho: The momentum rate.
            verbose: Toggle for debug feedback.
    '''
    def train(self, dataset, epochs, batch_size, eta, rho,
                    drop_input=0.2, drop_hidden=0.5, verbose=False):
        
        # Unpack the dataset, and determine the number of batches.
        x_train, y_train = dataset['training']
        x_val, y_val     = dataset['validation']
        
        # TODO: This changes the dataset.
        x_train = x_train[:2]
        y_train = y_train[:2]
        x_val = x_val[:2]
        y_val = y_val[:2]

        n_train_batches = x_train.shape.eval()[0] / batch_size
        n_val_batches   = x_val.shape.eval()[0] / batch_size
        
        # Cost expression. We'll use the squared error here.
        pred = nnet.layers.get_output(self.network)
        loss = nnet.objectives.squared_error(pred, self.out)
        loss = loss.mean()

        # Update rule. We'll use Nesterov momentum to speed things up.
        params  = nnet.layers.get_all_params(self.network, trainable=True)
        updates = nnet.updates.nesterov_momentum(loss, params,
                    learning_rate=eta, momentum=rho)

        # Validation cost expression.
        val_pred = nnet.layers.get_output(self.network, deterministic=True)
        val_loss = nnet.objectives.squared_error(val_pred, self.out)
        val_loss = val_loss.mean()

        # Define two symbolic functions -- one for training, and one for validation.
        train_model = theano.function(
                        [self.inpt, self.out], loss, updates=updates
        )
        val_model   = theano.function(
                        [self.inpt, self.out], val_loss
        )

        print 'beginning training ...\n'
        # Begin training.
        for epoch in xrange(epochs):
           
            # Train the model.
            train_error, train_batches = 0, 0
            for batch_index in xrange(n_train_batches):
                xs = x_train[batch_index * batch_size: (batch_index + 1) * batch_size]
                ys = y_train[batch_index * batch_size: (batch_index + 1) * batch_size]
                
                # Reshape the label data, so that our NNet can use it.
                ys = np.reshape(ys.eval(), ys.eval().shape + (1,))
                
                train_error += train_model(xs.eval(), ys)
                train_batches += 1
            
            # Validate the model.
            val_error, val_batches = 0, 0
            for batch_index in xrange(n_val_batches):
                xs = x_val[batch_index * batch_size: (batch_index + 1) * batch_size]
                ys = y_val[batch_index * batch_size: (batch_index + 1) * batch_size]
                
                # Reshape the label data, so that our NNet can use it.
                ys = np.reshape(ys.eval(), ys.eval().shape + (1,))
                
                val_error += val_model(xs.eval(), ys)
                val_batches += 1

            # Print feedback from the training.
            if verbose:
                print '# ======================================================='
                print 'epoch: ', epoch, ' of ', epochs
                print 'training error: ', (train_error / train_batches)
                print 'validation error: ', (val_error / val_batches)


# ==============================================================================
# Create the network and train it.
#
dataset = data.load_dataset()
network_in = {
                'training': dataset[0],
                'validation': dataset[1]
}

# Hyperparameters:
#
EPOCHS      = 2000
BATCH_SIZE  = 2
ETA         = 0.0001
RHO         = 0.9
VERBOSE     = True

inpt_shape = (BATCH_SIZE, 3)

knet = KNet(inpt_shape=inpt_shape)
knet.train(dataset=network_in, epochs=EPOCHS, batch_size=BATCH_SIZE,
           eta=ETA, rho=RHO, verbose=True)


