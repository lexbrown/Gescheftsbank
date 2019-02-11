# New panel

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rawdata = pd.read_excel('raw_set.xlsx')
new_pivot  = pd.pivot_table(rawdata, values='Total sum', 
                            index = 'Company', columns = 'Oil', aggfunc = np.sum)
new_pivot.to_excel('new_pivot.xlsx')