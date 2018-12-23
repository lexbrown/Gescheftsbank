#MVP Stage1 - 3-6-3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random as rnd
from datetime import datetime

capital = 100000
liabilities = 0
placcount = 0
appsperday = 40 #число заявок в день
assets = capital + liabilities
cycle = 252
accounts = pd.DataFrame(columns = ['AccType', 'ClientId', 'App_Id', 'Begindate', 'EndDate', 'BeginQ', 'EndQ', 'Status']) #пустой датафрейм
while wotw != "exit": #wotw - это что?
	for daynumber in range(cycle): #цикл - 252 рабочих дня
		for app in range(appsperday):
			newappscore = np.randn(100)
			if newappscore > 30:
				создать запись в таблице счетов
"""Переменные:
Заявка - Id, score - объединяются в датафрейм - генерируются во фрейме1, состоящем из 100 заявок, каждый день этот фрейм обнуляется, данные переписываются во фрейм2
Score сравнивается с бенчмарком (30)
Число одобренных заявок в день * 1000, ну т.е. кредиты по 1000
Случайное число депозитов в день * 1000, ну т.е. депозиты по 1000
Счета: A, L, K, PnL - обновляются каждый день
Если счета баланса уходят в минус - дефолт
Итерация датафрейма по счетам
Внутри дня разделение на: открытие - активность - закрытие
