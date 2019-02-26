# Test MySQL 3

from sqlalchemy import create_engine
import pandas as pd
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

engine = create_engine('mysql+mysqldb://lexbrown:***@localhost/newdb', echo=False)

df5 = pd.read_excel('rawset.xlsx')

df5.to_sql('pisos', con = engine, index = False, if_exists = 'replace')

df1488 = pd.read_sql_query("SELECT * FROM newdb.pisos", con = engine)