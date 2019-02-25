# just test

from sqlalchemy import create_engine
import pandas as pd
import pymysql

#engine = create_engine('mysql+mysqldb://...', echo = False)
engine = create_engine('mysql+mysqldb://...', pool_recycle = 3600)
#df = pd.DataFrame({'name': ['User1', 'User2', 'User3']})
#df.to_sql('users', con = engine, if_exists = 'replace')

#в итоге решение откопал здесь https://4admin.space/all/modulenotfounderror-no-module-named-mysqldb/
