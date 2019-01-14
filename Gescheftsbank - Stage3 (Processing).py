#Geschaftsbank - Stage3. Внесение изменений

#Основные задачи:
#   Заняться оптимизацией
#   Внедрить модель PD-LGD-EAD
#   Ввести стохастические параметры клиентов - В ПРОЦЕССЕ
#   Развести заёмщиков и кредиторов в разные датафреймы - начинаю...
#   Написать проверку на отрицательность кэша - готово

import numpy as np
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
operationcosts = 0

daily_outflow = 0
daily_inflow = 0


days =  int(input("Введите количество дней: ")) #перевести на инпуты
idclosed = 0
openaccounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 
                                   'EndDate', 'BeginQ', 'EndQ', 'Status'])
closedaccounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'BeginDate', 
                                   'EndDate', 'BeginQ', 'EndQ', 'Status'])
cash_balance = pd.DataFrame(columns = ['DayNumber', 'Balance', 'Daily outflows', 'Daily inflows'])
#cash_balance = pd.Series([0])
id = 0  #len(openaccounts) 

def assets():
    return capital + netincome() + liabilities
def cash():
    return assets() - loanaccount
def placcount():
    return interestincome - interestcosts
def netincome():
    return placcount() - operationcosts
'''def interbank_loan():
    accType = 'O/N'
    clientId = id + 1
    beginDate = i + 1
    endDate = i + 2
    beginQ = -2 * cash
    endQ = beginQ * 1.01
    status = 'Active'
    newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
    openaccounts.loc[len(openaccounts)] = newcostomer
    global id
    global liabilities
    global daily_inflow
    id += 1
    liabilities += beginQ
    daily_inflow += beginQ'''
    

#день
for i in range(days):   #номер дня это i+1
    randnumloans = random.choice(range(100)) #чот сильно
    randnumdeposits = random.choice(range(100)) #чот тож, многовато для маленького банка то
    #if cash() > assets()/10:
    for n in range(randnumloans):
        accType = 'L'
        clientId = id + 1
        beginDate = i + 1 #это чтобы дня О не было
        endDate = i + 6
        beginQ = random.choice(range(1, 101))*100
        if beginQ > cash():
            continue
        endQ = beginQ * 1.06
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        openaccounts.loc[len(openaccounts)] = newcostomer
        id += 1
        loanaccount += beginQ
        daily_outflow += beginQ
    for n in range(randnumdeposits):
        accType = 'D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 6
        beginQ = random.choice(range(1, 101))*100
        endQ = beginQ * 1.03
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        openaccounts.loc[len(openaccounts)] = newcostomer
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ
            
#вечер
    for n in range(len(openaccounts)):
        if openaccounts.loc[n, 'EndDate'] == i+1 and openaccounts.loc[n, 'Status'] == 'Active':
            openaccounts.loc[n, 'Status'] = 'Closed'
            if openaccounts.loc[n, 'AccType'] == 'D':
                liabilities -= openaccounts.loc[n, 'BeginQ']
                interestcosts += openaccounts.loc[n, 'BeginQ'] * 0.03
                daily_outflow += (openaccounts.loc[n, 'BeginQ'] * 1.03)
            elif openaccounts.loc[n, 'AccType'] == 'O/N':
                liabilities -= openaccounts.loc[n, 'BeginQ']
                interestcosts += openaccounts.loc[n, 'BeginQ'] * 0.01
                daily_outflow += (openaccounts.loc[n, 'BeginQ'] * 1.01)
            else:
                loanaccount -= openaccounts.loc[n, 'BeginQ']
                interestincome += openaccounts.loc[n, 'BeginQ'] * 0.06
                daily_inflow += (openaccounts.loc[n, 'BeginQ'] * 1.06)
            #начать closedaccounts
            closedaccounts.loc[idclosed] = openaccounts.loc[n]
            idclosed += 1
    if cash() < 0:
        accType = 'O/N'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 2
        beginQ = -2 * cash()
        endQ = beginQ * 1.01
        status = 'Active'
        newcostomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        openaccounts.loc[len(openaccounts)] = newcostomer
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ
        
        
    #openaccounts = openaccounts.drop(np.where(openaccounts["Status"] == "Closed")[0]) - не работает более чем для 6 дней
    openaccounts = openaccounts[openaccounts.Status != "Closed"] #это ужасно
    openaccounts.index = np.arange(len(openaccounts))
    operationcosts += 200
    daily_outflow += 200
    placcount()
    cash_balance.loc[i] = [i+1, cash(), daily_outflow, daily_inflow]
    daily_outflow = 0
    daily_inflow = 0
    #cash_balance[i] = cash()
    #cash_balance.index = np.arange(days)
    #placcount()
cash_balance.index = cash_balance['DayNumber']
#Reports:

#Graphical Report
graphRep = plt.figure(figsize=(15, 10))
ax1 = graphRep.add_subplot(2, 2, 1)
ax2 = graphRep.add_subplot(2, 2, 2)
ax3 = graphRep.add_subplot(2, 2, 3)
ax4 = graphRep.add_subplot(2, 2, 4)
balancesheet = pd.DataFrame([[loanaccount, 0], [cash(), 0], 
                        [0, capital], [0, netincome()], [0, liabilities]], 
    index = ['Loans', 'Cash', 'Equity', 'RE', 'Debt'], 
    columns = ['Assets', 'Equity and Debt'])
incomestatement = pd.DataFrame([interestincome, interestcosts, 
                                placcount(), operationcosts, netincome()], 
    index = ['Interest income', 'Interest costs (-)', 'Net profit margin', 'Operating costs (-)', 'Net income'], 
    columns = ['Accounts'])
#incomestatement.index.name = "P&L accounts"

balancesheet.T.plot(grid = True, rot = 0, ax = ax1, kind = "bar", stacked = True, fontsize = 12)
ax1.set_ylabel("U.S. dollars", fontsize = 15)
ax1.set_title("Balance sheet", fontsize = 25)
ax1.legend(loc= "center right", fontsize = 10)

#ax2.set_ylabel(fontsize = 20)
ax2.set_title("Income statement", fontsize = 25)
#ax2.legend(loc="center left", fontsize = 12)
#incomestatement.T.plot(grid = True, rot = 0, ax = ax2, kind = "bar", fontsize = 12)
ax2.barh(incomestatement.index, incomestatement.Accounts)
ax2.invert_yaxis()
ax2.grid(True)

cash_balance['Balance'].plot(grid = True, ax = ax3, marker = 'D', fontsize = 12, color = 'r')
ax3.set_ylabel("U.S. dollars", fontsize = 15)
ax3.set_title("Cash balance", fontsize = 25)

cash_balance['Daily outflows'].plot(grid = True, ax = ax4, marker = 's', fontsize = 12, color = 'g')
cash_balance['Daily inflows'].plot(grid = True, ax = ax4, marker = 'v', fontsize = 12, color = 'b')
ax4.set_title("Daily flows", fontsize = 25)
ax4.legend(loc="best", fontsize = 12)
#ax4.set_xticks(cash_balance['DayNumber'])

plt.subplots_adjust(wspace=0.5)
graphRep.savefig("report3.png")

#Table reports:
print()
print("Банк работал ", days, " дней")
print()
print("Баланс на конец периода:")
print(balancesheet)
print()
print("Total assets: ", assets())
print()
print(incomestatement)

#Внедрить Statsmodel в 4й версии
#Внедрить этап "Утро" - проверка условий
