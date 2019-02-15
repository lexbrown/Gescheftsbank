# Test MySQL 2.

import pandas as pd
import numpy as np
import mysql.connector as cnt

trial_init = cnt.connect(host="localhost", 
                       user="lexbrown", 
                       passwd="****")

trial_cursor = trial_init.cursor()
trial_cursor.execute("CREATE DATABASE IF NOT EXISTS Trial2db")

trial2db = cnt.connect(host="localhost", 
                       user="lexbrown", 
                       passwd="****",
                       database = 'Trial2db')

trial_new_cursor = trial2db.cursor()

dataset = pd.DataFrame([['FR', 'Paris', 'Euro'], ['GR', 'Berlin', 'Euro'], 
                        ['RU', 'Moscow', 'Rub'], ['US', 'DC', 'Dollar'], 
                        ['TR', 'Ankra', 'Lira'], ['GB', 'London', 'Pound']], index = np.arange(6), columns = ['Country', 'Capital', 'Currency'])

trial_new_cursor.execute("CREATE TABLE IF NOT EXISTS Countries (country VARCHAR(255), capital VARCHAR (255), currency VARCHAR(255))")

sql = "INSERT INTO Countries (country, capital, currency) VALUES (%s, %s, %s)"
val = [['FR', 'Paris', 'Euro'], ['GR', 'Berlin', 'Euro'], 
                        ['RU', 'Moscow', 'Rub'], ['US', 'DC', 'Dollar'], 
                        ['TR', 'Ankra', 'Lira'], ['GB', 'London', 'Pound']]
trial_new_cursor.executemany(sql, val)

trial2db.commit()

pause = input('May I drop the table?')

drop = "DROP TABLE Countries"

trial_new_cursor.execute(drop)
