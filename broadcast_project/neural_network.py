import numpy as np

def neural_network_bias():

    # 10 samples with 5 features
    x = np.random.rand(10,5)

    # bias for each neuron
    bias = np.array([1,2,3,4,5])

    output = x + bias

    print("Input Matrix Shape:", x.shape)
    print("Bias:", bias)
    print("Output After Broadcasting:\n", output)
    
neural_network_bias()