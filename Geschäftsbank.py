#Geschaftsbank - Stage5. Внесение изменений

#Основные задачи:
#   МОДЕЛЬ КРЕДИТНОГО СКОРИНГА
#   ПЛАТЁЖНЫЙ КАЛЕНДАРЬ
#   Сформировать резервы - пилот
#   Дополнить проверки


#============================= импорт модулей
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
#import seaborn as sns #отложить до следущего этапа
import mysql.connector as cnt
#import statsmodels.api as sm #отложим до следующего этапа
from tqdm import tqdm
from sqlalchemy import create_engine
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
import requests
from bs4 import BeautifulSoup
from GBank_database_module import crTable_lapp, crTable_la, crTable_da, crTable_bf
import warnings
warnings.filterwarnings("ignore")
import os




#============================= парсинг ставки Ruonia
url = 'https://www.cbr.ru/hd_base/ruonia/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
rfr = soup.find_all('td', {'class':'right'})[0].get_text() #пока сохранено с запятой, это факап
rfr = float(rfr.replace(',', '.'))





#============================= создание коннектора с базой данных
db_connector = cnt.connect(host="localhost", 
                           user="lexbrown", passwd="******") #нужен ввод пароля
bank_cursor = db_connector.cursor()
engine = create_engine('mysql+mysqldb://lexbrown:******@localhost/Geshbank', 
                       echo=False) #нужен ввод пароля




#============================= создание базы данных на сервере с необходимыми таблицами
bank_cursor.execute("DROP DATABASE IF EXISTS Geshbank")
bank_cursor.execute("CREATE DATABASE IF NOT EXISTS Geshbank")
bank_cursor.execute(crTable_la) #переменные импортированы из модуля
bank_cursor.execute(crTable_da)
bank_cursor.execute(crTable_bf)
bank_cursor.execute(crTable_lapp)




#============================= введение основных переменных
capital = 10000000
liabilities = 0
interestincome = 0
interestcosts = 0
placcount = 0
loanaccount = 0
operationcosts = 0
default_losses = 0
risk_free_rate = 0.06
daily_outflow = 0
daily_inflow = 0
days =  int(input("Введите количество дней: ")) #перевести на инпуты
max_clients = int(input("Введите максимальное количество клиентов в день: "))
id = 0





#============================= введение функционалных показателей
def assets(): #Активы
    return capital + netincome() + liabilities
def cash(): #Наличка
    return assets() - loanaccount
def placcount(): #Чистая процентная маржа
    return interestincome - interestcosts
#def reserves():
#    return reserve_expenses - reserve_recovery
def netincome():
    return placcount() - operationcosts - default_losses





#============================= создание классификаторов для скоринговой модели
age_classifier = pd.DataFrame([[range(18, 22), 2],
                                [range(22, 26), 3],
                                [range(26, 31), 4],
                                [range(31, 37), 5],
                                [range(37, 46), 5],
                                [range(46, 56), 4],
                                [range(56, 66), 2]], 
                                columns = ['Age', 'Mark'])
apptype_classifier = pd.DataFrame([['Card', 0],
                                   ['Consumer loan', 1],
                                   ['Car loan', 2],
                                   ['Mortgage', 3],
                                   ['SP loan', 1]], 
                                    columns = ['AppType', 'Mark'])
edu_classifier = pd.DataFrame([['Secondary', 0],
                               ['High school', 1],
                               ['Sharaga', 2],
                               ['Bachelor', 3],
                               ['Master', 4],
                               ['PhD', 5],
                               ['MBA', 5]], 
                                columns = ['EduType', 'Mark'])
job_classifier = pd.DataFrame([['Unemployed', -5],
                               ['LowGrade', 1],
                               ['BlueCollar', 2],
                               ['Self-employed', 2],
                               ['WhiteCollar', 4],
                               ['MidMan', 5],
                               ['TopMan', 7]], 
                                columns = ['Job', 'Mark'])
