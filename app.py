from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
con = sqlite3.connect('users.db')

def init_db():
    cs = con.cursor()
    cs.execute('''
        Create table if not exists users(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            Age INTEGER NOT NULL,
            Date_Of_Birth TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

@app.route('/')
def init():
    return "Init Setup"

if __name__ == '__main__':
    app.run(debug=True)