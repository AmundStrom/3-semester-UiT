import numpy as np

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Flatten

import matplotlib.pyplot as plt

from keras.layers import Conv2D, Dropout, MaxPooling2D
from keras.datasets import fashion_mnist, mnist

from keras import backend

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

n_classes = y_train.shape[1]