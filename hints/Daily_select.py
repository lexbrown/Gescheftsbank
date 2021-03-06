#Daily select

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector as cnt
from sqlalchemy import create_engine
import pandas as pd
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

foo_connector = cnt.connect(host="localhost", user="lexbrown", passwd="***")
foo_cursor = foo_connector.cursor()
foo_cursor.execute("CREATE DATABASE IF NOT EXISTS Foobar")
foo_engine = create_engine('mysql+mysqldb://lexbrown:***@localhost/Foobar', echo=False)

crTable_bar = "CREATE TABLE IF NOT EXISTS Foobar.Bar \
                (Foo1 INT, \
                Foo2 VARCHAR(255), \
                Foo3 DOUBLE(30, 2))"
foo_cursor.execute(crTable_bar)

foo_insert = "INSERT INTO Foobar.Bar (Foo1, Foo2, Foo3) VALUES (%s, %s, %s)"
val = [(12, "snafu", 2.5),
       (13, "tarfu", 3.5),
       (14, "fubar", 4.5),
       (15, "foooo", 5.5)]
foo_cursor.executemany(foo_insert, val)
foo_connector.commit()

daily_select = "SELECT * FROM Foobar.Bar WHERE Foo1 = %s OR Foo2 = %s"
daily_number = (12, 'tarfu')

foo_cursor.execute(daily_select, daily_number)
foo_result = pd.DataFrame(foo_cursor.fetchall())

daily_update = "UPDATE Foobar.Bar SET Foo3 = %s WHERE Foo1 >= %s"
val_update = (8.4, 14)
foo_cursor.execute(daily_update, val_update)
foo_connector.commit()
