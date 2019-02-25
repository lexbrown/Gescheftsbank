# just test

from sqlalchemy import create_engine
import pandas as pd
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

engine = create_engine('mysql+mysqldb://lexbrown:*******@localhost/newdb', echo=True)
df = pd.DataFrame({'name': ['User1', 'User2', 'User1488']})
df.to_sql('users', con = engine, if_exists = 'replace')

#в итоге решение откопал здесь https://4admin.space/all/modulenotfounderror-no-module-named-mysqldb/
