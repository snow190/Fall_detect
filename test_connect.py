import pyodbc
conn = pyodbc.connect(driver="SQL Server Native Client 11.0",server="123.195.132.32,1433",
                   database="Basic_Information",
                   uid="sa", pwd="jkl0979229277")  # 黃的資料庫連線
mycursor = conn.cursor()


mycursor.execute("SELECT * FROM jkl_7777")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)