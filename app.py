from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuración de conexión
import mysql.connector
def get_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="rico_aves"
    )

# RUTA: INICIO
@app.route('/')
def inicio():
    return render_template('index.html')

# RUTA: PRODUCTOS
@app.route('/productos')
def productos():
    return render_template('producto.html')

# RUTA: CONTACTO (GET para ver, POST para guardar)
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        email = request.form['email']
        mensaje = request.form.get('mensaje', '') 

        conn = get_db()
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nombre, telefono, direccion, email) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, telefono, direccion, email))
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('contactos.html', enviado=True, nombre=nombre)
    
    return render_template('contactos.html', enviado=False)

if __name__ == '__main__':
    app.run(debug=True)
