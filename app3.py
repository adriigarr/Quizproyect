import MySQLdb

connection = MySQLdb.connect(host='127.0.0.1',
                             user='root',
                             passwd='',
                             db='testing',
                             port=3306)
cursor = connection.cursor()
cursor.execute("SHOW DATABASES")
print(cursor.fetchone())
cursor.close()
connection.close()