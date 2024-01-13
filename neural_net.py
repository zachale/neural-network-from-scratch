import math
import random
import json
from PIL import Image
import numpy as np

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

        self.b_gradient = []
        self.w_gradient = []


        for i in range(0,number_of_layers-1):
            self.biases.append([])
            self.weights.append([])
            self.b_gradient.append([])
            self.w_gradient.append([])
            for j in range (0,layers[i+1]):
                self.biases[i].append(1)
                self.weights[i].append([])
                self.b_gradient[i].append(1)
                self.w_gradient[i].append([])
                
                for k in range (0, layers[i]):
                    self.weights[i][j].append(1)
                    self.w_gradient[i][j].append(1)


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
            
            net.layers[v].nodes[w].value = float(activation(value))
    
    outcome = []    

    for y in net.layers[len(net.layers)-1].nodes:
        outcome.append(y.value)
    

    return outcome




#calculates the cost of the neural net given the dataset
def costFunction(net : net):
    cost = 0

    for x in dataset:
        result = calculate(net, [x[0]/dim,x[1]/dim])
        # print(x[2], result[0])
        cost += pow(abs(result[0]-x[2] ),2)
    return cost


#brute forcing the weights and biases, 
def brute(net : net):
    cost = 50000
    while cost > 0:
        generate(net)

        result = costFunction(net)

        if result < cost:

            w = net.weights
            b = net.biases           
            cost = result
            print (cost)
            image(net)
            net.save()
    
    f = open("dataset", "w")
    json.dump([w,b], f) 

def gradientDecent(net : net):

    learn_rate = 25
    h = 0.0001

    generate(net)

    cost = 10

    while True:
        cost = costFunction(net)
        print("working")
        for x in range(0,len(net.weights)):
            for y in range(0,len(net.weights[x])):
                for z in range(0,len(net.weights[x][y])):
                    net.weights[x][y][z] -= h

                    newCost = costFunction(net)

                    net.weights[x][y][z] += h
                    net.w_gradient[x][y][z] = (newCost - cost)*learn_rate

        for x in range(0, len(net.biases)):
            for y in range(0,len(net.biases[x])):
                    net.biases[x][y] -= h
                    newCost = costFunction(net)
                    net.biases[x][y] += h
                    net.b_gradient[x][y] = (newCost - cost)*learn_rate

        print("applying")
        image(net)
        apply_gradient(net)
        print(cost, net.biases)

        
#horribly innefficient, but it gets the job done
#I would prefer this to be a backwards propagation algorythm
#I will have to apply my mathematics minor to do that at a later date
def apply_gradient(net : net):


    for x in range(0,len(net.weights)):
        for y in range(0,len(net.weights[x])):
            for z in range(0,len(net.weights[x][y])):
                net.weights[x][y][z] += net.w_gradient[x][y][z]
    for x in range(0, len(net.biases)):
        for y in range(0,len(net.biases[x])):
            net.biases[x][y] += net.b_gradient[x][y]






    
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
    cost = costFunction(net)
    name = 'generated_images/images-' + image_number +".png"
    image_number += 1
    print(cost)

    im.save(name)

#generates random weights and biases for a network
def generate (net : net, net2 = net(2,10,5,1), rate = 0):
    for x in range(0,len(net.weights)):
        for y in range(0,len(net.weights[x])):
            for z in range(0,len(net.weights[x][y])):
                net.weights[x][y][z] = net2.weights[x][y][z] * ((random.random() *2) -1)
    for x in range(0, len(net.biases)):
        for y in range(0,len(net.biases[x])):
            net.biases[x][y] = net2.biases[x][y] * ((random.random() *2) -1)

def activation (value : int):
    
    #alternate activation function (sigmoid)
    # return  1/(1 + math.exp(-5*value))
    
    return  1/(1 + math.exp(-value))
    
    
    # if value > 0:
    #      return value
    # else:
    #       return 0


