import math
import random
import numpy as np
from PIL import Image
import json



def calculate (list):
    # if list[1] > 200 * math.acos(list[0]/500):
    #     return 1
    # else:
    #     return 0

    if list[1] > -1 * pow(((list[0]/10)-25),2) + 400:
        return 1
    else:
        return 0

    # if list[1] > list[0] and list[1] < list[0] + 50:
    #     return 1
    # else:
    #     return 0
    


result = []
for i in range(0,5):
    result.append([])
    for x in range(0,5):
        result[i].append([])

        result[i][x] = [calculate([i,x]) * 255]
        result[i][x].append(0)
        result[i][x].append(0)

im = Image.fromarray(np.uint8(result))
# im.show()
im.save("base_pattern.png")


coords = []

for z in range (1, 100):
    x = random.randint(1,5)
    y = random.randint(1,5)

    
    coords.append([x,y,calculate([x,y])])
f = open("set.txt", "w")
json.dump(coords, f) 
print(coords)