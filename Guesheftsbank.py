#MVP Stage1 - 3-6-3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
from bs4 import BeautifulSoup #в mvp не используется

capital = 100000
liabilities = 0
placcount = 0
loanaccount = 0
def assets():
    return capital + placcount + liabilities
def cash():
    return capital + placcount + liabilities - loanaccount

days = 20
id = 0 #Пусть клиентский айди начинается с 1
accounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 'EndDate', 'BeginQ', 'EndQ', 'Status'])
#день
for i in range(days):   #номер дня это i+1
    randnumloans = random.choice(range(40))
    randnumdeposits = random.choice(range(40))
    for n in range(randnumloans):
        accType = 'L'
        clientId = id + 1
        beginDate = i + 1 #это чтобы дня О не было
        endDate = beginDate + 5
        beginQ = 1000
        endQ = beginQ * 1.06
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        accounts.loc[id] = newcostomer
        id += 1
        loanaccount += 1000
    for n in range(randnumdeposits):
        accType = 'D'
        clientId = id + 1
        beginDate = i + 1
        endDate = beginDate + 5
        beginQ = 1000
        endQ = beginQ * 1.03
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        accounts.loc[id] = newcostomer
        id += 1
        liabilities += 1000
#вечер
    for n in range(len(accounts)):
        if capital + placcount + liabilities  - loanaccount < (capital + placcount + liabilities) / 10:
            print("ЦБ отзывает лицензию")
            break
        if accounts.loc[n, 'EndDate'] == i+1 and accounts.loc[n, 'Status'] == 'Active':
            accounts.loc[n, 'Status'] = 'Closed'
            if accounts.loc[n, 'AccType'] == 'D':
                liabilities -= 1000
                placcount -= 30
            else:
                loanaccount -= 1000
                placcount += 60


print("Assets: ", assets())
print("    including cash: ", cash())
print("    including loans: ", loanaccount)
print("Capital: ", capital)
print("Retained Earnings: ", placcount)
print("Liabilities: ", liabilities)

#Graphical Report
graphRep = plt.figure(figsize=(10, 5))
ax = graphRep.add_subplot(1, 1, 1)
finalset = pd.DataFrame([[loanaccount, 0], [capital + placcount + liabilities - loanaccount, 0], 
                        [0, capital], [0, placcount], [0, liabilities]], index = ['Loans', 'Cash', 'Equity', 'RE', 'Debt'], 
    columns = ['Assets', 'Equity and Debt'])
finalset.plot(ax = ax, kind = "bar", stacked = True)
ax.set_ylabel("U.S. dollars", fontsize = 20)
ax.set_title("Balance sheet", fontsize = 30)
graphRep.savefig("report.png")

"""Переменные:
Заявка - Id, score - объединяются в датафрейм - генерируются во фрейме1, 
состоящем из 100 заявок, каждый день этот фрейм обнуляется, данные переписываются во фрейм2
Score сравнивается с бенчмарком (30) - в MVP отказаться!!! 
Число одобренных заявок в день * 1000, ну т.е. кредиты по 1000
Случайное число депозитов в день * 1000, ну т.е. депозиты по 1000
Счета: A, L, K, PnL - обновляются каждый день
Если счета баланса уходят в минус - дефолт
Итерация датафрейма по счетам - ВЫПОЛНЕНО
Внутри дня разделение на: открытие - активность - закрытие --- ПРОРАБОТАТЬ ОТКРЫТИЕ
Каждый новый счёт оформлять в виде словаря --- на втором этапе. На первом в виде листа
Оформить графон --- В ПРОЦЕССЕ
настроить инпуты
Написать функцию для статей
Настроить интеграцию с URL для скачивания бенчмарков
