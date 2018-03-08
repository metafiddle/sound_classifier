import h5py
import numpy as np
import tensorflow as tf
import math
import glob
from sklearn.model_selection import train_test_split

def load_features():
    filelist = glob.glob('features_mel_spectrograms/*.npy')
    labels = []
    data = []

    for file in filelist:
        nfile = np.load(file)
        if 'cat' in file:
            label = 0 #'cat'
        else:
            label = 1 #'dog'
        crop = int(nfile.shape[1] / 28)
        for i in range(crop):
            labels.append(label)
            data.append(nfile[:,i*28:(i+1)*28])

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.1, random_state=59)
    # return X_train, X_test, y_train, y_test
    return np.array(X_train, dtype=np.float32), np.array(X_test, dtype=np.float32), np.array(y_train), np.array(y_test)

def random_mini_batches(X, Y, mini_batch_size = 64, seed = 0):
    m = X.shape[0]
    mini_batches = []
    np.random.seed(seed)

    # Step 1: Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[permutation,:,:]
    shuffled_Y = Y[permutation].reshape((Y.shape[0],1))

    # Step 2: Partition (shuffled_X, shuffled_Y). Minus the end case.
    num_complete_minibatches = math.floor(m/mini_batch_size) # number of mini batches of size mini_batch_size in your partitionning
    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[k * mini_batch_size : k * mini_batch_size + mini_batch_size,:,:]
        mini_batch_Y = shuffled_Y[k * mini_batch_size : k * mini_batch_size + mini_batch_size, :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[num_complete_minibatches * mini_batch_size : m, :,:]
        mini_batch_Y = shuffled_Y[num_complete_minibatches * mini_batch_size : m, :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches