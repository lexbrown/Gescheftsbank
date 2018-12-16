#MVP Stage1 - 3-6-3

import numpy as np
import pandas as pd
import matplotlib as mpl

capital = 100000
liabilities = 0
placcount = 0
appsperday = 100 #число заявок в день
assets = capital + liabilities
while wotw != "exit": #wotw - это что?
	for i in range(5): #цикл - 5 рабочих дней
		for app in range(appsperday):
