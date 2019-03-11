#External environment

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.arange(0, 201)
df = pd.DataFrame(columns = ['Y', 'X'])
for i in x:
    df.loc[i] = [round((30 + 15 * np.sin(i / 5) + i) * (1 + np.random.randn()/10)), i]

figura = plt.figure(figsize=(15, 7))
sub1 = figura.add_subplot(1,1,1)
sub1.plot(df['Y'], marker = 'o', color = 'red')
