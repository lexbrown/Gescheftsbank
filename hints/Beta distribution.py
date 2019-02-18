# Beta distribution

import numpy as np
import matplotlib.pyplot as plt

asd = np.random.beta(2, 4, size = 1000)

fug = plt.figure(figsize = (5,5))
aux = fug.add_subplot(1,1,1)
aux.hist(asd, bins = 20)