#MVP Stage1 - 3-6-3

import numpy as np
import pandas as pd
import matplotlib as mpl

capital = 100000
liabilities = 0
placcount = 0
appsperday = 100 #число заявок в день
assets = capital + liabilities
while wotw != "exit": #wotw - это что?
	for i in range(5): #цикл - 5 рабочих дней
		for app in range(appsperday):
			newappscore = np.randn(100)
			if newappscore > 30:
"""Переменные:
Заявка - Id, score - объединяются в датафрейм - генерируются во фрейме1, состоящем из 100 заявок, каждый день этот фрейм обнуляется, данные переписываются во фрейм2
Score сравнивается с бенчмарком (30)
Число одобренных заявок в неделю * 1000, ну т.е. кредиты по 1000
Случайное число депозитов в неделю * 1000, ну т.е. депозиты по 1000
Счета: A, L, K, PnL - обновляются каждый день
Если счета баланса уходят в минус - дефолт
Итерация датафрейма по счетам
