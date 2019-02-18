# Beta distribution

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

asd1 = np.random.beta(2, 4, size = 1000)
asd2= [round(np.random.beta(2, 4), 1) + 0.1 for i in range(1000)]

fug = plt.figure(figsize = (10,5))
aux1 = fug.add_subplot(1,2,1)
aux1.hist(asd1, bins = 20)

aux2 = fug.add_subplot(1,2,2)
aux2.hist(asd2, bins = 10)

pd.DataFrame(asd2).to_excel('test beta distribution.xlsx')