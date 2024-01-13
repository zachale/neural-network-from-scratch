import neural_net as n;


#initialize the network
network = n.net(2,10,3,1)
 
# n.brute(network) # This function uses a random generator to try and brute force the data set (INCREDIBLY INEFFICIENT)

n.gradientDecent(network) # This function uses a gradient descent algorithm to learn the pattern of the data set slowly (INEFFICIENT)

# ToDo: backwards propagation #  # This function uses a backwards propagation algorithm to learn the pattern of the data set (GOOD)