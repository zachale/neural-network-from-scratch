import math
import random
import json
import os
from PIL import Image
import numpy as np
import time

number_of_layers = 4
image_number = 0
dataset = json.load(open("data/data_set.json"))
weights_biases = open("data/weights_biases.json", 'r+')
img = Image.open("base_pattern.png")
dim = img.size[0]

class net:

    def __init__(self, x, y, z, a) -> None: 
        self.layer1 = layer(x)
        self.layer2 = layer(y)
        self.layer3 = layer(z)
        self.layer4 = layer(a)
        self.layers = [self.layer1, self.layer2, self.layer3,self.layer4]
        layers = [x,y,z,a]

        


        self.biases = []
        self.weights = []


        for i in range(0,number_of_layers-1):
            self.biases.append([])
            self.weights.append([])
            for j in range (0,layers[i+1]):
                self.biases[i].append(1)
                self.weights[i].append([])
                
                for k in range (0, layers[i]):
                    self.weights[i][j].append(1)


    #function to save the  current weights and biases
    def save(self):
        f = weights_biases
        json.dump([self.weights, self.biases], f)

    #function to load weights and biases from a file
    def load(self):
        if weights_biases:
            
            f = weights_biases

            d = json.load(f)

            self.weights = d[1]
            self.biases = d[0]
        else:
            print("no dataset found!")



class layer:
    def __init__(self,z) -> None:
         self.nodes = []

        #append as many nodes are needed for this layer
         for i in range(0, z):
              self.nodes.append(node())

class node:
    def __init__(self) -> None:
         self.value = 0


#forward propagation algorithim
def calculate(net:net, value : list):

    for w in range(0,len(net.layer1.nodes)):
            net.layer1.nodes[w].value = value[w]


    #cycles through all of the layers ignoring the first
    for v in range(1,number_of_layers):
        #cycles through all of the nodes in the selected layer
        for w in range(0, len(net.layers[v].nodes)):
            value = 0
            for x in range(0, len(net.layers[v-1].nodes)):
                value = value + (net.layers[v-1].nodes[x].value * net.weights[v-1][w][x])
            value += net.biases[v-1][w]
            
            net.layers[v].nodes[w].value = activation(value)
    
    outcome = []    

    for y in net.layers[len(net.layers)-1].nodes:
        outcome.append(y.value)
    

    return outcome




#calculates the cost of the neural net given the dataset
def test(net : net):
    cost = 0

    for x in dataset:
        result = calculate(net, [x[0]/dim,x[1]/dim])
        # print(x[2], result[0])
        cost += pow(abs(x[2] - result[0]),2)
    return cost

#brute forcing the weights and biases, 
def brute(net : net):
    cost = 50000
    while cost > 0:
        generate(net)

        result = test(net)

        if result < cost:

            w = net.weights
            b = net.biases           
            cost = result
            print (cost)
            image(net)
            net.save()
    
    f = open("dataset", "w")
    json.dump([w,b], f) 
    
#generates a graphic based on the current network
def image (net : net):
    result = []
    for i in range(0,dim):
        result.append([])
        for x in range(0,dim):
            result[i].append([])
            result[i][x] = [calculate(net,[x/dim,i/dim])[0] * 255]
            result[i][x].append(0)
            result[i][x].append(0)
    
    im = Image.fromarray(np.uint8(result))

    im.save('generated_images/' + str(test(net))+".png")

#generates random weights and biases for a network
def generate (net : net, net2 = net(2,10,5,1), rate = 0):
    for x in range(0,len(net.weights)):
        for y in range(0,len(net.weights[x])):
            for z in range(0,len(net.weights[x][y])):
                net.weights[x][y][z] = net2.weights[x][y][z] * ((random.random() *2) -1)
    for x in range(0, len(net.biases)):
        for y in range(0,len(net.biases[x])):
            net.biases[x][y] = net2.biases[x][y] * ((random.random() *2) -1)


#uses a simulated evolution where the top two nets with the lowest cost reproduce
#NOT WORKING
def evolve (nets, size : int, rate = 1):
    cost = 500000
    best = net(2,10,5,1)
    best2 = net(2,10,5,1)

    generation = []
    while cost > 0:
        generation = []
        for x in range(0,size):
            
            network = net(2,10,5,1)
            generate(network, nets, rate)
            price = test(network)

            if price < cost:
                cost = price
                best2 = best
                best = network
        
        network = best
        network2 = best2

        print(cost)

        for w in range(0,len(network.layers)):
            for x in range(0,len(network.layers[w].nodes)):
                nets.layers[w].nodes[x].value = network.layers[w].nodes[x].value + network2.layers[w].nodes[x].value
            
        for x in range(0,len(nets.weights)):
            for y in range(0,len(nets.weights[x])):
                for z in range(0,len(nets.weights[x][y])):
                    nets.weights[x][y][z] = (network.weights[x][y][z] + network2.weights[x][y][z]) / 2
        for x in range(0, len(nets.biases)):
            for y in range(0,len(nets.biases[x])):
                nets.biases[x][y] = (network.biases[x][y] + network2.biases[x][y]) / 2
        
        image(network)
        image(network2)
        image(nets)


def activation (value : int):
    
    #alternate activation function (sigmoid)
    #return  1/(1 + math.exp(-5*value))
    
    
    
    if value > 0:
         return 1
    else:
         return 0



