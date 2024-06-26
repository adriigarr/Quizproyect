from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import re

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'your_super_secret_key'  # Change this to a random secret key

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password (if set)
app.config['MYSQL_DB'] = 'testingQuizs'  # Your database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'

# Initialize MySQL
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor,
    unix_socket=app.config['MYSQL_UNIX_SOCKET']
)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userID']
            session['name'] = user['name']
            message = 'Logged in successfully!'
            return render_template('user.html', message=message)
        else:
            message = 'Incorrect username/password!'
    return render_template('login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'surname1' in request.form and 'surname2' in request.form and 'gender' in request.form and 'dob' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        surname1 = request.form['surname1']
        surname2 = request.form['surname2']
        gender = request.form['gender']
        dateBirth = request.form['dob']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not (name and surname1 and surname2 and gender and dateBirth and email and password):
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user (name, surname1, surname2, gender, dateBirth, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                           (name, surname1, surname2, gender, dateBirth, email, password))
            mysql.commit()
            message = 'You have successfully registered!'
    return render_template('register.html', message=message)


# Define the route for pregunta1
@app.route('/pregunta1')
def pregunta1():
    # Your logic for the quiz page
    return render_template('pregunta1.html')


# Define the route for pregunta2
@app.route('/pregunta2')
def pregunta2():
    # Your logic for the quiz page
    return render_template('pregunta2.html')


# Define the route for pregunta3
@app.route('/pregunta3')
def pregunta3():
    # Your logic for the quiz page
    return render_template('pregunta3.html')


# Define the route for resultados
@app.route('/resultados')
def resultados():
    # Your logic for the quiz page
    return render_template('resultados.html')

# Define the route for dashboard
@app.route('/user')
def user():
    # Your logic for the quiz page
    return render_template('user.html')


# Define the route for dashboard
@app.route('/user2')
def user2():
    # Your logic for the quiz page
    return render_template('user2.html')



if __name__ == "__main__":
    app.run(debug=True)
