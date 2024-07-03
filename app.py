from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from mysql.connector import connect
import io
from io import BytesIO
from flask import send_file
from flask import Flask, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rishi@271'
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
        yield_amount = int(request.form['yield'])
        viscosity = float(request.form['viscosity'])
        weight_lit = float(request.form['weight_lit'])
        container_cost = float(request.form['container_cost'])
        transport_cost = float(request.form['transport_cost'])
        sales_cost = float(request.form['sales_cost'])
        misc_cost = float(request.form['misc_cost'])
        total_rate = float(request.form['total_rate'])
        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO products (product_name, description, yield, viscosity, weight_lit, container_cost, 
                                  transport_cost, sales_cost, misc_cost, total_rate) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (product_name, description, yield_amount, viscosity, weight_lit, container_cost, 
             transport_cost, sales_cost, misc_cost, total_rate)
        )
        mysql.connection.commit()
        cur.close()
        material_types = request.form.getlist('materialType1')
        raw_materials = request.form.getlist('materialName1')
        quantities = request.form.getlist('quantity1')
        
        conn = mysql.connection
        cur = conn.cursor()
        
        invoice_items = []
        for material_type, material_name, quantity in zip(material_types, raw_materials, quantities):
            cur.execute("SELECT price FROM raw_materials WHERE name = %s", [material_name])
            rate_per_unit = cur.fetchone()[0]
            total_cost = int(quantity) * float(rate_per_unit)
            invoice_items.append((material_name, int(quantity), float(rate_per_unit), total_cost))
        
        cur.close()

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Left side: yield, viscosity, weight/lit
        p.drawString(50, height - 50, f"Yield: {yield_amount}")
        p.drawString(50, height - 70, f"Viscosity: {viscosity}")
        p.drawString(50, height - 90, f"Weight / Lit: {weight_lit}")

        # Right side: container, transport, sales, misc cost
        p.drawString(width - 200, height - 50, f"Container Cost: Rs {container_cost}")
        p.drawString(width - 200, height - 70, f"Transport Cost: Rs {transport_cost}")
        p.drawString(width - 200, height - 90, f"Sales Cost: Rs {sales_cost}")
        p.drawString(width - 200, height - 110, f"Misc. Cost: Rs {misc_cost}")

        # Draw a horizontal line
        p.line(50, height - 130, width - 50, height - 130)

        # Draw Table for Materials
        table_data = [["Material Name", "Quantity", "Rate per Unit (Rs)", "Total Cost (Rs)"]]
        for item in invoice_items:
            table_data.append([item[0], item[1], item[2], item[3]])
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        table = Table(table_data, colWidths=[7 * cm, 3 * cm, 5 * cm, 5 * cm])
        table.setStyle(table_style)
        table.wrapOn(p, width - 100, height)
        table.drawOn(p, 50, height - 300)

        # Display total cost at the bottom
        p.drawString(50, height - 320, f"Total Cost: Rs {total_rate}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='invoice.pdf', mimetype='application/pdf')
        # return redirect(url_for('product_history'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, mat_type FROM raw_materials")
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

@app.route('/raw_material_management', methods=['GET'])
def raw_material_management():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, name, price, mat_type FROM raw_materials WHERE deleted = FALSE")
    raw_materials = cursor.fetchall()
    return render_template('raw_material_management.html', raw_materials=raw_materials)

@app.route('/update_material', methods=['POST'])
def update_material():
    material_id = request.form['material_id']
    name = request.form['name']
    price = request.form['price']
    mat_type = request.form['mat_type']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("UPDATE raw_materials SET name=%s, price=%s, mat_type=%s WHERE id=%s", (name, price, mat_type, material_id))
    mysql.connection.commit()
    return jsonify(success=True)

@app.route('/delete_material', methods=['POST'])
def delete_material():
    material_id = request.form['material_id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM raw_materials WHERE id=%s", (material_id,))
    mysql.connection.commit()
    return jsonify(success=True)

@app.route('/add_material', methods=['POST'])
def add_material():
    name = request.form['name']
    price = request.form['price']
    mat_type = request.form['mat_type']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO raw_materials (name, price, mat_type, deleted) VALUES (%s, %s, %s, FALSE)", (name, price, mat_type))
    mysql.connection.commit()
    return jsonify(success=True)

    
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



@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    product_name = request.form['product_name']
    description = request.form['description']
    yield_value = request.form['yield']
    viscosity = request.form['viscosity']
    weight_lit = request.form['weight_lit']
    container_cost = float(request.form['container_cost'])
    transport_cost = float(request.form['transport_cost'])
    sales_cost = float(request.form['sales_cost'])
    misc_cost = float(request.form['misc_cost'])
    total_rate = float(request.form['total_rate'])
    
    material_types = request.form.getlist('materialType1')
    raw_materials = request.form.getlist('materialName1')
    quantities = request.form.getlist('quantity1')
    
    conn = mysql.connection
    cur = conn.cursor()
    
    invoice_items = []
    for material_type, material_name, quantity in zip(material_types, raw_materials, quantities):
        cur.execute("SELECT price FROM raw_materials WHERE name = %s", [material_name])
        rate_per_unit = cur.fetchone()[0]
        total_cost = int(quantity) * float(rate_per_unit)
        invoice_items.append((material_name, int(quantity), float(rate_per_unit), total_cost))
    
    cur.close()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Left side: yield, viscosity, weight/lit
    p.drawString(50, height - 50, f"Yield: {yield_value}")
    p.drawString(50, height - 70, f"Viscosity: {viscosity}")
    p.drawString(50, height - 90, f"Weight / Lit: {weight_lit}")

    # Right side: container, transport, sales, misc cost
    p.drawString(width - 200, height - 50, f"Container Cost: Rs {container_cost}")
    p.drawString(width - 200, height - 70, f"Transport Cost: Rs {transport_cost}")
    p.drawString(width - 200, height - 90, f"Sales Cost: Rs {sales_cost}")
    p.drawString(width - 200, height - 110, f"Misc. Cost: Rs {misc_cost}")

    # Draw a horizontal line
    p.line(50, height - 130, width - 50, height - 130)

    # Draw Table for Materials
    table_data = [["Material Name", "Quantity", "Rate per Unit (Rs)", "Total Cost (Rs)"]]
    for item in invoice_items:
        table_data.append([item[0], item[1], item[2], item[3]])
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    
    table = Table(table_data, colWidths=[7 * cm, 3 * cm, 5 * cm, 5 * cm])
    table.setStyle(table_style)
    table.wrapOn(p, width - 100, height)
    table.drawOn(p, 50, height - 300)

    # Display total cost at the bottom
    p.drawString(50, height - 320, f"Total Cost: Rs {total_rate}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='invoice.pdf', mimetype='application/pdf')
if __name__ == '__main__':
    app.run(debug=True)