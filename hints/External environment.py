#External environment

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.arange(0, 101)
df = pd.DataFrame(columns = ['Y', 'X'])
for i in x:
    df.loc[i] = [round((10 + 15 * np.sin(i / 5) + i) * (1 + np.random.randn()/5)), i]

#y = (10 + 15 * np.sin(x / 5) + x) #* np.random.rand(100) #+ random.choice(range(111))
#z = [(10 + 15 * np.sin(x / 5) + x) for i in range(1) ]

figura = plt.figure(figsize=(15, 7))
sub1 = figura.add_subplot(1,1,1)
sub1.plot(df.Y)
