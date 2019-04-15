# Classifier

import pandas as pd

n = int(input('Введи возраст: '))
age_classifier = pd.DataFrame([[range(18, 22), 2],
                                [range(22, 26), 3],
                                [range(26, 31), 4],
                                [range(31, 37), 5],
                                [range(37, 46), 5],
                                [range(46, 56), 4],
                                [range(56, 66), 2]], columns = ['Age', 'Mark'])

'''
i = 0
while n not in age_classifier.iloc[i, 0]:
    i += 1
n_score = age_classifier.iloc[i, 1]
print(n_score)
'''

for i in range(len(age_classifier)):
    if n in age_classifier.iloc[i, 0]:
        n_score = age_classifier.iloc[i, 1]
        print(n_score)