experience_classifier = pd.DataFrame([[range(1), 0],
                                    [np.arange(0.25, 3.25, 0.25), 1],
                                    [range(4, 8), 2],
                                    [range(8, 16), 3],
                                    [range(16, 21), 4],
                                    [range(21, 100), 5]], 
                                    columns = ['Experience', 'Mark'])
income_classifier = pd.DataFrame([[range(10000, 30000, 1000), 1],
                                [range(30000, 50000, 1000), 2],
                                [range(50000, 80000, 1000), 3],
                                [range(80000, 300000, 1000), 4],
                                [range(300000, 500000, 1000), 5],
                                [range(500000, 1000000, 1000), 6],
                                [range(1000000, 3005000, 1000), 7]], 
                                columns = ['Income', 'Mark'])
ois_classifier = pd.DataFrame([[range(1), 0], #other income sources
                                [range(1000, 11000, 1000), 1],
                                [range(11000, 51000, 1000), 2],
                                [range(51000, 1000000, 1000), 3]], 
                                columns = ['OIS', 'Mark'])
'''
brb_classifier = pd.DataFrame([[range(1), 3], #burden rate before
                                    [np.arange(0.05, 0.3, 0.05), 2],
                                    [np.arange(0.3, 1.05, 0.05), 1],
                                    [np.arange(1.05, 3.05, 0.05), 0],
                                    [np.arange(3.05, 10, 0.05), -3]], 
                                    columns = ['BRB', 'Mark'])
'''
brb_classifier = pd.DataFrame([[range(1), 3], #burden rate before
                                    [np.round(np.arange(0.05, 0.3, 0.05), 2), 2],
                                    [np.round(np.arange(0.3, 1.05, 0.05), 2), 1],
                                    [np.round(np.arange(1.05, 3.05, 0.05), 2), 0],
                                    [np.round(np.arange(3.05, 10, 0.05), 2), -3]])
possessions_classifier = pd.DataFrame([['-', 0],
                                       ['Poor', 1],
                                       ['Middle', 2],
                                       ['Good', 3]], 
                                        columns = ['PosQuality', 'Mark'])
credithistory_classifier = pd.DataFrame([['-', 0],
                                       ['Poor', -3],
                                       ['Middle', 1],
                                       ['Good', 3]], 
                                        columns = ['CredHist', 'Mark'])
appsum_classifier = pd.DataFrame([[range(100, 1100, 100), 4],
                                [range(1100, 5100, 100), 3],
                                [range(5100, 50100, 100), 2],
                                [range(50100, 250100, 100), 1],
                                [range(250100, 500100, 100), 0]], 
                                columns = ['AppSum', 'Mark'])
duration_classifier = pd.DataFrame([[range(21, 64), 5],
                                    [range(64, 127), 4],
                                    [range(127, 169), 3],
                                    [range(169, 253), 2],
                                    [range(253, 505), 1]], 
                                    columns = ['Dur', 'Mark'])
bra_classifier = pd.DataFrame([[np.arange(0, 0.3, 0.1), 4],#burden rate before
                                [np.round(np.arange(0.3, 1.1, 0.1), 1), 3],
                                [np.round(np.arange(1.1, 3, 0.1), 1), 1],
                                [np.round(np.arange(3, 10, 0.1), 1), -3]], 
                                columns = ['BRA', 'Mark'])
q = 1 #специальная переменная для нумерации id кредитных заявок










