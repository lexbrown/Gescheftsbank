#Geschaftsbank - Stage5. Внесение изменений, скоринг + платёжный календарь
#Основные задачи:
#   МОДЕЛЬ КРЕДИТНОГО СКОРИНГА
#   ПЛАТЁЖНЫЙ КАЛЕНДАРЬ
#   Сформировать резервы - пилот
#   Дополнить проверки на балансовые показатели 

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import mysql.connector as cnt
from tqdm import tqdm
#import statsmodels.api as sm
from sqlalchemy import create_engine
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError: 
    pass

db_connector = cnt.connect(host="localhost", user="lexbrown", passwd="***")
bank_cursor = db_connector.cursor()

bank_cursor.execute("DROP DATABASE IF EXISTS Geshbank")

bank_cursor.execute("CREATE DATABASE IF NOT EXISTS Geshbank")
crTable_lapp = "CREATE TABLE IF NOT EXISTS Geshbank.loan_applications \
                (IdApp INT, \
                AppType VARCHAR(255), \
                Sex VARCHAR(10), \
                Age INT, \
                Education VARCHAR(255), \
                Job VARCHAR(255), \
                Experience INT, \
                AnnualIncome INT, \
                OtherSources INT, \
                BurdenRateBefore DOUBLE(10, 4), \
                Possessions VARCHAR(255), \
                CreditHistory VARCHAR(255), \
                AppSum INT, \
                Duration INT, \
                BurdenRateAfter DOUBLE(10, 4), \
                CreditScore DOUBLE(10, 4), \
                Category VARCHAR(255), \
                Approvement VARCHAR(255))"
crTable_la = "CREATE TABLE IF NOT EXISTS Geshbank.loan_accounts \
                (AccType VARCHAR(255), \ 
                ClientId INT, \
                IdApp INT, \
                BeginDate INT, \
                EndDate INT, \
                BeginQ INT, \
                EndQ DOUBLE(30, 2), \
                PD DOUBLE(10, 2), \
                LGD DOUBLE(10, 2), \
                InterestRate DOUBLE(10, 4), \
                Status VARCHAR(255), \
                Random DOUBLE(10, 4), \
                DefaultFunc DOUBLE(10, 4))"
crTable_da = "CREATE TABLE IF NOT EXISTS Geshbank.deposit_accounts \
                (AccType VARCHAR(255), \ 
                ClientId INT, \
                BeginDate INT, \
                EndDate INT, \
                BeginQ INT, \
                EndQ DOUBLE(30, 2), \
                Status VARCHAR(255))"
crTable_bf = "CREATE TABLE IF NOT EXISTS Geshbank.balance_frame \
                (DayNumber INT, \
                CashBalance DOUBLE(30, 2), \
                AssetBalance DOUBLE(30, 2), \
                DailyCashInflow DOUBLE(30, 2), \
                DailyCashOutflow DOUBLE(30, 2))"
bank_cursor.execute(crTable_la)
bank_cursor.execute(crTable_da)
bank_cursor.execute(crTable_bf)
bank_cursor.execute(crTable_lapp)
engine = create_engine('mysql+mysqldb://lexbrown:***@localhost/Geshbank', echo=False)




capital = 10000000
liabilities = 0
interestincome = 0
interestcosts = 0
placcount = 0
loanaccount = 0
operationcosts = 0
default_losses = 0

#reserve_expenses = 0
#reserve_recovery = 0

risk_free_rate = 0.06

daily_outflow = 0
daily_inflow = 0


days =  int(input("Введите количество дней: ")) #перевести на инпуты
max_clients = int(input("Введите максимальное количество клиентов в день: "))



id = 0

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
                               ['Sharaga', 2],
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
                                [np.round(np.arange(0.3, 1.1, 0.1), 1), 3],
                                [np.round(np.arange(1.1, 3, 0.1), 1), 1],
                                [np.round(np.arange(3, 10, 0.1), 1), -3]], columns = ['BRA', 'Mark'])



q = 1

