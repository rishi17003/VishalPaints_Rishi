from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from mysql.connector import connect
import io
from flask import send_file

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aloobhujiya'
app.config['MYSQL_DB'] = 'vishalpaints'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product_rate_calculator', methods=['GET', 'POST'])
def product_rate_calculator():
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        yield_amount = request.form['yield']
        total_rate = 0

        raw_materials = request.form.getlist('raw_materials')
        quantities = request.form.getlist('quantities')

        cur = mysql.connection.cursor()
        for material, quantity in zip(raw_materials, quantities):
            cur.execute("SELECT price FROM raw_materials WHERE name=%s", [material])
            price = cur.fetchone()[0]
            total_rate += price * float(quantity)

        cur.execute("INSERT INTO products (product_name, description, yield, total_rate) VALUES (%s, %s, %s, %s)",
                    (product_name, description, yield_amount, total_rate))
        product_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('invoice', product_id=product_id))

    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM raw_materials")
    raw_materials = cur.fetchall()
    cur.close()

    return render_template('product_rate_calculator.html', raw_materials=raw_materials)

@app.route('/product_history')
def product_history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return render_template('product_history.html', products=products)

@app.route('/raw_material_management', methods=['GET', 'POST'])
def raw_material_management():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        mat_type = request.form['mat_type']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO raw_materials (name, price, mat_type) VALUES (%s, %s, %s)",
                    (name, price, mat_type))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('raw_material_management'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM raw_materials")
    raw_materials = cur.fetchall()
    cur.close()
    return render_template('raw_material_management.html', raw_materials=raw_materials)

@app.route('/inventory_details')
def inventory_details():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM raw_materials")
    raw_materials = cur.fetchall()
    cur.close()
    return render_template('inventory_details.html', raw_materials=raw_materials)

@app.route('/raw_material_history')
def raw_material_history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM raw_materials")
    raw_materials = cur.fetchall()
    cur.close()
    return render_template('raw_material_history.html', raw_materials=raw_materials)

# @app.route('/invoice/<int:product_id>')
# def invoice(product_id):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM products WHERE product_id = %s", [product_id])
#     product = cur.fetchone()
#     cur.close()
#     return render_template('invoice.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)