#Default function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''a = []
for i in np.power(list(map(int, list(str(2) * 20))), np.arange(0.01, 0.21, 0.01)):
#for i in np.exp(np.arange(0.01, 0.21, 0.01)):
#for i in np.power(np.full((20, 1), 2), np.arange(0.01, 0.21, 0.01)):
    for j in np.arange(0.01, 1.01, 0.01):
        a.append(i*(1+j))
a = np.array(a)

b = []
#for i in np.power(list(map(int, list(str(2) * 20))), np.arange(0.01, 0.21, 0.01)):
for i in np.exp(np.arange(0.01, 0.21, 0.01)):
#for i in np.power(np.full((20, 1), 2), np.arange(0.01, 0.21, 0.01)):
    for j in np.arange(0.01, 1.01, 0.01):
        b.append(i*(1+j))
b = np.array(b)'''

a = []
for i in np.power(list(map(int, list(str(2) * 20))), np.arange(0.01, 0.21, 0.01)):
#for i in np.exp(np.arange(0.01, 0.21, 0.01)):
#for i in np.power(np.full((20, 1), 2), np.arange(0.01, 0.21, 0.01)):
    for j in np.arange(0.01, 1.01, 0.01):
        a.append(i*(j))
a = np.array(a)

b = []
#for i in np.power(list(map(int, list(str(2) * 20))), np.arange(0.01, 0.21, 0.01)):
for i in np.exp(np.arange(0.01, 0.21, 0.01)):
#for i in np.power(np.full((20, 1), 2), np.arange(0.01, 0.21, 0.01)):
    for j in np.arange(0.01, 1.01, 0.01):
        b.append(i*(j))
b = np.array(b)

pic = plt.figure(figsize = (15, 5))
graph1 = pic.add_subplot(1,1,1)
#graph2 = pic.add_subplot(1,2,2)
graph1.plot(a)
graph1.plot(b)
graph1.plot(list(map(int, list(str(2) * len(a)))), linestyle="-", color = "r")
graph1.plot(list(map(int, list(str(1) * len(a)))), linestyle="-", color = "g")

#np.power(list(map(int, list(str(2) * 20))), np.arange(0.01, 0.21, 0.01))

finalset = pd.DataFrame(a.reshape(20, 100))
finalset.T.to_excel('default_function - research - done.xlsx')

