r"""
This is going to be a Neural Network with 1 hiddep layer consisting of a specified number of neurons.

So there is going to be needed a Matrix with the size of the number of inputs and hidden layer one.

For example if we have 3 inputs and a number of 5 hidden layer neurons: 

$\begin{bmatrix} i_1, i_2, i_3 \end{bmatrix} \\
    * \begin{bmatrix} [h_1, h_2, h_3], [h_4, h_5, h_6], [h_7, h_8, h_9] \end{bmatrix} \\
        = \begin{bmatrix} o_1, o_2, o_3, o_4, o_5 \end{bmatrix}$

Also there is added a bias on every layer except the input layer:

$\begin{bmatrix} o_1, o_2, o_3, o_4, o_5 \end{bmatrix} \\
        + \begin{bmatrix} b_1, b_2, b_3, b_4, b_5 \end{bmatrix}$

After that the values of the neurons are send through an activation function (currently the sigmoid function: $x = \frac{1}{1 + \exp{-x}}$).

So we need 2 matrices that have the size of:

1. number of inputs x number of hidden layer neurons
2. number of hidden layer neurons x number of outputs

And two vectors that have the size of:

1. number of hidden layer neurons
2. number of output neurons

To learn the NN gets another NN and creates a slightly different version of that inputted NN.

"""

import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
__docformat__ = "google"

import numpy as np
import random
import numba

@numba.njit
def sigmoid(x: int):
    """
    The sigmoid function

    Args:
        x (int): The x input

    """
    x = 1 / (1 + np.exp(-x))
    return x


def random_negative_positive(x: int):
    """
    Return the input random negative of positive.

    Args:
        x (int): The input

    """
    return x * random.randint(-1, 1)

class Neural_Net:
    def __init__(self, input_count, output_count, hidden_layer_count=5, learning_rate: int = 300):
        """
        Create Neural Network width 2 Hidden layers.

        Args:
            self (undefined):
            input_count (undefined): The number of inputs.
            output_count (undefined): The number of outputs.
            learning_rate (int = 500): The higher the more the NN learns from another given NN.

        """

        self.learning_rate = 1 / learning_rate
        self.output_count = output_count
        self.input_count = input_count
        self.hidden_layer_count = hidden_layer_count

        self.weights_input_hidden = np.random.rand(
            input_count, self.hidden_layer_count)

        self.weights_hidden_output = np.random.rand(
            self.hidden_layer_count, output_count)

        self.bias_hidden = np.random.rand(1, self.hidden_layer_count)
        self.bias_output = np.random.rand(1, self.output_count)

        self.activation_function = sigmoid

    def calc_outputs(self, inputs: list) -> list:
        """
        Calculate the layers of the Neural Network and give an output.

        Args:
            self (undefined):
            inputs (list): The list of inputs.

        Returns:
            list

        """

        hidden = np.matmul(inputs, self.weights_input_hidden)
        hidden = hidden + self.bias_hidden
        hidden = self.activation_function(hidden)

        output = np.matmul(hidden, self.weights_hidden_output)
        output = output + self.bias_output
        output = self.activation_function(output)

        return output.tolist()[0]

    def adapting(self, NN_to_adapt):
        """
        Adapt the hidden layers from another bird, but slightly different.

        Args:
            self (undefined):
            NN_to_adapt (Neural_Net): The Neural Net to adapt to.

        TODO: Maybe compare the inputted NN decisions with the one this NN made to compare them and the learn from them.

        """

        adapt_rate_weights_input_hidden = random_negative_positive(
            np.random.rand(self.input_count, self.hidden_layer_count))
        self.weights_input_hidden = NN_to_adapt.weights_input_hidden + \
            adapt_rate_weights_input_hidden * self.learning_rate

        adapt_rate_weights_hidden_output = random_negative_positive(
            np.random.rand(self.hidden_layer_count, self.output_count))
        self.weights_hidden_output = NN_to_adapt.weights_hidden_output + \
            adapt_rate_weights_hidden_output * self.learning_rate

        adapt_rate_bias_hidden = random_negative_positive(
            np.random.rand(1, self.hidden_layer_count))
        self.bias_hidden = NN_to_adapt.bias_hidden + \
            adapt_rate_bias_hidden * self.learning_rate

        adapt_rate_bias_output = random_negative_positive(
            np.random.rand(1, self.output_count))
        self.bias_output = NN_to_adapt.bias_output + \
            adapt_rate_bias_output * self.learning_rate
