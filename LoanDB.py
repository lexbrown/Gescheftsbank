import mysql.connector

loandb = mysql.connector.connect(
  host="localhost",
  user="lexbrown",
  passwd="******"
)

cursordb = loandb.cursor()

cursordb.execute("CREATE DATABASE Loanapps")

cursordb.execute("CREATE TABLE Applicants (name VARCHAR(255), address VARCHAR(255))")