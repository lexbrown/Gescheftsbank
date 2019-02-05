# MySQL test

import mysql.connector

testdb = mysql.connector.connect(
  host="localhost",
  user="lexbrown",
  passwd="****",
  database = "testdatabase"
)

#print(testdb) - testdb

testcursor = testdb.cursor()

#testcursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")

#testcursor.execute("SHOW DATABASES")

#for x in testcursor:
#  print(x)

  
testcursor.execute("CREATE TABLE IF NOT EXISTS customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = [
  ('Peter', 'Lowstreet 4'),
  ('Amy', 'Apple st 652'),
  ('Hannah', 'Mountain 21'),
  ('Michael', 'Valley 345'),
  ('Sandy', 'Ocean blvd 2'),
  ('Betty', 'Green Grass 1'),
  ('Richard', 'Sky st 331'),
  ('Susan', 'One way 98'),
  ('Vicky', 'Yellow Garden 2'),
  ('Ben', 'Park Lane 38'),
  ('William', 'Central st 954'),
  ('Chuck', 'Main Road 989'),
  ('Viola', 'Sideway 1633')
]

testcursor.executemany(sql, val)

testdb.commit

print(testcursor.rowcount, "was inserted.")
