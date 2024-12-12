from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = 'superss'

# Initialize the database
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            lname TEXT,
            email TEXT NOT NULL,
            phone INT NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('base.html', title="Home", varadd = url_for('add_student'), varsrc = url_for('search_student'))

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        grade = request.form['grade']
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (fname, lname, email, phone, grade) VALUES (?, ?, ?, ?, ?)', (fname, lname, email, phone, grade))
        conn.commit()
        conn.close()
    
        flash(f'Student "{fname}" added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_student.html', title="Add Student")

@app.route('/search-student', methods=['GET', 'POST'])
def search_student():
    students = []
    if request.method == 'POST':
        fname = request.form['fname']
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE fname LIKE ?', (f'%{fname}%',))
        students = cursor.fetchall()
        conn.close()
            
    return render_template('search_student.html', title="Search Student", students=students)  

if __name__ == '__main__':
    app.secret_key = 'superss'
    init_db()
    app.run(debug=True)
