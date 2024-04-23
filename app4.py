from flask import Flask, jsonify
from flask_mysqldb import MySQL
import pymysql

app = Flask(__name__)

# Configure database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Set your MySQL password here if you have one
app.config['MYSQL_DB'] = 'testing'  # Change to your database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Depending on the package you're using, you might need to switch to Flask-MySQL
# If you continue using flask_mysqldb but want to specify the UNIX socket, 
# you need to manually configure this in the MySQL connection creation in pymysql.
# Here's how you might modify it to use pymysql directly for more explicit control:
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

mysql = MySQL(app)

@app.route('/')
@app.route('/test_db')
def test_db():
    try:
        conn = pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            db=app.config['MYSQL_DB'],
            unix_socket=app.config['MYSQL_UNIX_SOCKET']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        return f"MySQL version: {version}"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
