#MVP Stage1 - 3-6-3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime

capital = 100000
liabilities = 0
placcount = 0
assets = capital + liabilities
days = 252
id = 0
accounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 'EndDate', 'BeginQ', 'EndQ', 'Status'])
for i in range(days):
    randnumloans = random.choice(range(40))
    randnumdeposits = random.choice(range(40))
    for n in range(randnumloans):
        accType = 'L'
        clientId = id
        beginDate = i
        endDate = i + 5
        beginQ = 100000
        endQ = beginQ * 1.06
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        accounts.loc[id] = newcostomer
        id += 1
    for n in range(randnumdeposits):
        accType = 'D'
        clientId = id
        beginDate = i
        endDate = i + 5
        beginQ = 100000
        endQ = beginQ * 1.03
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        accounts.loc[id] = newcostomer
        id += 1
"""Переменные:
Заявка - Id, score - объединяются в датафрейм - генерируются во фрейме1, состоящем из 100 заявок, каждый день этот фрейм обнуляется, данные переписываются во фрейм2
Score сравнивается с бенчмарком (30) - в MVP отказаться!!! 
Число одобренных заявок в день * 1000, ну т.е. кредиты по 1000
Случайное число депозитов в день * 1000, ну т.е. депозиты по 1000
Счета: A, L, K, PnL - обновляются каждый день
Если счета баланса уходят в минус - дефолт
Итерация датафрейма по счетам
Внутри дня разделение на: открытие - активность - закрытие
Каждый новый счёт оформлять в виде словаря - на втором этапе. На первом в виде листа
