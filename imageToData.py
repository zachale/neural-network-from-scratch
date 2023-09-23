import math
import random
import numpy as np
from PIL import Image
import json


img = Image.open("base.png")
data = list(img.getdata())
dim = img.size[0]
print(len(data))


for x in data:
    x = list(x)


def calculate (list, data):
    return data[list[0] + (list[1] * dim)][0]
    


result = []
for i in range(0,dim):
    result.append([])
    for x in range(0,dim):
        result[i].append([])
        result[i][x] = [calculate([i,x],data) * 255]
        result[i][x].append(0)
        result[i][x].append(0)


coords = []

for z in range (0, int(dim*dim)):
    x = random.randint(0,dim-1)
    y = random.randint(0,dim-1)


    coords.append([x,y,calculate([x,y],data)/255])

f = open("set.txt", "w")
print(coords)
json.dump(np.ndarray.tolist(np.int32(coords)), f)    
