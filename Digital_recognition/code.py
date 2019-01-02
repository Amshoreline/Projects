import numpy as np
import matplotlib.pyplot as plt



def softmax(x):
    """
    Compute softmax function for input. 
    Use tricks from previous assignment to avoid overflow
    """
    ### YOUR CODE HERE
    # x is a numpy.ndarray
    size = x.shape[0]
    maxnum = x.max();
    s = np.zeros(size)
    denominator = sum(np.exp(x - maxnum))
    s = np.exp(x - maxnum) / denominator
    
    ### END YOUR CODE
    return s

def sigmoid(x):
    """
    Compute the sigmoid function for the input here.
    """
    ### YOUR CODE HERE
    s = 1.0 / (1 + np.exp(-x))
    ### END YOUR CODE
    return s

def forward_prop(data, labels, params):
    """
    return hidder layer, output(softmax) layer and loss
    """
    W1 = params['W1']
    b1 = params['b1']
    W2 = params['W2']
    b2 = params['b2']

    ### YOUR CODE HERE
    #print data.shape # 1000 * 784
    #print W1.shape   # 300 * 784
    #print b1.shape   # 300 * 1
    #print W2.shape   # 10 * 300
    #print b2.shape   # 10 * 1
    
    z_1 = np.matmul(data, np.transpose(W1)) + np.transpose(b1)
    a_1 = sigmoid(z_1)
    z_2 = np.matmul(a_1, np.transpose(W2)) + np.transpose(b2)
    h = [softmax(line) for line in z_2]
    y = h
    m = data.shape[0]
    cost = np.log(h)
    cost[np.isinf(cost)] = 0
    cost[np.isnan(cost)] = 0
    cost = sum(sum(labels * cost)) / (-m)
    ### END YOUR CODE
    return h, y, cost

def backward_prop(data, labels, params):
    """
    return gradient of parameters
    """
    W1 = params['W1']
    b1 = params['b1']
    W2 = params['W2']
    b2 = params['b2']

    ### YOUR CODE HERE
    #print data.shape # 1000 * 784
    #print W1.shape   # 300 * 784
    #print b1.shape   # 300 * 1
    #print W2.shape   # 10 * 300
    #print b2.shape   # 10 * 1
    
    z_1 = np.matmul(data, np.transpose(W1)) + np.transpose(b1)
    a_1 = sigmoid(z_1)
    z_2 = np.matmul(a_1, np.transpose(W2)) + np.transpose(b2)
    a_2 = [softmax(line) for line in z_2]
    
    m   = data.shape[0] # 1000
    n_1 = data.shape[1] # 784 
    n_2 = W1.shape[0]   # 300
    n_3 = W2.shape[0]   # 10
    
    U = np.sum(labels, axis=1)
    #print U.shape  # (1000L, )
    U.shape = (m, 1) # => (1000L, 1L)
    U = (labels - a_2 * U)
    
    lamb = 0.0001
    
    gradW2 = (-1.0 / m) * np.matmul(np.transpose(U), a_1) + lamb * W2
    gradb2 = np.sum(U, axis=0)
    gradb2.shape = (n_3, 1)
    gradb2 = (-1.0 / m) * gradb2
    
    V = np.matmul(U, W2) * a_1 * (1 - a_1)
    gradW1 = (-1.0 / m) * np.matmul(np.transpose(V), data) + lamb * W1
    gradb1 = np.sum(V, axis=0)
    gradb1.shape = (n_2, 1)
    gradb1 = (-1.0 / m) * gradb1
    
    #print gradW1.shape   # 300 * 784
    #print gradb1.shape   # 300 * 1
    #print gradW2.shape   # 10 * 300
    #print gradb2.shape   # 10 * 1
    ### END YOUR CODE

    grad = {}
    grad['W1'] = gradW1
    grad['W2'] = gradW2
    grad['b1'] = gradb1
    grad['b2'] = gradb2

    return grad

def nn_train(trainData, trainLabels, devData, devLabels):
    (m, n) = trainData.shape
    num_hidden = 300
    learning_rate = 5
    params = {}

    ### YOUR CODE HERE
    params['W1'] = np.random.random((num_hidden, n))
    params['b1'] = np.random.random((num_hidden, 1))
    params['W2'] = np.random.random((10, num_hidden))
    params['b2'] = np.random.random((10, 1))
    maxIteration = 200
    
    B = 1000
    epochs = m / B
    print "epochs = ", epochs
    for i in range(epochs):
        preCost = -100
        print "Epoch :", i + 1
        for j in range(maxIteration):
            h, y, cost = forward_prop(trainData[B * i : B * (i + 1), :], \
                                      trainLabels[B * i : B * (i + 1), :], params)
            #print "Current cost is :", cost
            if (preCost - cost < 0.00001) & (cost - preCost < 0.00001):
                break
            preCost = cost
            grad = backward_prop(trainData[B * i : B * (i + 1), :], \
                                      trainLabels[B * i : B * (i + 1), :], params)
            params['W1'] = params['W1'] - learning_rate * grad['W1'] 
            params['b1'] = params['b1'] - learning_rate * grad['b1'] 
            params['W2'] = params['W2'] - learning_rate * grad['W2'] 
            params['b2'] = params['b2'] - learning_rate * grad['b2'] 
        
    ### END YOUR CODE

    return params

def nn_test(data, labels, params):
    h, output, cost = forward_prop(data, labels, params)
    accuracy = compute_accuracy(output, labels)
    return accuracy

def compute_accuracy(output, labels):
    accuracy = (np.argmax(output,axis=1) == np.argmax(labels,axis=1)).sum() * 1. / labels.shape[0]
    return accuracy

def one_hot_labels(labels):
    one_hot_labels = np.zeros((labels.size, 10))
    one_hot_labels[np.arange(labels.size),labels.astype(int)] = 1
    return one_hot_labels

def main():
    np.random.seed(100)
    trainData, trainLabels = readData('images_train.csv', 'labels_train.csv')
    trainLabels = one_hot_labels(trainingLabels)
    p = np.random.permutation(60000)
    trainData = trainingData[p,:]
    trainLabels = trainLabels[p,:]

    devData = trainData[0:10000,:]
    devLabels = trainLabels[0:10000,:]
    trainData = trainData[10000:,:]
    trainLabels = trainLabels[10000:,:]

    mean = np.mean(trainData)
    std = np.std(trainData)
    trainData = (trainData - mean) / std
    devData = (devData - mean) / std

    testData, testLabels = readData('images_test.csv', 'labels_test.csv')
    testLabels = one_hot_labels(testingLabels)
    testData = (testingData - mean) / std
    
    params = nn_train(trainData, trainLabels, devData, devLabels)


    readyForTesting = True
    if readyForTesting:
        accuracy = nn_test(testData, testLabels, params)
    print 'Test accuracy: %f' % accuracy

if __name__ == '__main__':
    main()
