from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def init():
    return "Init Setup"

if __name__ == '__main__':
    app.run(debug=True)