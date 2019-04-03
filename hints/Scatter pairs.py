# scatter plots

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

scatterset = pd.read_excel('model final.xlsx')

pd.plotting.scatter_matrix(scatterset, alpha = 1, s = 60,figsize = (16,16), diagonal = 'kde')
