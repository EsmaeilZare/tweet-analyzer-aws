import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/create', methods=('GET', 'POST'))
def analyze():
    return render_template('create.html')


@app.route('/analyze', methods=('GET', 'POST'))
def analyze_tweets():
    if request.method == 'POST':
        source = request.form['source']
        start_index = request.form['start_index']
        end_index = request.form['end_index']

        if not source:
            flash('Source is required!')
        else:
            conn = get_db_connection()
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')
