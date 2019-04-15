# Classifier

import numpy as np
import pandas as pd

'''
n = int(input('Введи возраст: '))
k = input('Введи тип кредита: ')
l = input('Введи образование: ')
'''


#классификаторы
age_classifier = pd.DataFrame([[range(18, 22), 2],
                                [range(22, 26), 3],
                                [range(26, 31), 4],
                                [range(31, 37), 5],
                                [range(37, 46), 5],
                                [range(46, 56), 4],
                                [range(56, 66), 2]], columns = ['Age', 'Mark'])
apptype_classifier = pd.DataFrame([['Card', 0],
                                   ['Consumer loan', 1],
                                   ['Car loan', 2],
                                   ['Mortgage', 3],
                                   ['SP loan', 1]], columns = ['AppType', 'Mark'])
edu_classifier = pd.DataFrame([['Secondary', 0],
                               ['High school', 1],
                               ['ComCollege', 2],
                               ['Bachelor', 3],
                               ['Master', 4],
                               ['PhD', 5],
                               ['MBA', 5]], columns = ['EduType', 'Mark'])
job_classifier = pd.DataFrame([['Unemployed', -5],
                               ['LowGrade', 1],
                               ['BlueCollar', 2],
                               ['Self-employed', 2],
                               ['WhiteCollar', 4],
                               ['MidMan', 5],
                               ['TopMan', 7]], columns = ['Job', 'Mark'])
experience_classifier = pd.DataFrame([[range(1), 0],
                                    [np.arange(0.25, 3.25, 0.25), 1],
                                    [range(4, 8), 2],
                                    [range(8, 16), 3],
                                    [range(16, 21), 4],
                                    [range(21, 100), 5]], columns = ['Experience', 'Mark'])
income_classifier = pd.DataFrame([[range(10000, 30000, 5000), 1],
                                [range(30000, 50000, 5000), 2],
                                [range(50000, 80000, 5000), 3],
                                [range(80000, 300000, 5000), 4],
                                [range(300000, 500000, 5000), 5],
                                [range(500000, 1000000, 5000), 6],
                                [range(1000000, 3005000, 5000), 7]], columns = ['Income', 'Mark'])
ois_classifier = pd.DataFrame([[range(1), 0], #other income sources
                                [range(1000, 11000, 1000), 1],
                                [range(11000, 51000, 1000), 2],
                                [range(51000, 1000000, 1000), 3]], columns = ['OIS', 'Mark'])
brb_classifier = pd.DataFrame([[range(1), 3], #burden rate before
                                    [np.arange(0.05, 0.3, 0.05), 2],
                                    [np.arange(0.3, 1.05, 0.05), 1],
                                    [np.arange(1.05, 3.05, 0.05), 0],
                                    [np.arange(3.05, 10, 0.05), -3]], columns = ['BRB', 'Mark'])
possessions_classifier = pd.DataFrame([['-', 0],
                                       ['Poor', 1],
                                       ['Middle', 2],
                                       ['Good', 3]], columns = ['PosQuality', 'Mark'])
credithistory_classifier = pd.DataFrame([['-', 0],
                                       ['Poor', -3],
                                       ['Middle', 1],
                                       ['Good', 3]], columns = ['CredHist', 'Mark'])
appsum_classifier = pd.DataFrame([[range(100, 1100, 100), 4],
                                [range(1100, 5100, 100), 3],
                                [range(5100, 50100, 100), 2],
                                [range(50100, 250100, 100), 1],
                                [range(250100, 500100, 100), 0]], columns = ['AppSum', 'Mark'])
duration_classifier = pd.DataFrame([[range(21, 64), 5],
                                    [range(64, 127), 4],
                                    [range(127, 169), 3],
                                    [range(169, 253), 2],
                                    [range(253, 505), 1]], columns = ['Dur', 'Mark'])
bra_classifier = pd.DataFrame([[np.arange(0, 0.3, 0.1), 4],#burden rate before
                                [np.arange(0.3, 1.1, 0.1), 3],
                                [np.arange(1.1, 3, 0.1), 1],
                                [np.arange(3, 10, 0.1), -3]], columns = ['BRA', 'Mark'])


'''
for i in range(len(age_classifier)):
    if n in age_classifier.iloc[i, 0]:
        n_score = age_classifier.iloc[i, 1]
        print(n_score)
        break

for i in range(len(apptype_classifier)):
    if k == apptype_classifier.iloc[i, 0]:
        k_score = apptype_classifier.iloc[i, 1]
        print(k_score)
        break
    
for i in range(len(edu_classifier)):
    if l == edu_classifier.iloc[i, 0]:
        l_score = edu_classifier.iloc[i, 1]
        print(l_score)
        break
    
print(n_score + k_score + l_score)
'''