#============================= старт моделирования
#============================= верхний цикл - это один день
#============================= 
for i in tqdm(range(days)):   #номер дня это i+1
    #============================= Этап "День" - клиентская активность  
    randnumloans = random.choice(range(max_clients)) #чот сильно
    #randnumloans = (10 + 15 * np.sin(i / 5) + i)
    #randnumdeposits = (10 + 15 * np.sin(i / 5) + i) #попытка смоделировать волатильность внешней среды
    randnumdeposits = random.choice(range(max_clients)) #чот сильно
    randnumapps = random.choice(range(200)) #чот сильно
    for n in range(int(randnumapps)):
        idApp = q
        appType = random.choice(['Card', 'Consumer loan', 'Car loan', 'Mortgage', 
                                 'SP loan'])
        sex = random.choice(['M', 'F'])
        age = random.choice(range(18, 66))
        if age <= 25:
            education = random.choice(['Secondary', 'High school', 'Sharaga', 
                                       'Bachelor', 'Master', 'PhD'])
        else:
            education = random.choice(['Secondary', 'High school', 'Sharaga', 
                                       'Bachelor', 'Master', 'PhD', 'MBA'])
        if age < 30:
            job = random.choice(['Unemployed', 'LowGrade', 'BlueCollar', 
                                 'Self-employed', 'WhiteCollar', 'MidMan'])
            if job == 'Unemployed':
                annualIncome = random.choice(range(0, 16000, 2000))
            elif job in ['LowGrade', 'BlueCollar']:
                annualIncome = random.choice(range(10000, 90000, 2000))
            else:
                annualIncome = random.choice(range(20000, 300000, 10000)) #переделать в бета-распределение
        else:
            job = random.choice(['Unemployed', 'LowGrade', 'BlueCollar', 
                                 'Self-employed', 'WhiteCollar', 'MidMan', 
                                 'TopMan'])
            if job == 'Unemployed':
                annualIncome = random.choice(range(0, 20000, 2000))
            elif job in ['Self-employed', 'WhiteCollar', 'MidMan', 'TopMan']:
                annualIncome = random.choice(range(100000, 300000, 10000)) 
            else:
                annualIncome = random.choice(range(10000, 100000, 2000)) 
        experience = int((age - 18) * np.random.beta(6, 1))
        #annualIncome = random.choice(range(10000, 3000000, 10000))
        ois = random.choice(range(0, 70000, 10000)) #other income sources
        burdenRateBefore = random.choice([0, random.choice(range(0, 16))/4])
        possessions = random.choice(['-', 'Poor', 'Middle', 'Good'])
        creditHistory = random.choice(['-', 'Poor', 'Middle', 'Good'])
        appSum = random.choice(range(100, 500100, 100))
        duration = random.choice(range(21, 504, 21))
        try:
            burdenRateAfter = round(burdenRateBefore + appSum / (annualIncome + ois), 1)
        except:
            burdenRateAfter = 5 
        
        for cl in range(len(age_classifier)):
            if age in age_classifier.iloc[cl, 0]:
                age_score = age_classifier.iloc[cl, 1]
                break
        for cl in range(len(apptype_classifier)):
            if appType == apptype_classifier.iloc[cl, 0]:
                appType_score = apptype_classifier.iloc[cl, 1]
                break
        for cl in range(len(edu_classifier)):
            if education == edu_classifier.iloc[cl, 0]:
                edu_score = edu_classifier.iloc[cl, 1]
                break
        for cl in range(len(job_classifier)):
            if job == job_classifier.iloc[cl, 0]:
                job_score = job_classifier.iloc[cl, 1]
                break    
        for cl in range(len(experience_classifier)):
            if experience in experience_classifier.iloc[cl, 0]:
                experience_score = experience_classifier.iloc[cl, 1]
                break            
        for cl in range(len(income_classifier)):
            if annualIncome in income_classifier.iloc[cl, 0]:
                income_score = income_classifier.iloc[cl, 1]
                break    
        for cl in range(len(ois_classifier)):
            if ois in ois_classifier.iloc[cl, 0]:
                ois_score = ois_classifier.iloc[cl, 1]
                break 
        for cl in range(len(brb_classifier)):
            if burdenRateBefore in brb_classifier.iloc[cl, 0]:
                brb_score = brb_classifier.iloc[cl, 1]
                break 
        for cl in range(len(possessions_classifier)):
            if possessions == possessions_classifier.iloc[cl, 0]:
                possessions_score = possessions_classifier.iloc[cl, 1]
                break
        for cl in range(len(credithistory_classifier)):
            if creditHistory == credithistory_classifier.iloc[cl, 0]:
                ch_score = credithistory_classifier.iloc[cl, 1]
                break
        for cl in range(len(appsum_classifier)):
            if appSum in appsum_classifier.iloc[cl, 0]:
                appSum_score = appsum_classifier.iloc[cl, 1]
                break    
        for cl in range(len(duration_classifier)):
            if duration in duration_classifier.iloc[cl, 0]:
                dur_score = duration_classifier.iloc[cl, 1]
                break 
        for cl in range(len(bra_classifier)):
            if burdenRateAfter in bra_classifier.iloc[cl, 0]:
                bra_score = bra_classifier.iloc[cl, 1]
                break 
        #Дальше запихать расчёт
        #creditScore = random.choice(range(-10, 101, 10))
        creditScore = sum([age_score, appType_score, edu_score,
                           job_score, experience_score, income_score,
                           ois_score, brb_score, possessions_score,
                           ch_score, appSum_score, dur_score, bra_score])
        #category = random.choice(['Green', 'Yellow', 'Red', 'Black'])
        if creditScore <= 20:
            category = 'Black'
            approvement = 'Disapproved'
        elif 20 < creditScore <= 25:
            category = 'Red'
            approvement = 'Approved'
        elif 25 < creditScore <= 30:
            category = 'Yellow'
            approvement = 'Approved'
        else:
            category = 'Green'
            approvement = 'Approved'
        #category = 'foobar'
        #approvement = random.choice(['Approved', 'Disapproved'])
        pd.DataFrame([{'IdApp':idApp, 'AppType':appType, 'Sex':sex, 'Age':age, 
                      'Education':education, 
                      'Job':job, 'Experience':experience, 
                      'AnnualIncome':annualIncome, 'OtherSources':ois, 
                      'BurdenRateBefore':burdenRateBefore,
                      'Possessions':possessions, 
                      'CreditHistory':creditHistory, 
                      'AppSum':appSum, 'Duration':duration,
                      'BurdenRateAfter':burdenRateAfter, 
                      'CreditScore':creditScore, 
                      'Category':category, 'Approvement':approvement}]).to_sql('loan_applications', 
                        con = engine, index = False, if_exists = 'append')
        q += 1
        
        
        #Если кредитная заявка одобрена, то:
        if approvement == 'Approved':
            accType = 'L'
            clientId = id + 1
            beginDate = i + 1 #это чтобы дня О не было
            endDate = i + 1 + random.choice(range(2, 16)) * 10
            #beginQ = random.choice(range(1, 101))*100
            beginQ = appSum
            status = 'Active'
            prob_d = round(np.random.beta(1, 7) / 10 + 0.01, 2)
            lgd = round(np.random.beta(1, 7), 2)
            interest_rate = round((risk_free_rate + prob_d * lgd) /(1 - prob_d) + 0.015, 4)
            endQ = round(beginQ * (1 + interest_rate * (endDate - beginDate) / 252), 2)
            random_default = random.choice(range(1, 101))/100
            default_function = random_default * np.exp(prob_d)
            pd.DataFrame([{'AccType':accType, 'ClientId':clientId,
                           'IdApp':idApp, 
                           'BeginDate':beginDate, 'EndDate':endDate, 
                           'BeginQ':beginQ, 'EndQ':endQ, 'PD':prob_d, 
                           'LGD':lgd, 'InterestRate':interest_rate, 
                           'Status':status,
                           'Random':random_default, 
                           'DefaultFunc':default_function}]).to_sql('loan_accounts', 
                            con = engine, index = False, if_exists = 'append')
            id += 1
            loanaccount += beginQ
            daily_outflow += beginQ
            #reserve_expenses += (beginQ * prob_d * lgd)
            
            
            
    #============Теперь поехали депозиты. Кстати здесь есть возможность распараллеливания
    for n in range(int(randnumdeposits)):
        #if capital + netincome() < assets() * 0.1: #проверка достаточности капитала
            #break #продумать норматив достаточности капитала
        accType = 'D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 1 + random.choice(range(2, 16)) * 10
        beginQ = random.choice(range(1, 501))*1000
        endQ = round(beginQ * (1 + 0.03 * (endDate - beginDate) / 252), 2)
        status = 'Active'
        #newcustomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        #open_deposit_accounts.loc[len(open_deposit_accounts)] = newcustomer
        pd.DataFrame([{'AccType':accType, 
                       'ClientId':clientId, 
                       'BeginDate':beginDate, 
                       'EndDate':endDate, 
                       'BeginQ':beginQ, 
                       'EndQ':endQ, 
                       'Status':status}]).to_sql('deposit_accounts', 
                        con = engine, index = False, if_exists = 'append')
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ





#============================= Этап "Вечер" - выполняются проверки 
        
    #кредиты
    evening_frame = pd.read_sql_query("SELECT * FROM Geshbank.loan_accounts \
                                      WHERE EndDate = %s", con = engine, params = (i+1, ))
    closing_update = "UPDATE Geshbank.loan_accounts \
                    SET Status = %s WHERE EndDate = %s"
    closing_values = ('Closed', i+1)
    bank_cursor.execute(closing_update, closing_values)
    db_connector.commit()  
    loanaccount -= float(np.sum(evening_frame['BeginQ']))
    daily_inflow += ((pd.read_sql_query("SELECT SUM(BeginQ * \(1 - LGD)) AS Repayment \
                                        FROM Geshbank.loan_accounts \
                                        WHERE EndDate = %s AND DefaultFunc >= 1", 
                                        con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    default_losses += ((pd.read_sql_query("SELECT SUM(BeginQ * LGD) AS Losses \
                                          FROM Geshbank.loan_accounts \
                                          WHERE EndDate = %s AND DefaultFunc >= 1", 
                                          con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    interestincome += ((pd.read_sql_query("SELECT SUM(BeginQ * (InterestRate * (EndDate - BeginDate) / 252)) AS Income \
                                          FROM Geshbank.loan_accounts \
                                          WHERE EndDate = %s AND DefaultFunc < 1", 
                                          con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    daily_inflow += ((pd.read_sql_query("SELECT SUM(EndQ) \
                                        FROM Geshbank.loan_accounts \
                                        WHERE EndDate = %s AND DefaultFunc < 1", 
                                        con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]

    #депозиты
    evening_frame = pd.read_sql_query("SELECT * FROM Geshbank.deposit_accounts \
                                      WHERE EndDate = %s", 
                                      con = engine, params = (i+1, ))
    closing_update = "UPDATE Geshbank.deposit_accounts SET Status = %s \
                        WHERE EndDate = %s"
    closing_values = ('Closed', i+1)
    bank_cursor.execute(closing_update, closing_values)
    db_connector.commit()
    liabilities -= np.sum(evening_frame['BeginQ'])
    interestcosts += ((pd.read_sql_query("SELECT SUM(BeginQ * (0.03 * (EndDate - BeginDate) / 252)) AS Cost \
                                         FROM Geshbank.deposit_accounts \
                                         WHERE EndDate = %s AND AccType = 'D'", 
                                         con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    interestcosts += ((pd.read_sql_query("SELECT SUM(BeginQ * (0.06 * (EndDate - BeginDate) / 252)) AS Cost \
                                         FROM Geshbank.deposit_accounts \
                                         WHERE EndDate = %s AND AccType = 'O/N - D'", 
                                         con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    daily_outflow += ((pd.read_sql_query("SELECT SUM(EndQ) \
                                         FROM Geshbank.deposit_accounts \
                                         WHERE EndDate = %s", 
                                         con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    operationcosts += 2000
    daily_outflow += 2000
    

    #============================= Модуль "Межбанковский рынок"
    if cash() < 0:
        accType = 'O/N - D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 2
        beginQ = int(-cash() + assets() * 0.1)
        endQ = round(beginQ * (1 + risk_free_rate * (endDate - beginDate) / 252), 2)
        status = 'Active'
        pd.DataFrame([{'AccType':accType, 
                       'ClientId':clientId, 
                       'BeginDate':beginDate, 
                       'EndDate':endDate, 
                       'BeginQ':beginQ, 
                       'EndQ':endQ, 
                       'Status':status}]).to_sql('deposit_accounts', 
                        con = engine, index = False, if_exists = 'append')
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ
    elif cash() < (assets() * 0.05):
        accType = 'O/N - D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 2
        beginQ = int(assets() * 0.1)
        endQ = round(beginQ * (1 + risk_free_rate * (endDate - beginDate) / 252), 2)
        status = 'Active'
        pd.DataFrame([{'AccType':accType, 
                       'ClientId':clientId, 
                       'BeginDate':beginDate, 
                       'EndDate':endDate, 
                       'BeginQ':beginQ, 
                       'EndQ':endQ, 
                       'Status':status}]).to_sql('deposit_accounts', 
                        con = engine, index = False, if_exists = 'append')
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ
    elif cash() > (assets() * 0.20):
        accType = 'O/N - L'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 2
        beginQ = int(cash() - assets() * 0.15)
        status = 'Active'
        prob_d = 0
        lgd = 0
        interest_rate = risk_free_rate
        endQ = round(beginQ * (1 + interest_rate * (endDate - beginDate) / 252), 2)
        random_default = random.choice(range(1, 101))/100
        default_function = random_default * np.exp(prob_d)
        pd.DataFrame([{'AccType':accType, 
                       'ClientId':clientId, 
                       'BeginDate':beginDate, 
                       'EndDate':endDate,
                       'BeginQ':beginQ, 
                       'EndQ':endQ, 
                       'PD':prob_d, 
                       'LGD':lgd, 
                       'InterestRate':interest_rate, 
                       'Status':status,
                       'Random':random_default, 
                       'DefaultFunc':default_function}]).to_sql('loan_accounts', 
                        con = engine, index = False, if_exists = 'append')
        id += 1
        loanaccount += beginQ
        daily_outflow += beginQ
    else:
        True
    #operationcosts += 200
    #daily_outflow += 200
    placcount()
    pd.DataFrame([{'DayNumber':i+1, 
                   'CashBalance':cash(), 
                   'AssetBalance':assets(), 
                   'DailyCashInflow':daily_inflow, 
                   'DailyCashOutflow':daily_outflow}]).to_sql('balance_frame', 
                    con = engine, index = False, if_exists = 'append')
    daily_outflow = 0
    daily_inflow = 0
    #print("День ", i+1)







#============================= модуль визуализации и построения отчётов
graphRep = plt.figure(figsize=(15, 15))
ax1 = graphRep.add_subplot(3, 2, 1)
ax2 = graphRep.add_subplot(3, 2, 2)
ax3 = graphRep.add_subplot(3, 2, 3)
ax4 = graphRep.add_subplot(3, 2, 4)
ax5 = graphRep.add_subplot(3, 2, 5)
ax6 = graphRep.add_subplot(3, 2, 6)
balancesheet = pd.DataFrame([[loanaccount, 0], [cash(), 0], 
                        [0, capital], [0, netincome()], [0, liabilities]], 
    index = ['Loans', 'Cash', 'Equity', 'RE', 'Debt'], 
    columns = ['Assets', 'Equity and Debt'])
incomestatement = pd.DataFrame([interestincome, interestcosts, placcount(),
                                operationcosts, default_losses, netincome()], 
    index = ['Interest income', 'Interest costs (-)', 'NIM', 
             'Operating costs (-)', 'Default losses (-)', 'Net income'], 
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


cash_balance = pd.read_sql('SELECT * FROM Geshbank.Balance_frame', con = engine)
#cash_balance['CashBalance'].plot(grid = True, ax = ax3, marker = 'D', fontsize = 12, color = 'orange')
cash_balance['CashBalance'].plot(grid = True, ax = ax3, fontsize = 12, color = 'orange')
#ax3.fill_between(cash_balance['DayNumber'], cash_balance['Balance'], color = 'r')
asset_balance = pd.read_sql('SELECT * FROM Geshbank.Balance_frame', con = engine)
#asset_balance['AssetBalance'].plot(grid = True, ax = ax3, marker = 'o', fontsize = 12, color = 'red')
asset_balance['AssetBalance'].plot(grid = True, ax = ax3, fontsize = 12, color = 'red')
ax3.set_ylabel("U.S. dollars", fontsize = 15)
ax3.set_title("Cash balance", fontsize = 25)
ax3.legend(loc="best", fontsize = 12)

cash_balance['DailyCashOutflow'].plot(grid = True, ax = ax4, marker = 's', fontsize = 12, color = 'g')
cash_balance['DailyCashInflow'].plot(grid = True, ax = ax4, marker = 'v', fontsize = 12, color = 'b')
ax4.set_title("Daily flows", fontsize = 25)
ax4.legend(loc="best", fontsize = 12)
#ax4.set_xticks(cash_balance['DayNumber'])

unionframe = pd.read_sql('SELECT * FROM Geshbank.loan_accounts', con = engine)
unionframe.index = np.arange(len(unionframe))
ax5.hist(unionframe['LGD'], bins = 11)
ax5.set_title("LGD Distribution", fontsize = 25)

ax6.hist(unionframe['PD'], bins = 8)
ax6.set_title("PD Distribution", fontsize = 25)

plt.subplots_adjust(wspace=0.5)
graphRep.savefig("Report - Stage 5.png")








#Отчёт в виде таблиц:
print('\n',"Банк работал ", days, " дней", '\n')
print("Баланс на конец периода:")
print(balancesheet, '\n')
print("Total assets: ", assets(), '\n')
print(incomestatement, '\n')
print('Овернайты на рынке межбанковских кредитов брались ', 
      ((pd.read_sql("SELECT COUNT(*) FROM geshbank.deposit_accounts \
                    WHERE AccType = 'O/N - D'", 
                    con = engine)).sum(axis = 0)).iat[0], ' раз:')
print('Овернайты на рынке межбанковских кредитов давались ', 
       ((pd.read_sql("SELECT COUNT(*) FROM geshbank.loan_accounts \
                     WHERE AccType = 'O/N - L'", 
                     con = engine)).sum(axis = 0)).iat[0], ' раз:')







#для удобства проверки датасеты можно сохранить в Excel
question = input('Сохраняем весь этот ужас? ')
if question == 'y':
    ladf = pd.read_sql('SELECT * FROM Geshbank.loan_accounts', con = engine)
    ladf.to_excel('Loan_accounts_Stage5.xlsx')
    dadf = pd.read_sql('SELECT * FROM Geshbank.deposit_accounts', con = engine)
    dadf.to_excel('Deposit_accounts_Stage5.xlsx')
    bfdf = pd.read_sql('SELECT * FROM Geshbank.Balance_frame', con = engine)
    bfdf.to_excel('Balance_frame_Stage5.xlsx')
    afdf = pd.read_sql('SELECT * FROM Geshbank.Loan_applications', con = engine)
    afdf.to_excel('Loan_applications_Stage5.xlsx')

    

#гипотеза: RE коррелирует с кэшем
#Внедрить этап "Утро" - проверка условий
    