#день
for i in range(days):   #номер дня это i+1
    randnumloans = random.choice(range(max_clients)) #чот сильно
    #randnumloans = (10 + 15 * np.sin(i / 5) + i)
    #randnumdeposits = (10 + 15 * np.sin(i / 5) + i) #чот тож, многовато для маленького банка то
    randnumdeposits = random.choice(range(max_clients)) #чот сильно
    #if cash() > assets()/10:
    randnumapps = random.choice(range(200)) #чот сильно
    for n in range(int(randnumapps)):
        idApp = q
        appType = random.choice(['Card', 'Consumer loan', 'Car loan', 'Mortgage', 'SP loan'])
        sex = random.choice(['M', 'F'])
        age = random.choice(range(18, 66))
        if age <= 25:
            education = random.choice(['Secondary', 'High school', 'Sharaga', 'Bachelor', 'Master', 'PhD'])
        else:
            education = random.choice(['Secondary', 'High school', 'Sharaga', 'Bachelor', 'Master', 'PhD', 'MBA'])
        #job = random.choice(['Unemployed', 'LowGrade', 'BlueCollar', 'Self-employed', 'WhiteCollar', 'MidMan', 'TopMan'])
        #experience = random.choice(range(40))
        if age < 30:
            job = random.choice(['Unemployed', 'LowGrade', 'BlueCollar', 'Self-employed', 'WhiteCollar', 'MidMan'])
            if job == 'Unemployed':
                annualIncome = random.choice(range(0, 16000, 2000))
            elif job in ['LowGrade', 'BlueCollar']:
                annualIncome = random.choice(range(10000, 90000, 2000))
            else:
                annualIncome = random.choice(range(20000, 300000, 10000)) #переделать в бета-распределение
        else:
            job = random.choice(['Unemployed', 'LowGrade', 'BlueCollar', 'Self-employed', 'WhiteCollar', 'MidMan', 'TopMan'])
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
                      'Education':education, 'Job':job, 'Experience':experience, 'AnnualIncome':annualIncome, 'OtherSources':ois, 'BurdenRateBefore':burdenRateBefore,
                       'Possessions':possessions, 'CreditHistory':creditHistory, 'AppSum':appSum, 'Duration':duration,
                       'BurdenRateAfter':burdenRateAfter, 'CreditScore':creditScore, 'Category':category, 'Approvement':approvement}]).to_sql('loan_applications', con = engine, index = False, if_exists = 'append')
        q += 1
        
        if approvement == 'Approved':
            accType = 'L'
            clientId = id + 1
            beginDate = i + 1 #это чтобы дня О не было
            endDate = i + 1 + random.choice(range(2, 16)) * 10
            #beginQ = random.choice(range(1, 101))*100
            beginQ = appSum
            """
            if beginQ > cash():
                continue
            """
            '''
            if netincome() + capital < assets() * 0.1:
                continue
            '''
            status = 'Active'
            prob_d = round(np.random.beta(1, 7) / 10 + 0.01, 2)
            lgd = round(np.random.beta(1, 7), 2)
            interest_rate = round((risk_free_rate + prob_d * lgd) /(1 - prob_d) + 0.015, 4)
            endQ = round(beginQ * (1 + interest_rate * (endDate - beginDate) / 252), 2)
            random_default = random.choice(range(1, 101))/100
            default_function = random_default * np.exp(prob_d)
            #newcustomer = [accType, clientId, beginDate, endDate, beginQ, endQ, prob_d, lgd, interest_rate, status, random_default, default_function]
            #open_loan_accounts.loc[len(open_loan_accounts)] = newcustomer
            pd.DataFrame([{'AccType':accType, 'ClientId':clientId,'IdApp':idApp, 'BeginDate':beginDate, 'EndDate':endDate, 
                          'BeginQ':beginQ, 'EndQ':endQ, 'PD':prob_d, 'LGD':lgd, 'InterestRate':interest_rate, 'Status':status,
                           'Random':random_default, 'DefaultFunc':default_function}]).to_sql('loan_accounts', con = engine, index = False, if_exists = 'append')
            id += 1
            loanaccount += beginQ
            daily_outflow += beginQ
            #reserve_expenses += (beginQ * prob_d * lgd)
    for n in range(int(randnumdeposits)):
        '''if netincome() + capital < assets() * 0.1:
            continue'''
        accType = 'D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 1 + random.choice(range(2, 16)) * 10
        beginQ = random.choice(range(1, 501))*1000
        endQ = round(beginQ * (1 + 0.03 * (endDate - beginDate) / 252), 2)
        status = 'Active'
        #newcustomer = [accType, clientId, beginDate, endDate, beginQ, endQ, status]
        #open_deposit_accounts.loc[len(open_deposit_accounts)] = newcustomer
        pd.DataFrame([{'AccType':accType, 'ClientId':clientId, 'BeginDate':beginDate, 'EndDate':endDate, 'BeginQ':beginQ, 'EndQ':endQ, 'Status':status}]).to_sql('deposit_accounts', con = engine, index = False, if_exists = 'append')
        id += 1
        liabilities += beginQ
        daily_inflow += beginQ

