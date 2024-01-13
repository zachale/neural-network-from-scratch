### Why did I build this?

I created this neural network to dip my toes into machine learning algorithms.

I have always found machine learning fascinating and this project has made me appreciate it more

### The Fundamentals

This neural network can be used to learn data sets of 2 dimensions input, one dimension output.
So if your data set say has 2 different properties that need to map to a binary yes/no decision, this will work!
This is a little bit limiting, but the hidden layers can be any size and can be scaled to be able to learn on complex data sets.

This script creates a grayscale visualization at each learning step, so you can compare it to the base image and see how much more it needs to learn!

### Instructions

Change the base png to a *square* image of any size! (preferably 50px width or smaller)
run the image to data set script
finally, run main.py!

This script will run until keyboard interupt (ie ```ctrl^c``` on windows)

In main.py you can different functionality that the neural netowork has. 

have fun!

**you may observe some flickering in the image, this is the neural netowork settling down at a saddle point.**
**just give the network some time and it will figure its way out**

### WishList: ToDo

- implement a backwards propagation algorithm
- allow for input/output layers of any size
- implement parallel processing