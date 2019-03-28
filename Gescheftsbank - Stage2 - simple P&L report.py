#Stage2. Добавлен P&L report

import numpy as np #1
import pandas as pd
import random
import matplotlib.pyplot as plt
#import statsmodels.api as sm

capital = 100000
liabilities = 0
interestincome = 0
interestcosts = 0
placcount = 0
loanaccount = 0
def assets():
    return capital + netincome() + liabilities
def cash():
    return assets() - loanaccount
def netincome():
    return placcount - operatincosts

days =  int(input("Введите количество дней: ")) #перевести на инпуты
idclosed = 0
openaccounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 
                                   'EndDate', 'BeginQ', 'EndQ', 'Status'])
closedaccounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 
                                   'EndDate', 'BeginQ', 'EndQ', 'Status'])
id = 0  #len(openaccounts) 

#день
for i in range(days):   #номер дня это i+1
    randnumloans = random.choice(range(100)) #чот сильно
    randnumdeposits = random.choice(range(100)) #чот тож, многовато для маленького банка то
    for n in range(randnumloans):
        accType = 'L'
        clientId = id + 1
        beginDate = i + 1 #это чтобы дня О не было
        endDate = i + 6
        beginQ = 1000
        endQ = beginQ * 1.06
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        openaccounts.loc[len(openaccounts)] = newcostomer
        id += 1
        loanaccount += 1000
    for n in range(randnumdeposits):
        accType = 'D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 6
        beginQ = 1000
        endQ = beginQ * 1.03
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        openaccounts.loc[len(openaccounts)] = newcostomer
        id += 1
        liabilities += 1000
#вечер
    for n in range(len(openaccounts)):
        if openaccounts.loc[n, 'EndDate'] == i+1 and openaccounts.loc[n, 'Status'] == 'Active':
            openaccounts.loc[n, 'Status'] = 'Closed'
            if openaccounts.loc[n, 'AccType'] == 'D':
                liabilities -= 1000
                interestcosts += 30
            else:
                loanaccount -= 1000
                interestincome += 60
            #начать closedaccounts
            closedaccounts.loc[idclosed] = openaccounts.loc[n]
            idclosed += 1
    #openaccounts = openaccounts.drop(np.where(openaccounts["Status"] == "Closed")[0]) - не работает более чем для 6 дней
    openaccounts = openaccounts[openaccounts.Status != "Closed"] #это ужасно
    openaccounts.index = np.arange(len(openaccounts))
operatincosts = days * 200
placcount = interestincome - interestcosts

#Reports:

#Graphical Report
graphRep = plt.figure(figsize=(10, 5))
ax1 = graphRep.add_subplot(1, 2, 1)
ax2 = graphRep.add_subplot(1, 2, 2)
balancesheet = pd.DataFrame([[loanaccount, 0], [cash(), 0], 
                        [0, capital], [0, netincome()], [0, liabilities]], 
    index = ['Loans', 'Cash', 'Equity', 'RE', 'Debt'], 
    columns = ['Assets', 'Equity and Debt'])
incomestatement = pd.DataFrame([interestincome, interestcosts, 
                                placcount, operatincosts, netincome()], 
    index = ['Interest income', 'Interest costs (-)', 'Net profit margin', 'Operating costs (-)', 'Net income'], 
    columns = ['Accounts'])
#incomestatement.index.name = "P&L accounts"
balancesheet.T.plot(grid = True, rot = 0, ax = ax1, kind = "bar", stacked = True, fontsize = 15)
incomestatement.plot(grid = True, rot = 60, ax = ax2, kind = "bar", fontsize = 10)
ax1.set_ylabel("U.S. dollars", fontsize = 20)
ax1.set_title("Balance sheet", fontsize = 30)
ax1.legend(loc= "center right", fontsize = 10)
#ax2.set_ylabel("U.S. dollars", fontsize = 20)
ax2.set_title("Income statement", fontsize = 30)
#ax2.legend(loc="center left", fontsize = 12)
plt.subplots_adjust(wspace=0.5)
graphRep.savefig("report2.png")

#Table reports:
print()
print("Банк работал ", days, " дней")
print()
print("Баланс на конец периода:")
print()
print(balancesheet)
print()
print("Total assets: ", assets())

