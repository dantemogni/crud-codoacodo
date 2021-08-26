from flask import Flask  # Importamos el framework Flask
# Importamos el render para mostrar todos los templates
from flask import render_template, request, redirect
from flaskext.mysql import MySQL  # Importamos para conectarnos a la BD
from datetime import datetime  # Nos permitirá darle el nombre a la foto
import os  # Nos pemite acceder a los archivos

app = Flask(__name__)  # Creamos la aplicación

mysql = MySQL()

# Creamos la referencia al host, para que se conecte a la base de datos MYSQL utilizamos el host localhost
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# Indicamos el usuario, por defecto es user
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''  # Sin contraseña, se puede omitir
app.config['MYSQL_DATABASE_BD'] = 'sistema'  # Nombre de nuestra BD

mysql.init_app(app)  # Creamos la conexión con los datos

CARPETA = os.path.join('uploads')  # Referencia a la carpeta
# Indicamos que vamos a guardar esta ruta de la carpeta
app.config['CARPETA'] = CARPETA


@app.route('/')  # Hacemos el ruteo para que el usuario entre en la raiz
def index():
    sql = "SELECT * FROM `sistema`.`empleados`;"
    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos
    cursor.execute(sql)  # Ejecutamos la sentencia SQL
    empleados = cursor.fetchall()  # Traemos toda la información
    conn.commit()  # Cerramos la conexión

    # Identifica la carpeta y el archivo htm
    return render_template('empleados/index.html', empleados=empleados)


@app.route('/destroy/<int:id>')  # Recibe como parámetro el id del registro
def destroy(id):
    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos

    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s",id) #Buscamos la foto
    fila = cursor.fetchall() #Traemos toda la información
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) #Ese valor seleccionado se encuentra en la posición 0 y la fila

    cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
    conn.commit()  # Cerramos la

    return redirect('/')  # Regresamos de donde vinimos


@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos
    # Ejecutamos la sentendia SQL sobre el registro de dicha ID
    cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
    empleados = cursor.fetchall()
    conn.commit()  # Cerramos la conexión

    return render_template('empleados/edit.html', empleados=empleados)


@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtID']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")  # Años horas minutos y segundos

    if _foto.filename != '':
        nuevoNombreFoto = tiempo+_foto.filename  # Concatena el nombre
        _foto.save("uploads/"+nuevoNombreFoto)  # Lo guarda en la carpeta

    sql = "UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
    datos = (_nombre, _correo, id)

    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos

    cursor.execute(sql, datos)  # Ejecutamos la sentencia SQL

    # Buscamos la foto
    cursor.execute("SELECT foto FROM `sistema`.`empleados` WHERE id=%s", id)
    fila = cursor.fetchall()  # Traemos toda la información

    # Ese valor seleccionado se encuentra en la posición 0 y la fila 0
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    cursor.execute("UPDATE `sistema`.`empleados` SET foto=%s WHERE id=%s",
                   (nuevoNombreFoto, id))  # Buscamos la foto

    conn.commit()  # Cerramos la conexión

    return redirect('/')


@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    now = datetime.now()  # Para añadir al nombre del archivo subido
    tiempo = now.strftime("%Y%H%M%S")  # Años horas minutos y segundos

    if _foto.filename != '':
        nuevoNombreFoto = tiempo + _foto.filename  # Concatena el nombre
        # Lo guarda en la carpeta 'uploads'
        _foto.save('uploads/'+nuevoNombreFoto)

    sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()  # Se conecta a la conexión mysql.init_app(app)
    cursor = conn.cursor()  # Almacenaremos lo que ejecutamos
    cursor.execute(sql, datos)  # Ejecutamos la sentencia SQL
    conn.commit()  # Cerramos la conexión

    # Identifica la carpeta y el archivo html
    return render_template('empleados/index.html')


if __name__ == '__main__':  # Estas lìneas de código las requiere python para que se pueda empezar a trabajar con la aplicación
    # Corremos la aplicación en modo debug (con el código activamos el debugger)
    app.run(debug=True)
