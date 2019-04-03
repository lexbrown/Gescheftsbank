# loan pivot

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#dataset = pd.read_excel('Full_portfolio.xlsx')
dataset = pd.read_csv('loan_database.csv')
dataset['Duration'] = dataset['EndDate'] - dataset['BeginDate']
for i in range(len(dataset)):
    if dataset.loc[i, 'PD'] < 0.06:
        dataset.loc[i, 'Riskiness'] = 'Low risk'
    elif dataset.loc[i, 'PD'] < 0.16 and dataset.loc[i, 'PD'] >= 0.06:
        dataset.loc[i, 'Riskiness'] = 'Medium risk'
    else:
        dataset.loc[i, 'Riskiness'] = 'High risk'
loanpivot = pd.pivot_table(dataset, index = 'Duration', 
                           values = 'Interest rate', columns = 'Riskiness', aggfunc = np.mean)
print(loanpivot)
#print(dataset[['ClientId', 'BeginDate', 'EndDate', 'Duration']])
#dataset.to_excel('sss.xlsx')
