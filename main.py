import neural_net as n;



network = n.net(2,10,3,1)
 
# n.brute(network)

n.gradientDecent(network)