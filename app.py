from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from threading import Lock

app = Flask(__name__)
db_lock = Lock()

# Init SQLite db
def init_db():
    with db_lock:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            date_of_birth TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

init_db()

# Route for the input form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        date_of_birth = request.form['date_of_birth']

        # Insert data into database
        with db_lock:
            conn = sqlite3.connect('users.db', check_same_thread=False)
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (name, email, age, date_of_birth) VALUES (?, ?, ?, ?)", (name, email, int(age), date_of_birth))
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                return "Error: Email already exists.", 400
            except sqlite3.OperationalError:
                conn.close()
                return "Error: Database is locked. Please try again.", 500
            conn.close()

        return redirect(url_for('display'))
    return render_template('index.html')

# Route to display the data
@app.route('/display')
def display():
    with db_lock:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
    return render_template('display.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)