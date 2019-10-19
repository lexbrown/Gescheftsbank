# Проект Geschäftsbank

![](https://github.com/lexbrown/Gescheftsbank/blob/master/PR-campaign/gblogo.PNG)

## Общая информация

### Annotation (ENG)
A platform to test new solutions and business process. Our mission is to simulate the financial system whose starting point is a commercial bank.
The project is conducted in order to simulate banking activities and financial companies' deals. The goal is to demonstrate an exposure to several finansial risks:
- Credit risk,
- Market risk,
- ALM-risks (including interest rate risk, foreign exchange risk, and liquidity risk).


### Аннотация (РУС)
Платформа для тестирования новых решений и бизнес-процессов. Наша миссия смоделировать финансовую систему, точкой отсчёта которой является коммерческий банк.
Проект создаётся для того, чтобы смоделировать банковскую активность и активность финансовых компаний с целью демонстрации воздействия следующих рисков:
- Кредитный риск, 
- Рыночный риск, 
- ALM-риски (включая процентный, валютный и риск ликвидности).


### Условия запуска
- Python (версии не ниже 3.5)
- MySQL сервер


### Результаты
Результаты итераций представлены в [репозитории](https://github.com/lexbrown/Gescheftsbank/tree/master/results)

### История проекта
История проекта, ход работы и теоретические предпосылки описаны в соответствующем [репозитории](https://github.com/lexbrown/Gescheftsbank/tree/master/Politics)

###Тестирование
По результатам каждого испытания, проводится калибровка модели с целью улучшения параметров и повышения правдоподобия. 
Результаты тестирования представлены в виде датасетов и соответствующих графиков в репозитории [Testing](https://github.com/lexbrown/Gescheftsbank/tree/master/testing)



## Ход реализации

| Этап  | Описание |
| ------------- | ------------- |
| *Этап 1*  | Модель 3-6-3 <br> Демонстрируются стандартизированные клиенты | 
| *Этап 2*  | Дифференциация заёмщиков <br> Введение Income Statement <br> Начало разработки модуля "Межбанковский рынок" |
| *Этап 3*  | Разработка динамического ценообразования на основе метрик PD-LGD-EAD <br> Разработка системы резервирования капитала <br> Реализована модель дефолтов|
| *Этап 4*  | Перевод хранения данных на MySQL сервер <br> Скорректирован расчёт доходности | 
| *Этап 5*  | Разработка скоринговой модели <br> Разра,отка платёжного календаря | 
