import neural_net as n;



network = n.net(2,5,3,1)
 
# n.brute(network)

n.gradientDecent(network)