#вечер
    
    #кредиты
    evening_frame = pd.read_sql_query("SELECT * FROM Geshbank.loan_accounts WHERE EndDate = %s", con = engine, params = (i+1, ))
#    for n in range(len(evening_frame)):
#        print('lol')
    closing_update = "UPDATE Geshbank.loan_accounts SET Status = %s WHERE EndDate = %s"
    closing_values = ('Closed', i+1)
    bank_cursor.execute(closing_update, closing_values)
    db_connector.commit()  
    loanaccount -= float(np.sum(evening_frame['BeginQ']))
    #evening_default_frame = pd.read_sql_query("SELECT * FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc >= 1", con = engine, params = (i+1, ))
    daily_inflow += ((pd.read_sql_query("SELECT SUM(BeginQ * (1 - LGD)) AS Repayment FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc >= 1", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    #default_losses += np.sum(pd.read_sql_query("SELECT BeginQ * LGD AS Losses FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc >= 1", con = engine, params = (i+1, )))
    default_losses += ((pd.read_sql_query("SELECT SUM(BeginQ * LGD) AS Losses FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc >= 1", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    interestincome += ((pd.read_sql_query("SELECT SUM(BeginQ * (InterestRate * (EndDate - BeginDate) / 252)) AS Income FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc < 1", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    daily_inflow += ((pd.read_sql_query("SELECT SUM(EndQ) FROM Geshbank.loan_accounts WHERE EndDate = %s AND DefaultFunc < 1", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]

    #депозиты
    evening_frame = pd.read_sql_query("SELECT * FROM Geshbank.deposit_accounts WHERE EndDate = %s", con = engine, params = (i+1, ))
    closing_update = "UPDATE Geshbank.deposit_accounts SET Status = %s WHERE EndDate = %s"
    closing_values = ('Closed', i+1)
    bank_cursor.execute(closing_update, closing_values)
    db_connector.commit()
    liabilities -= np.sum(evening_frame['BeginQ'])
    interestcosts += ((pd.read_sql_query("SELECT SUM(BeginQ * (0.03 * (EndDate - BeginDate) / 252)) AS Cost FROM Geshbank.deposit_accounts WHERE EndDate = %s AND AccType = 'D'", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    interestcosts += ((pd.read_sql_query("SELECT SUM(BeginQ * (0.06 * (EndDate - BeginDate) / 252)) AS Cost FROM Geshbank.deposit_accounts WHERE EndDate = %s AND AccType = 'O/N - D'", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    daily_outflow += ((pd.read_sql_query("SELECT SUM(EndQ) FROM Geshbank.deposit_accounts WHERE EndDate = %s", con = engine, params = (i+1, ))).sum(axis = 0)).iat[0]
    operationcosts += 2000
    daily_outflow += 2000
    

    '''
    for n in range(len(open_loan_accounts)): #вечерняя проверка кредитных счетов
        if open_loan_accounts.loc[n, 'EndDate'] == i+1 and open_loan_accounts.loc[n, 'Status'] == 'Active':
            open_loan_accounts.loc[n, 'Status'] = 'Closed'
            loanaccount -= open_loan_accounts.loc[n, 'BeginQ']
            if open_loan_accounts.loc[n, 'AccType'] != 'O/N - L': #можно грамотнее: если дефолтный и L - тогда признать убыток. Иначе - нет
                #reserve_recovery += (open_loan_accounts.loc[n, 'BeginQ'] * open_loan_accounts.loc[n, 'LGD'] * open_loan_accounts.loc[n, 'PD'])
                if open_loan_accounts.loc[n, 'Default function'] >= 1: #Если дефолт
                    daily_inflow += (open_loan_accounts.loc[n, 'BeginQ'] * (1 - open_loan_accounts.loc[n, 'LGD']))
                    default_losses += (open_loan_accounts.loc[n, 'BeginQ'] * open_loan_accounts.loc[n, 'LGD'])
                else:
                    interestincome += open_loan_accounts.loc[n, 'BeginQ'] * (open_loan_accounts.loc[n, 'Interest rate'] * (open_loan_accounts.loc[n, 'EndDate'] - open_loan_accounts.loc[n, 'BeginDate']) / 252)
                    daily_inflow += (open_loan_accounts.loc[n, 'BeginQ'] * (1 + (open_loan_accounts.loc[n, 'Interest rate'] * (open_loan_accounts.loc[n, 'EndDate'] - open_loan_accounts.loc[n, 'BeginDate']) / 252)))
            else:
                interestincome += open_loan_accounts.loc[n, 'BeginQ'] * (open_loan_accounts.loc[n, 'Interest rate'] * (open_loan_accounts.loc[n, 'EndDate'] - open_loan_accounts.loc[n, 'BeginDate']) / 252)
                daily_inflow += (open_loan_accounts.loc[n, 'BeginQ'] * (1 + (open_loan_accounts.loc[n, 'Interest rate'] * (open_loan_accounts.loc[n, 'EndDate'] - open_loan_accounts.loc[n, 'BeginDate']) / 252)))
            closed_loan_accounts.loc[id_loan_closed] = open_loan_accounts.loc[n]
            id_loan_closed += 1
    for n in range(len(open_deposit_accounts)): #вечерняя проверка депозитных счетов
        if open_deposit_accounts.loc[n, 'EndDate'] == i+1 and open_deposit_accounts.loc[n, 'Status'] == 'Active':
            open_deposit_accounts.loc[n, 'Status'] = 'Closed'
            if open_deposit_accounts.loc[n, 'AccType'] == 'D':
                liabilities -= open_deposit_accounts.loc[n, 'BeginQ']
                interestcosts += open_deposit_accounts.loc[n, 'BeginQ'] * (0.03 * (open_deposit_accounts.loc[n, 'EndDate'] - open_deposit_accounts.loc[n, 'BeginDate']) / 252)
                daily_outflow += (open_deposit_accounts.loc[n, 'BeginQ'] * (1 + (0.03 * (open_deposit_accounts.loc[n, 'EndDate'] - open_deposit_accounts.loc[n, 'BeginDate']) / 252)))
            else: #open_deposit_accounts.loc[n, 'AccType'] == 'O/N':
                liabilities -= open_deposit_accounts.loc[n, 'BeginQ']
                interestcosts += open_deposit_accounts.loc[n, 'BeginQ'] * (0.01 * (open_deposit_accounts.loc[n, 'EndDate'] - open_deposit_accounts.loc[n, 'BeginDate']) / 252)
                daily_outflow += (open_deposit_accounts.loc[n, 'BeginQ'] * (1 + (0.01 * (open_deposit_accounts.loc[n, 'EndDate'] - open_deposit_accounts.loc[n, 'BeginDate']) / 252)))
            #начать closedaccounts
            closed_deposit_accounts.loc[id_deposit_closed] = open_deposit_accounts.loc[n]
            id_deposit_closed += 1
    operationcosts += 200
    daily_outflow += 200
    '''


    #вечерние проверки
    if cash() < 0:
        accType = 'O/N - D'
        clientId = id + 1
        beginDate = i + 1
        endDate = i + 2
        beginQ = int(-cash() + assets() * 0.1)
        endQ = round(beginQ * (1 + risk_free_rate * (endDate - beginDate) / 252), 2)
        status = 'Active'
        pd.DataFrame([{'AccType':accType, 'ClientId':clientId, 'BeginDate':beginDate, 'EndDate':endDate, 'BeginQ':beginQ, 'EndQ':endQ, 'Status':status}]).to_sql('deposit_accounts', con = engine, index = False, if_exists = 'append')
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
        pd.DataFrame([{'AccType':accType, 'ClientId':clientId, 'BeginDate':beginDate, 'EndDate':endDate, 'BeginQ':beginQ, 'EndQ':endQ, 'Status':status}]).to_sql('deposit_accounts', con = engine, index = False, if_exists = 'append')
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
        pd.DataFrame([{'AccType':accType, 'ClientId':clientId, 'BeginDate':beginDate, 'EndDate':endDate, 
                      'BeginQ':beginQ, 'EndQ':endQ, 'PD':prob_d, 'LGD':lgd, 'InterestRate':interest_rate, 'Status':status,
                       'Random':random_default, 'DefaultFunc':default_function}]).to_sql('loan_accounts', con = engine, index = False, if_exists = 'append')
        id += 1
        loanaccount += beginQ
        daily_outflow += beginQ
    else:
        True
        
    '''        
    #openaccounts = openaccounts.drop(np.where(openaccounts["Status"] == "Closed")[0]) - не работает более чем для 6 дней
    open_loan_accounts = open_loan_accounts[open_loan_accounts.Status != "Closed"] #это ужасно
    open_deposit_accounts = open_deposit_accounts[open_deposit_accounts.Status != "Closed"] #дублирование - вообще ужас
    open_loan_accounts.index = np.arange(len(open_loan_accounts))
    open_deposit_accounts.index = np.arange(len(open_deposit_accounts))
    '''
    #operationcosts += 200
    #daily_outflow += 200
    placcount()
    pd.DataFrame([{'DayNumber':i+1, 'CashBalance':cash(), 'AssetBalance':assets(), 'DailyCashInflow':daily_inflow, 'DailyCashOutflow':daily_outflow}]).to_sql('balance_frame', con = engine, index = False, if_exists = 'append')
    daily_outflow = 0
    daily_inflow = 0
    #cash_balance[i] = cash()
    #cash_balance.index = np.arange(days)
    #placcount()
    print("День ", i+1)


#Reports:

#Graphical Report
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
print()
print('Овернайты на рынке межбанковских кредитов брались ', 
      ((pd.read_sql("SELECT COUNT(*) FROM geshbank.deposit_accounts WHERE AccType = 'O/N - D'", con = engine)).sum(axis = 0)).iat[0],
      ' раз:')

'''
if len(closed_deposit_accounts.loc[closed_deposit_accounts.AccType == 'O/N - D']) != 0:
    print(closed_deposit_accounts.loc[closed_deposit_accounts.AccType == 'O/N - D'])
if len(open_deposit_accounts.loc[open_deposit_accounts.AccType == 'O/N - D']) != 0:
    print(open_deposit_accounts.loc[open_deposit_accounts.AccType == 'O/N - D'])
'''

    
print('Овернайты на рынке межбанковских кредитов давались ', 
       ((pd.read_sql("SELECT COUNT(*) FROM geshbank.loan_accounts WHERE AccType = 'O/N - L'", con = engine)).sum(axis = 0)).iat[0],
      ' раз:')

'''
if len(closed_loan_accounts.loc[closed_loan_accounts.AccType == 'O/N - L']) != 0:
    print(closed_loan_accounts.loc[closed_loan_accounts.AccType == 'O/N - L'])
if len(open_loan_accounts.loc[open_loan_accounts.AccType == 'O/N - L']) != 0:
    print(open_loan_accounts.loc[open_loan_accounts.AccType == 'O/N - L'])
'''
    
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
#Внедрить Statsmodel в 5й версии
#Внедрить этап "Утро" - проверка условий
    
