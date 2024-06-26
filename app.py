from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (name, email, phone, password) VALUES (%s, %s, %s, %s)', 
                       (name, email, phone, password))
        mysql.connection.commit()
        cursor.close()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if role == 'admin':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM admin WHERE email = %s', (email,))
            admin = cursor.fetchone()
            cursor.close()
            
            if admin and admin['password'] == password:
                session['logged_in'] = True
                session['email'] = admin['email']
                session['role'] = 'admin'
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Admin login failed. Check your email and password.', 'danger')
        elif role == 'user':
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s OR phone = %s', (email, email))
            user = cursor.fetchone()
            cursor.close()
            
            if user and bcrypt.check_password_hash(user['password'], password):
                session['logged_in'] = True
                session['user_id'] = user['id']
                session['role'] = 'user'
                flash('User login successful!', 'success')
                return redirect(url_for('user_dashboard'))
            else:
                flash('User login failed. Check your email/phone and password.', 'danger')
    return render_template('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'logged_in' in session and session['role'] == 'admin':
        return render_template('admin-dashboard.html')
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    
@app.route('/user-dashboard')
def user_dashboard():
    if 'logged_in' in session:
        return render_template('user-dashboard.html')
    
@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
